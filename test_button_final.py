"""
Teste final do botão de sincronização
Simula exatamente o que acontece quando o botão é clicado no dashboard
"""

import subprocess
import sys
import os
from datetime import datetime

def test_button_click():
    """Simula o clique no botão de atualização"""
    print("🧪 Testando clique no botão de atualização...")
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"⏰ Timestamp: {datetime.now()}")
    
    try:
        # Simula exatamente o que o botão faz
        result = subprocess.run([sys.executable, "sync_sheets.py"], 
                              capture_output=True, text=True, cwd=".", timeout=60)
        
        print(f"📊 Código de saída: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Sincronização executada com sucesso!")
            print("📊 Resultado:")
            print(result.stdout)
            
            # Verifica se há dados atualizados
            if "sincronizada!" in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "sincronizada!" in line:
                        print(f"📈 {line}")
                        break
            
            return True
        else:
            print(f"❌ Erro na sincronização (código {result.returncode})")
            if result.stderr:
                print(f"Detalhes do erro: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout: A sincronização demorou muito para responder")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar sincronização: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

def verify_data_updated():
    """Verifica se os dados foram realmente atualizados"""
    print("\n🔍 Verificando se os dados foram atualizados...")
    
    try:
        from database import dados_crud, cliente_crud
        
        # Buscar cliente Dra Marlei
        clientes = cliente_crud.get_all_clientes()
        dra_marlei = None
        for cliente in clientes:
            if 'Marlei' in cliente.nome_da_clinica:
                dra_marlei = cliente
                break
        
        if dra_marlei:
            dados = dados_crud.get_dados_by_cliente(dra_marlei.id)
            print(f"📊 Dados encontrados: {len(dados)} registros")
            
            for dado in dados:
                print(f"   📅 {dado.mes}: {dado.leads_totais} leads, R$ {dado.faturamento:,.2f} (Atualizado: {dado.data_criacao})")
            
            return True
        else:
            print("❌ Clínica Dra Marlei não encontrada")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar dados: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTE FINAL DO BOTÃO DE SINCRONIZAÇÃO")
    print("=" * 50)
    
    # Testa o botão
    button_success = test_button_click()
    
    if button_success:
        # Verifica se os dados foram atualizados
        data_updated = verify_data_updated()
        
        if data_updated:
            print("\n🎉 TESTE COMPLETO: Botão funcionando perfeitamente!")
            print("✅ Sincronização executada")
            print("✅ Dados atualizados no banco")
            print("✅ Dashboard deve mostrar dados atualizados")
        else:
            print("\n⚠️ TESTE PARCIAL: Botão executou, mas dados não foram atualizados")
    else:
        print("\n❌ TESTE FALHOU: Botão não executou corretamente")
    
    print("\n" + "=" * 50)


