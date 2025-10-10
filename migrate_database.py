"""
Script de migração do banco de dados para o novo formato.
Atualiza a estrutura do banco para suportar os novos campos da planilha.
"""

import os
import sqlite3
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def migrate_database():
    """Migra o banco de dados para o novo formato"""
    
    # Conectar ao banco
    database_url = os.getenv('DATABASE_URL', 'sqlite:///prestige_clinic.db')
    engine = create_engine(database_url)
    
    print("🔄 Iniciando migração do banco de dados...")
    
    with engine.connect() as conn:
        try:
            # Verificar se as novas colunas já existem
            result = conn.execute(text("PRAGMA table_info(dados_dashboard)"))
            columns = [row[1] for row in result.fetchall()]
            
            # Novos campos a serem adicionados
            new_columns = [
                ('valor_investido_total', 'REAL DEFAULT 0.0'),
                ('orcamento_previsto_total', 'REAL DEFAULT 0.0'),
                ('orcamento_realizado_facebook', 'REAL DEFAULT 0.0'),
                ('orcamento_previsto_facebook', 'REAL DEFAULT 0.0'),
                ('orcamento_realizado_google', 'REAL DEFAULT 0.0'),
                ('orcamento_previsto_google', 'REAL DEFAULT 0.0'),
                ('conversao_csm_leads', 'REAL DEFAULT 0.0'),
                ('conversao_csc_csm', 'REAL DEFAULT 0.0'),
                ('conversao_fechamento_csc', 'REAL DEFAULT 0.0'),
                ('conversao_fechamento_leads', 'REAL DEFAULT 0.0'),
                ('custo_por_compra_cirurgias', 'REAL DEFAULT 0.0'),
                ('custo_por_lead_total', 'REAL DEFAULT 0.0'),
                ('custo_por_consulta_marcada', 'REAL DEFAULT 0.0'),
                ('custo_por_consulta_comparecida', 'REAL DEFAULT 0.0'),
                ('ticket_medio', 'REAL DEFAULT 0.0'),
                ('taxa_ideal_csm', 'REAL DEFAULT 10.0'),
                ('taxa_ideal_csc', 'REAL DEFAULT 50.0'),
                ('taxa_ideal_fechamentos', 'REAL DEFAULT 40.0')
            ]
            
            # Adicionar novas colunas se não existirem
            for column_name, column_type in new_columns:
                if column_name not in columns:
                    print(f"   ➕ Adicionando coluna: {column_name}")
                    conn.execute(text(f"ALTER TABLE dados_dashboard ADD COLUMN {column_name} {column_type}"))
                else:
                    print(f"   ✅ Coluna já existe: {column_name}")
            
            # Migrar dados existentes
            print("   🔄 Migrando dados existentes...")
            
            # Copiar investimento_total para valor_investido_total se necessário
            conn.execute(text("""
                UPDATE dados_dashboard 
                SET valor_investido_total = investimento_total 
                WHERE valor_investido_total = 0 AND investimento_total > 0
            """))
            
            # Copiar investimento_facebook para orcamento_realizado_facebook se necessário
            conn.execute(text("""
                UPDATE dados_dashboard 
                SET orcamento_realizado_facebook = investimento_facebook 
                WHERE orcamento_realizado_facebook = 0 AND investimento_facebook > 0
            """))
            
            # Copiar investimento_google para orcamento_realizado_google se necessário
            conn.execute(text("""
                UPDATE dados_dashboard 
                SET orcamento_realizado_google = investimento_google 
                WHERE orcamento_realizado_google = 0 AND investimento_google > 0
            """))
            
            conn.commit()
            print("✅ Migração concluída com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro na migração: {e}")
            conn.rollback()
            raise

def verify_migration():
    """Verifica se a migração foi bem-sucedida"""
    
    database_url = os.getenv('DATABASE_URL', 'sqlite:///prestige_clinic.db')
    engine = create_engine(database_url)
    
    print("🔍 Verificando migração...")
    
    with engine.connect() as conn:
        try:
            # Verificar se as novas colunas existem
            result = conn.execute(text("PRAGMA table_info(dados_dashboard)"))
            columns = [row[1] for row in result.fetchall()]
            
            required_columns = [
                'valor_investido_total',
                'orcamento_previsto_total',
                'orcamento_realizado_facebook',
                'orcamento_previsto_facebook',
                'orcamento_realizado_google',
                'orcamento_previsto_google',
                'conversao_csm_leads',
                'conversao_csc_csm',
                'conversao_fechamento_csc',
                'conversao_fechamento_leads',
                'custo_por_compra_cirurgias',
                'custo_por_lead_total',
                'custo_por_consulta_marcada',
                'custo_por_consulta_comparecida',
                'ticket_medio',
                'taxa_ideal_csm',
                'taxa_ideal_csc',
                'taxa_ideal_fechamentos'
            ]
            
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"❌ Colunas faltando: {missing_columns}")
                return False
            else:
                print("✅ Todas as colunas foram criadas com sucesso!")
                return True
                
        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            return False

if __name__ == "__main__":
    print("🚀 MIGRAÇÃO DO BANCO DE DADOS - NOVO FORMATO")
    print("=" * 50)
    
    try:
        migrate_database()
        if verify_migration():
            print("\n🎉 Migração concluída com sucesso!")
            print("📊 O banco de dados agora suporta o novo formato da planilha.")
        else:
            print("\n❌ Migração falhou. Verifique os erros acima.")
    except Exception as e:
        print(f"\n❌ Erro durante a migração: {e}")
