"""
Script para migrar o banco de dados e criar a nova tabela de procedimentos.
"""

from database import db_manager
from models import Base

def migrate_database():
    """Executa a migração do banco de dados"""
    print("🔄 Iniciando migração do banco de dados...")
    
    try:
        # Cria todas as tabelas (incluindo a nova tabela de procedimentos)
        db_manager.create_tables()
        print("✅ Migração concluída com sucesso!")
        print("📊 Nova tabela 'procedimentos' criada")
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        return False
    
    return True

if __name__ == "__main__":
    migrate_database()
