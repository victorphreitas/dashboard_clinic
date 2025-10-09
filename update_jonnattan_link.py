"""
Script para atualizar o link da planilha do Dr. Jonnattan
"""

from database import cliente_crud, db_manager
from sqlalchemy.orm import sessionmaker

def update_jonnattan_link():
    """Atualiza o link da planilha do Dr. Jonnattan"""
    print("🔄 Atualizando link da planilha do Dr. Jonnattan...")
    
    # Buscar cliente Dr. Jonnattan
    clientes = cliente_crud.get_all_clientes()
    jonnattan = None
    
    for cliente in clientes:
        if 'Jonnattan' in cliente.nome_da_clinica:
            jonnattan = cliente
            break
    
    if not jonnattan:
        print("❌ Dr. Jonnattan não encontrado")
        return False
    
    print(f"🏥 Clínica encontrada: {jonnattan.nome_da_clinica}")
    print(f"📧 Email: {jonnattan.email}")
    print(f"🔗 Link atual: {jonnattan.link_empresa}")
    
    # Solicitar novo link
    print(f"\\n💡 SOLUÇÕES:")
    print(f"   1. Criar nova planilha e compartilhar")
    print(f"   2. Usar planilha existente que funciona")
    print(f"   3. Verificar se o link atual está correto")
    
    print(f"\\n📋 Para atualizar o link:")
    print(f"   1. Crie uma nova planilha")
    print(f"   2. Compartilhe com: dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com")
    print(f"   3. Copie o novo link")
    print(f"   4. Execute este script novamente com o novo link")
    
    # Exemplo de como atualizar (descomente quando tiver o novo link)
    """
    novo_link = "https://docs.google.com/spreadsheets/d/NOVO_ID/edit"
    
    # Atualizar no banco
    session = db_manager.get_session()
    try:
        jonnattan.link_empresa = novo_link
        session.commit()
        print(f"✅ Link atualizado com sucesso!")
        print(f"🔗 Novo link: {novo_link}")
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")
        session.rollback()
        return False
    finally:
        session.close()
    """
    
    return False

def test_new_link():
    """Testa se o novo link funciona"""
    print("\\n🧪 Para testar o novo link:")
    print("   1. Execute: python test_jonnattan.py")
    print("   2. Se funcionar, execute: python check_empty_clinics.py")
    print("   3. Verifique no dashboard se os dados aparecem")

if __name__ == "__main__":
    print("🏥 ATUALIZAÇÃO DE LINK - DR. JONNATTAN")
    print("=" * 50)
    
    success = update_jonnattan_link()
    
    if success:
        test_new_link()
    else:
        print("\\n💡 Siga as instruções acima para resolver o problema")

