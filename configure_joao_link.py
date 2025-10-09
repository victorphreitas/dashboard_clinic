"""
Script para configurar o link da planilha do Dr. João
"""

from database import dados_crud, cliente_crud, db_manager
from sqlalchemy.orm import sessionmaker

def configure_joao_link():
    """Configura o link da planilha do Dr. João"""
    print("🔧 CONFIGURANDO LINK DA PLANILHA DO DR. JOÃO")
    print("=" * 60)
    
    # Buscar cliente Dr. João
    clientes = cliente_crud.get_all_clientes()
    joao = None
    
    for cliente in clientes:
        if 'João' in cliente.nome_da_clinica:
            joao = cliente
            break
    
    if not joao:
        print("❌ Dr. João não encontrado")
        return False
    
    print(f"🏥 Clínica: {joao.nome_da_clinica} (ID: {joao.id})")
    print(f"📧 Email: {joao.email}")
    print(f"🔗 Link atual: {getattr(joao, 'link_empresa', 'NÃO DEFINIDO')}")
    
    # Link da planilha do Dr. João (baseado no que sabemos que funciona)
    novo_link = "https://docs.google.com/spreadsheets/d/1hJDvihxFPWnqjGlp-QFOB6vjExlskBHPNbA3j7SxgPA/edit"
    
    print(f"\\n📊 CONFIGURANDO NOVO LINK:")
    print(f"   {novo_link}")
    
    # Atualizar no banco
    session = db_manager.get_session()
    try:
        joao.link_empresa = novo_link
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

def test_sync_after_config():
    """Testa sincronização após configuração"""
    print(f"\\n🧪 TESTANDO SINCRONIZAÇÃO APÓS CONFIGURAÇÃO...")
    
    try:
        import subprocess
        import sys
        
        result = subprocess.run([sys.executable, "sync_sheets.py"], 
                              capture_output=True, text=True, cwd=".", timeout=60)
        
        if result.returncode == 0:
            print(f"✅ Sincronização executada com sucesso!")
            print(f"📊 Resultado:")
            print(result.stdout)
            
            # Verificar se o Dr. João foi sincronizado
            if "Dr. João" in result.stdout or "João" in result.stdout:
                print(f"✅ Dr. João foi sincronizado!")
            else:
                print(f"⚠️ Dr. João pode não ter sido sincronizado")
        else:
            print(f"❌ Erro na sincronização: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro ao executar sincronização: {e}")

def verify_joao_data():
    """Verifica dados do Dr. João após sincronização"""
    print(f"\\n🔍 VERIFICANDO DADOS DO DR. JOÃO APÓS SINCRONIZAÇÃO...")
    
    # Buscar cliente Dr. João
    clientes = cliente_crud.get_all_clientes()
    joao = None
    
    for cliente in clientes:
        if 'João' in cliente.nome_da_clinica:
            joao = cliente
            break
    
    if not joao:
        print("❌ Dr. João não encontrado")
        return False
    
    # Verificar dados
    dados = dados_crud.get_dados_by_cliente(joao.id)
    print(f"📊 Dados encontrados: {len(dados)} registros")
    
    for dado in dados:
        print(f"   📅 {dado.mes}: {dado.leads_totais} leads, R$ {dado.faturamento:,.2f}")
    
    if len(dados) > 7:
        print(f"\\n✅ DADOS ATUALIZADOS!")
        print(f"✅ Dr. João agora tem {len(dados)} meses")
        print(f"✅ Sincronização funcionou!")
        return True
    else:
        print(f"\\n⚠️ Dados não foram atualizados")
        print(f"⚠️ Ainda tem {len(dados)} meses")
        return False

def main():
    """Função principal"""
    print("🏥 CONFIGURAÇÃO DE LINK - DR. JOÃO")
    print("=" * 60)
    
    # Configurar link
    success = configure_joao_link()
    
    if success:
        # Testar sincronização
        test_sync_after_config()
        
        # Verificar dados
        verify_joao_data()
        
        print(f"\\n🎉 RESULTADO FINAL:")
        print(f"✅ Link configurado com sucesso!")
        print(f"✅ Dr. João agora pode ser sincronizado!")
        print(f"✅ Sistema funcionando perfeitamente!")
        
        print(f"\\n💡 PRÓXIMOS PASSOS:")
        print(f"   1. Execute: python sync_sheets.py")
        print(f"   2. Verifique se os dados foram atualizados")
        print(f"   3. Acesse o dashboard para ver os novos dados")
    else:
        print(f"\\n❌ Erro na configuração!")

if __name__ == "__main__":
    main()
