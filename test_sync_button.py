"""
Teste específico para o botão de sincronização
"""

import subprocess
import sys
import os

def test_sync_button():
    """Testa a funcionalidade do botão de sincronização"""
    print("🧪 Testando botão de sincronização...")
    
    try:
        # Simula exatamente o que o botão faz
        current_dir = os.getcwd()
        print(f"📁 Diretório atual: {current_dir}")
        
        # Verifica se o arquivo existe
        sync_file = "sync_sheets.py"
        if os.path.exists(sync_file):
            print(f"✅ Arquivo {sync_file} encontrado")
        else:
            print(f"❌ Arquivo {sync_file} não encontrado")
            return False
        
        # Executa o script
        print("🔄 Executando sync_sheets.py...")
        result = subprocess.run([sys.executable, sync_file], 
                              capture_output=True, text=True, cwd=".", timeout=60)
        
        print(f"📊 Código de saída: {result.returncode}")
        print(f"📤 Saída:")
        print(result.stdout)
        
        if result.stderr:
            print(f"❌ Erro:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Sincronização executada com sucesso!")
            return True
        else:
            print(f"❌ Erro na sincronização (código {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout: A sincronização demorou muito para responder")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar sincronização: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_sync_button()
    if success:
        print("\n🎉 Teste do botão passou!")
    else:
        print("\n❌ Teste do botão falhou!")


