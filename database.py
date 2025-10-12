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
    
    def update_cliente(self, cliente_id: int, **kwargs) -> bool:
        """Atualiza dados de um cliente"""
        session = self.db_manager.get_session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                return False
            
            # Atualiza apenas os campos fornecidos
            for key, value in kwargs.items():
                if hasattr(cliente, key) and value is not None:
                    if key == 'senha' and value:
                        # Hash da nova senha
                        setattr(cliente, 'senha_hash', self.hash_password(value))
                    else:
                        setattr(cliente, key, value)
            
            cliente.data_atualizacao = datetime.utcnow()
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Erro ao atualizar cliente: {e}")
            return False
        finally:
            self.db_manager.close_session(session)
    
    def delete_cliente(self, cliente_id: int) -> bool:
        """Remove um cliente (soft delete)"""
        session = self.db_manager.get_session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                return False
            
            # Soft delete - marca como inativo
            cliente.ativo = False
            cliente.data_atualizacao = datetime.utcnow()
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Erro ao deletar cliente: {e}")
            return False
        finally:
            self.db_manager.close_session(session)
    
    def hard_delete_cliente(self, cliente_id: int) -> bool:
        """Remove um cliente permanentemente (hard delete)"""
        session = self.db_manager.get_session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                return False
            
            # Remove dados relacionados primeiro (cascade)
            session.query(DadosDashboard).filter(DadosDashboard.cliente_id == cliente_id).delete()
            
            # Remove o cliente
            session.delete(cliente)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Erro ao deletar cliente permanentemente: {e}")
            return False
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
            'Cliente_ID': [d.cliente_id for d in dados],
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
            'Valor_Investido_Total': [d.valor_investido_total for d in dados],
            'Orcamento_Previsto_Total': [d.orcamento_previsto_total for d in dados],
            'Orcamento_Realizado_Facebook': [d.orcamento_realizado_facebook for d in dados],
            'Orcamento_Previsto_Facebook': [d.orcamento_previsto_facebook for d in dados],
            'Orcamento_Realizado_Google': [d.orcamento_realizado_google for d in dados],
            'Orcamento_Previsto_Google': [d.orcamento_previsto_google for d in dados],
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
        """Calcula KPIs para o DataFrame conforme novo formato"""
        def safe_divide(numerator, denominator):
            return np.where(denominator != 0, numerator / denominator, 0)

        # KPIs de conversão (em percentual)
        df['Conversao_Csm_Leads'] = safe_divide(df['Consultas_Marcadas_Totais'], df['Leads_Totais']) * 100
        df['Conversao_Csc_Csm'] = safe_divide(df['Consultas_Comparecidas'], df['Consultas_Marcadas_Totais']) * 100
        df['Conversao_Fechamento_Csc'] = safe_divide(df['Fechamentos_Totais'], df['Consultas_Comparecidas']) * 100
        df['Conversao_Fechamento_Leads'] = safe_divide(df['Fechamentos_Totais'], df['Leads_Totais']) * 100
        
        # KPIs financeiros
        df['Custo_por_Compra_Cirurgias'] = safe_divide(df['Valor_Investido_Total'], df['Fechamentos_Totais'])
        df['ROAS'] = safe_divide(df['Faturamento'], df['Valor_Investido_Total'])
        df['Custo_por_Lead_Total'] = safe_divide(df['Valor_Investido_Total'], df['Leads_Totais'])
        df['Custo_por_Consulta_Marcada'] = safe_divide(df['Valor_Investido_Total'], df['Consultas_Marcadas_Totais'])
        df['Custo_por_Consulta_Comparecida'] = safe_divide(df['Valor_Investido_Total'], df['Consultas_Comparecidas'])
        df['Ticket_Medio'] = safe_divide(df['Faturamento'], df['Fechamentos_Totais'])
        
        # Taxas ideais (thresholds)
        df['Taxa_Ideal_Csm'] = 10.0  # Csm. = Consultas Marcadas >10%
        df['Taxa_Ideal_Csc'] = 50.0  # Csc. = Consultas Comparecidas >50%
        df['Taxa_Ideal_Fechamentos'] = 40.0  # Fechamentos >40%
        
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

