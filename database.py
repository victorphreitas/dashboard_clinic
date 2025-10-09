"""
Módulo de conexão e operações com banco de dados.
Gerencia a conexão com SQLite e operações CRUD.
"""

import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any
import bcrypt
from datetime import datetime
from dotenv import load_dotenv

from models import Base, Cliente, DadosDashboard

# Carregar variáveis de ambiente
load_dotenv()

class DatabaseManager:
    """Gerenciador de conexão e operações com banco de dados"""
    
    def __init__(self, database_url: str = None):
        """
        Inicializa o gerenciador de banco de dados
        
        Args:
            database_url: URL de conexão com o banco (SQLite por padrão)
        """
        # Usar variável de ambiente se disponível, senão usar padrão
        self.database_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///prestige_clinic.db')
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Cria todas as tabelas no banco de dados"""
        try:
            Base.metadata.create_all(bind=self.engine)
            print("✅ Tabelas criadas com sucesso!")
        except SQLAlchemyError as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            raise
    
    def get_session(self) -> Session:
        """Retorna uma sessão do banco de dados"""
        return self.SessionLocal()
    
    def close_session(self, session: Session):
        """Fecha uma sessão do banco de dados"""
        session.close()

class ClienteCRUD:
    """Operações CRUD para a tabela de clientes"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def hash_password(self, password: str) -> str:
        """Gera hash da senha usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_cliente(self, nome: str, email: str, senha: str, cnpj: str = None, 
                      nome_da_clinica: str = "", telefone: str = None, 
                      endereco: str = None, link_empresa: str = None, is_admin: bool = False) -> Optional[Cliente]:
        """Cria um novo cliente"""
        session = self.db_manager.get_session()
        try:
            # Verifica se email já existe
            existing = session.query(Cliente).filter(Cliente.email == email).first()
            if existing:
                return None
            
            cliente = Cliente(
                nome=nome,
                email=email,
                senha_hash=self.hash_password(senha),
                cnpj=cnpj,
                nome_da_clinica=nome_da_clinica,
                telefone=telefone,
                endereco=endereco,
                link_empresa=link_empresa,
                is_admin=is_admin
            )
            
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            return cliente
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Erro ao criar cliente: {e}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def authenticate_cliente(self, email: str, senha: str) -> Optional[Cliente]:
        """Autentica um cliente"""
        session = self.db_manager.get_session()
        try:
            cliente = session.query(Cliente).filter(
                Cliente.email == email,
                Cliente.ativo == True
            ).first()
            
            if cliente and self.verify_password(senha, cliente.senha_hash):
                return cliente
            return None
        except SQLAlchemyError as e:
            print(f"❌ Erro na autenticação: {e}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def get_cliente_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca cliente por ID"""
        session = self.db_manager.get_session()
        try:
            return session.query(Cliente).filter(Cliente.id == cliente_id).first()
        except SQLAlchemyError as e:
            print(f"❌ Erro ao buscar cliente: {e}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def get_all_clientes(self) -> List[Cliente]:
        """Lista todos os clientes ativos"""
        session = self.db_manager.get_session()
        try:
            return session.query(Cliente).filter(Cliente.ativo == True).all()
        except SQLAlchemyError as e:
            print(f"❌ Erro ao listar clientes: {e}")
            return []
        finally:
            self.db_manager.close_session(session)

class DadosDashboardCRUD:
    """Operações CRUD para a tabela de dados do dashboard"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_dados_dashboard(self, cliente_id: int, mes: str, ano: int = 2024, **kwargs) -> Optional[DadosDashboard]:
        """Cria novos dados do dashboard para um cliente"""
        session = self.db_manager.get_session()
        try:
            dados = DadosDashboard(
                cliente_id=cliente_id,
                mes=mes,
                ano=ano,
                **kwargs
            )
            session.add(dados)
            session.commit()
            session.refresh(dados)
            return dados
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Erro ao criar dados do dashboard: {e}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def get_dados_by_cliente(self, cliente_id: int) -> List[DadosDashboard]:
        """Busca todos os dados de um cliente"""
        session = self.db_manager.get_session()
        try:
            return session.query(DadosDashboard).filter(
                DadosDashboard.cliente_id == cliente_id
            ).order_by(DadosDashboard.ano, DadosDashboard.mes).all()
        except SQLAlchemyError as e:
            print(f"❌ Erro ao buscar dados do cliente: {e}")
            return []
        finally:
            self.db_manager.close_session(session)
    
    def get_dados_by_cliente_and_period(self, cliente_id: int, meses: List[str]) -> List[DadosDashboard]:
        """Busca dados de um cliente para meses específicos"""
        session = self.db_manager.get_session()
        try:
            return session.query(DadosDashboard).filter(
                DadosDashboard.cliente_id == cliente_id,
                DadosDashboard.mes.in_(meses)
            ).order_by(DadosDashboard.ano, DadosDashboard.mes).all()
        except SQLAlchemyError as e:
            print(f"❌ Erro ao buscar dados do período: {e}")
            return []
        finally:
            self.db_manager.close_session(session)
    
    def dados_to_dataframe(self, dados: List[DadosDashboard]) -> pd.DataFrame:
        """Converte dados do banco para DataFrame do pandas"""
        if not dados:
            return pd.DataFrame()
        
        # Mapeia os dados para o formato esperado pelo dashboard
        data = {
            'Meses': [d.mes for d in dados],
            'Leads_Totais': [d.leads_totais for d in dados],
            'Leads_Google_Ads': [d.leads_google_ads for d in dados],
            'Leads_Meta_Ads': [d.leads_meta_ads for d in dados],
            'Leads_Instagram_Organico': [d.leads_instagram_organico for d in dados],
            'Leads_Indicacao': [d.leads_indicacao for d in dados],
            'Leads_Origem_Desconhecida': [d.leads_origem_desconhecida for d in dados],
            
            'Consultas_Marcadas_Totais': [d.consultas_marcadas_totais for d in dados],
            'Consultas_Marcadas_Google_Ads': [d.consultas_marcadas_google_ads for d in dados],
            'Consultas_Marcadas_Meta_Ads': [d.consultas_marcadas_meta_ads for d in dados],
            'Consultas_Marcadas_IG_Organico': [d.consultas_marcadas_ig_organico for d in dados],
            'Consultas_Marcadas_Indicacao': [d.consultas_marcadas_indicacao for d in dados],
            'Consultas_Marcadas_Outros': [d.consultas_marcadas_outros for d in dados],
            
            'Consultas_Comparecidas': [d.consultas_comparecidas for d in dados],
            'Fechamentos_Totais': [d.fechamentos_totais for d in dados],
            'Fechamentos_Google_Ads': [d.fechamentos_google_ads for d in dados],
            'Fechamentos_Meta_Ads': [d.fechamentos_meta_ads for d in dados],
            'Fechamentos_IG_Organico': [d.fechamentos_ig_organico for d in dados],
            'Fechamentos_Indicacao': [d.fechamentos_indicacao for d in dados],
            'Fechamentos_Outros': [d.fechamentos_outros for d in dados],
            
            'Faturamento': [d.faturamento for d in dados],
            'Investimento_Total': [d.investimento_total for d in dados],
            'Investimento_Facebook': [d.investimento_facebook for d in dados],
            'Investimento_Google': [d.investimento_google for d in dados],
        }
        
        df = pd.DataFrame(data)
        
        # Ordena os meses na ordem correta
        if not df.empty:
            # Mapeia os meses para números para ordenação
            mes_order = {
                'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
                'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
                'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
            }
            
            # Adiciona coluna de ordenação
            df['mes_order'] = df['Meses'].map(mes_order)
            
            # Ordena por mês
            df = df.sort_values('mes_order').drop('mes_order', axis=1)
            
            # Calcula KPIs se não estiverem armazenados
            df = self._calculate_kpis(df)
        
        return df
    
    def _calculate_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula KPIs para o DataFrame"""
        def safe_divide(numerator, denominator):
            return np.where(denominator != 0, numerator / denominator, 0)

        df['Conversao_Leads_Csm'] = safe_divide(df['Consultas_Marcadas_Totais'], df['Leads_Totais']) * 100
        df['Conversao_Csm_Csc'] = safe_divide(df['Consultas_Comparecidas'], df['Consultas_Marcadas_Totais']) * 100
        df['Conversao_Csc_Fechamento'] = safe_divide(df['Fechamentos_Totais'], df['Consultas_Comparecidas']) * 100
        df['Conversao_Leads_Fechamento'] = safe_divide(df['Fechamentos_Totais'], df['Leads_Totais']) * 100
        df['Custo_por_Compra'] = safe_divide(df['Investimento_Total'], df['Fechamentos_Totais'])
        df['ROAS'] = safe_divide(df['Faturamento'], df['Investimento_Total'])
        df['Custo_por_Lead'] = safe_divide(df['Investimento_Total'], df['Leads_Totais'])
        df['Custo_por_Consulta_Marcada'] = safe_divide(df['Investimento_Total'], df['Consultas_Marcadas_Totais'])
        df['Custo_por_Consulta_Comparecida'] = safe_divide(df['Investimento_Total'], df['Consultas_Comparecidas'])
        df['Ticket_Medio'] = safe_divide(df['Faturamento'], df['Fechamentos_Totais'])
        
        # Substitui valores infinitos e NaN por 0
        df = df.replace([np.inf, -np.inf, np.nan], 0)
        
        return df
    
    def update_dados_dashboard(self, dados_id: int, **kwargs) -> bool:
        """Atualiza dados do dashboard"""
        session = self.db_manager.get_session()
        try:
            dados = session.query(DadosDashboard).filter(DadosDashboard.id == dados_id).first()
            if not dados:
                return False
            
            for key, value in kwargs.items():
                if hasattr(dados, key):
                    setattr(dados, key, value)
            
            dados.data_atualizacao = datetime.utcnow()
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Erro ao atualizar dados: {e}")
            return False
        finally:
            self.db_manager.close_session(session)
    
    def delete_dados_dashboard(self, dados_id: int) -> bool:
        """Remove dados do dashboard"""
        session = self.db_manager.get_session()
        try:
            dados = session.query(DadosDashboard).filter(DadosDashboard.id == dados_id).first()
            if dados:
                session.delete(dados)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Erro ao deletar dados: {e}")
            return False
        finally:
            self.db_manager.close_session(session)

# Instância global do gerenciador de banco
db_manager = DatabaseManager()
cliente_crud = ClienteCRUD(db_manager)
dados_crud = DadosDashboardCRUD(db_manager)

