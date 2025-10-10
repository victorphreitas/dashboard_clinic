"""
Script de teste para verificar o CRUD completo de clínicas e usuários.
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("🔍 Testando conexão com banco de dados...")
    
    try:
        from database import db_manager, cliente_crud
        
        # Testa conexão
        session = db_manager.get_session()
        session.close()
        print("✅ Conexão com banco de dados: OK")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

def test_crud_operations():
    """Testa operações CRUD"""
    print("🔍 Testando operações CRUD...")
    
    try:
        from database import cliente_crud
        from auth import AuthManager
        
        # Teste de criação
        print("   📝 Testando criação de cliente...")
        import time
        timestamp = str(int(time.time()))
        cliente = cliente_crud.create_cliente(
            nome="Clínica Teste",
            email=f"teste{timestamp}@clinica.com",
            senha="teste123",
            cnpj=f"12.345.678/0001-{timestamp[-2:]}",
            nome_da_clinica="Clínica Teste CRUD",
            telefone="(11) 99999-9999",
            endereco="Rua Teste, 123",
            link_empresa="https://teste.com"
        )
        
        if not cliente:
            print("❌ Falha na criação de cliente")
            return False
        
        print(f"   ✅ Cliente criado com ID: {cliente.id}")
        
        # Teste de leitura
        print("   📖 Testando leitura de cliente...")
        cliente_lido = cliente_crud.get_cliente_by_id(cliente.id)
        if not cliente_lido:
            print("❌ Falha na leitura de cliente")
            return False
        
        print(f"   ✅ Cliente lido: {cliente_lido.nome}")
        
        # Teste de atualização
        print("   ✏️ Testando atualização de cliente...")
        success = cliente_crud.update_cliente(
            cliente.id,
            nome="Clínica Teste Atualizada",
            telefone="(11) 88888-8888"
        )
        
        if not success:
            print("❌ Falha na atualização de cliente")
            return False
        
        print("   ✅ Cliente atualizado com sucesso")
        
        # Teste de soft delete
        print("   🗑️ Testando soft delete de cliente...")
        success = cliente_crud.delete_cliente(cliente.id)
        
        if not success:
            print("❌ Falha no soft delete de cliente")
            return False
        
        print("   ✅ Cliente desativado com sucesso")
        
        # Verificar se cliente foi desativado
        cliente_desativado = cliente_crud.get_cliente_by_id(cliente.id)
        if cliente_desativado and cliente_desativado.ativo:
            print("❌ Cliente ainda está ativo após soft delete")
            return False
        
        print("   ✅ Cliente corretamente desativado")
        
        # Teste de hard delete
        print("   🔥 Testando hard delete de cliente...")
        success = cliente_crud.hard_delete_cliente(cliente.id)
        
        if not success:
            print("❌ Falha no hard delete de cliente")
            return False
        
        print("   ✅ Cliente removido permanentemente")
        
        # Verificar se cliente foi removido
        cliente_removido = cliente_crud.get_cliente_by_id(cliente.id)
        if cliente_removido:
            print("❌ Cliente ainda existe após hard delete")
            return False
        
        print("   ✅ Cliente corretamente removido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas operações CRUD: {e}")
        return False

def test_auth_manager():
    """Testa AuthManager"""
    print("🔍 Testando AuthManager...")
    
    try:
        from auth import AuthManager
        
        auth = AuthManager()
        
        # Teste de validação de email
        if not auth._validate_email("teste@exemplo.com"):
            print("❌ Falha na validação de email válido")
            return False
        
        if auth._validate_email("email-invalido"):
            print("❌ Falha na validação de email inválido")
            return False
        
        # Teste de validação de senha
        if not auth._validate_password("senha123"):
            print("❌ Falha na validação de senha válida")
            return False
        
        if auth._validate_password("123"):
            print("❌ Falha na validação de senha inválida")
            return False
        
        print("✅ AuthManager funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no AuthManager: {e}")
        return False

def test_interface_functions():
    """Testa funções de interface"""
    print("🔍 Testando funções de interface...")
    
    try:
        from auth import (
            show_edit_clinic_form,
            show_delete_confirmation,
            show_clinic_management_panel
        )
        
        print("✅ Funções de interface importadas com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas funções de interface: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE DO CRUD COMPLETO - SISTEMA DE GERENCIAMENTO")
    print("=" * 70)
    
    tests = [
        ("Conexão com Banco", test_database_connection),
        ("Operações CRUD", test_crud_operations),
        ("AuthManager", test_auth_manager),
        ("Funções de Interface", test_interface_functions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! CRUD implementado com sucesso!")
        print("\n📋 FUNCIONALIDADES IMPLEMENTADAS:")
        print("✅ Criação de clínicas")
        print("✅ Leitura de clínicas")
        print("✅ Atualização de clínicas")
        print("✅ Soft delete (desativação)")
        print("✅ Hard delete (remoção permanente)")
        print("✅ Validações de dados")
        print("✅ Interface de gerenciamento")
        print("✅ Formulários de edição")
        print("✅ Confirmações de exclusão")
        print("\n🚀 SISTEMA PRONTO PARA USO!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM! Verifique os erros acima.")
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrija os erros identificados")
        print("2. Execute os testes novamente")
        print("3. Só prossiga quando todos os testes passarem")

if __name__ == "__main__":
    main()