class AdminDashboardCRUD:
    """Operações CRUD para dashboard consolidado do administrador"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_consolidated_metrics(self) -> Dict[str, Any]:
        """Retorna métricas consolidadas de todas as clínicas"""
        session = self.db_manager.get_session()
        try:
            # Busca todos os dados de todas as clínicas (exceto admin)
            dados = session.query(DadosDashboard).join(Cliente).filter(
                Cliente.is_admin == False,
                Cliente.ativo == True
            ).all()
            
            if not dados:
                return {
                    'total_leads': 0,
                    'total_consultas_marcadas': 0,
                    'total_consultas_comparecidas': 0,
                    'total_fechamentos': 0,
                    'total_faturamento': 0,
                    'total_investimento': 0,
                    'roas_medio': 0,
                    'custo_por_lead_medio': 0,
                    'ticket_medio': 0,
                    'clinicas_ativas': 0,
                    'meses_ativos': 0
                }
            
            # Agregação dos dados
            total_leads = sum(d.leads_totais for d in dados)
            total_consultas_marcadas = sum(d.consultas_marcadas_totais for d in dados)
            total_consultas_comparecidas = sum(d.consultas_comparecidas for d in dados)
            total_fechamentos = sum(d.fechamentos_totais for d in dados)
            total_faturamento = sum(d.faturamento for d in dados)
            total_investimento = sum(d.valor_investido_total for d in dados)
            
            # Cálculos de médias
            roas_medio = (total_faturamento / total_investimento) if total_investimento > 0 else 0
            custo_por_lead_medio = (total_investimento / total_leads) if total_leads > 0 else 0
            ticket_medio = (total_faturamento / total_fechamentos) if total_fechamentos > 0 else 0
            
            # Contagem de clínicas ativas
            clinicas_ativas = len(set(d.cliente_id for d in dados))
            
            # Contagem de meses ativos
            meses_ativos = len(set((d.mes, d.ano) for d in dados))
            
            return {
                'total_leads': total_leads,
                'total_consultas_marcadas': total_consultas_marcadas,
                'total_consultas_comparecidas': total_consultas_comparecidas,
                'total_fechamentos': total_fechamentos,
                'total_faturamento': total_faturamento,
                'total_investimento': total_investimento,
                'roas_medio': roas_medio,
                'custo_por_lead_medio': custo_por_lead_medio,
                'ticket_medio': ticket_medio,
                'clinicas_ativas': clinicas_ativas,
                'meses_ativos': meses_ativos
            }
            
        except SQLAlchemyError as e:
            print(f"❌ Erro ao buscar métricas consolidadas: {e}")
            return {}
        finally:
            self.db_manager.close_session(session)
    
    def get_clinics_comparison(self) -> List[Dict[str, Any]]:
        """Retorna dados comparativos entre clínicas"""
        session = self.db_manager.get_session()
        try:
            # Busca dados agrupados por clínica
            from sqlalchemy import func
            
            query = session.query(
                Cliente.nome_da_clinica,
                Cliente.nome,
                func.sum(DadosDashboard.leads_totais).label('total_leads'),
                func.sum(DadosDashboard.consultas_marcadas_totais).label('total_consultas_marcadas'),
                func.sum(DadosDashboard.consultas_comparecidas).label('total_consultas_comparecidas'),
                func.sum(DadosDashboard.fechamentos_totais).label('total_fechamentos'),
                func.sum(DadosDashboard.faturamento).label('total_faturamento'),
                func.sum(DadosDashboard.valor_investido_total).label('total_investimento'),
                func.avg(DadosDashboard.roas).label('roas_medio'),
                func.avg(DadosDashboard.custo_por_lead_total).label('custo_por_lead_medio'),
                func.avg(DadosDashboard.ticket_medio).label('ticket_medio')
            ).join(DadosDashboard).filter(
                Cliente.is_admin == False,
                Cliente.ativo == True
            ).group_by(Cliente.id, Cliente.nome_da_clinica, Cliente.nome)
            
            results = query.all()
            
            clinicas = []
            for result in results:
                clinicas.append({
                    'nome_da_clinica': result.nome_da_clinica,
                    'nome': result.nome,
                    'total_leads': result.total_leads or 0,
                    'total_consultas_marcadas': result.total_consultas_marcadas or 0,
                    'total_consultas_comparecidas': result.total_consultas_comparecidas or 0,
                    'total_fechamentos': result.total_fechamentos or 0,
                    'total_faturamento': result.total_faturamento or 0,
                    'total_investimento': result.total_investimento or 0,
                    'roas_medio': result.roas_medio or 0,
                    'custo_por_lead_medio': result.custo_por_lead_medio or 0,
                    'ticket_medio': result.ticket_medio or 0
                })
            
            return clinicas
            
        except SQLAlchemyError as e:
            print(f"❌ Erro ao buscar comparação de clínicas: {e}")
            return []
        finally:
            self.db_manager.close_session(session)
    
    def get_monthly_evolution(self) -> List[Dict[str, Any]]:
        """Retorna evolução mensal consolidada"""
        session = self.db_manager.get_session()
        try:
            from sqlalchemy import func
            
            query = session.query(
                DadosDashboard.mes,
                DadosDashboard.ano,
                func.sum(DadosDashboard.leads_totais).label('total_leads'),
                func.sum(DadosDashboard.consultas_marcadas_totais).label('total_consultas_marcadas'),
                func.sum(DadosDashboard.consultas_comparecidas).label('total_consultas_comparecidas'),
                func.sum(DadosDashboard.fechamentos_totais).label('total_fechamentos'),
                func.sum(DadosDashboard.faturamento).label('total_faturamento'),
                func.sum(DadosDashboard.valor_investido_total).label('total_investimento')
            ).join(Cliente).filter(
                Cliente.is_admin == False,
                Cliente.ativo == True
            ).group_by(DadosDashboard.mes, DadosDashboard.ano).order_by(
                DadosDashboard.ano, DadosDashboard.mes
            )
            
            results = query.all()
            
            meses = []
            for result in results:
                meses.append({
                    'mes': result.mes,
                    'ano': result.ano,
                    'total_leads': result.total_leads or 0,
                    'total_consultas_marcadas': result.total_consultas_marcadas or 0,
                    'total_consultas_comparecidas': result.total_consultas_comparecidas or 0,
                    'total_fechamentos': result.total_fechamentos or 0,
                    'total_faturamento': result.total_faturamento or 0,
                    'total_investimento': result.total_investimento or 0
                })
            
            return meses
            
        except SQLAlchemyError as e:
            print(f"❌ Erro ao buscar evolução mensal: {e}")
            return []
        finally:
            self.db_manager.close_session(session)
    
    def get_channel_analysis(self) -> Dict[str, Any]:
        """Retorna análise por canal de marketing"""
        session = self.db_manager.get_session()
        try:
            from sqlalchemy import func
            
            query = session.query(
                func.sum(DadosDashboard.leads_google_ads).label('leads_google'),
                func.sum(DadosDashboard.leads_meta_ads).label('leads_meta'),
                func.sum(DadosDashboard.leads_instagram_organico).label('leads_instagram'),
                func.sum(DadosDashboard.leads_indicacao).label('leads_indicacao'),
                func.sum(DadosDashboard.leads_origem_desconhecida).label('leads_desconhecida'),
                func.sum(DadosDashboard.orcamento_realizado_google).label('investimento_google'),
                func.sum(DadosDashboard.orcamento_realizado_facebook).label('investimento_facebook')
            ).join(Cliente).filter(
                Cliente.is_admin == False,
                Cliente.ativo == True
            )
            
            result = query.first()
            
            return {
                'leads_google': result.leads_google or 0,
                'leads_meta': result.leads_meta or 0,
                'leads_instagram': result.leads_instagram or 0,
                'leads_indicacao': result.leads_indicacao or 0,
                'leads_desconhecida': result.leads_desconhecida or 0,
                'investimento_google': result.investimento_google or 0,
                'investimento_facebook': result.investimento_facebook or 0
            }
            
        except SQLAlchemyError as e:
            print(f"❌ Erro ao buscar análise de canais: {e}")
            return {}
        finally:
            self.db_manager.close_session(session)

# Instância global do gerenciador de banco
db_manager = DatabaseManager()
cliente_crud = ClienteCRUD(db_manager)
dados_crud = DadosDashboardCRUD(db_manager)
admin_dashboard_crud = AdminDashboardCRUD(db_manager)

