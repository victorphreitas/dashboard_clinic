"""
Script para resolver o problema de acesso à planilha do Dr. Jonnattan
"""

import gspread
from google.oauth2.service_account import Credentials
from database import cliente_crud, dados_crud, db_manager
import re

def extract_sheet_id_from_url(url):
    """Extrai o ID da planilha de uma URL do Google Sheets"""
    if not url:
        return None
    
    patterns = [
        r'/spreadsheets/d/([a-zA-Z0-9-_]+)',
        r'id=([a-zA-Z0-9-_]+)',
        r'/([a-zA-Z0-9-_]{44})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def test_different_access_methods():
    """Testa diferentes métodos de acesso à planilha"""
    print("🔍 TESTANDO DIFERENTES MÉTODOS DE ACESSO")
    print("=" * 50)
    
    # Configurar credenciais
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file('google_credentials.json', scopes=SCOPES)
    gc = gspread.authorize(creds)
    
    # URL da planilha
    url = "https://docs.google.com/spreadsheets/d/1ZhqhpA1agIKo2w92X8h0NqLSJy1QJKt2/edit?gid=1445686101#gid=1445686101"
    sheet_id = extract_sheet_id_from_url(url)
    
    print(f"📊 URL: {url}")
    print(f"📊 ID extraído: {sheet_id}")
    
    # Método 1: Acesso direto por ID
    print(f"\\n🧪 Método 1: Acesso direto por ID")
    try:
        spreadsheet = gc.open_by_key(sheet_id)
        print(f"✅ Sucesso: {spreadsheet.title}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Método 2: Acesso por URL
    print(f"\\n🧪 Método 2: Acesso por URL")
    try:
        spreadsheet = gc.open_by_url(url)
        print(f"✅ Sucesso: {spreadsheet.title}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Método 3: URL sem gid
    print(f"\\n🧪 Método 3: URL sem gid")
    try:
        clean_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        spreadsheet = gc.open_by_url(clean_url)
        print(f"✅ Sucesso: {spreadsheet.title}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return False

def check_sharing_status():
    """Verifica o status de compartilhamento"""
    print(f"\\n🔍 VERIFICANDO STATUS DE COMPARTILHAMENTO")
    print("=" * 50)
    
    print(f"📧 Email do service account:")
    print(f"   dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com")
    
    print(f"\\n📋 PASSOS PARA RESOLVER:")
    print(f"   1. Acesse a planilha: https://docs.google.com/spreadsheets/d/1ZhqhpA1agIKo2w92X8h0NqLSJy1QJKt2/edit")
    print(f"   2. Clique em 'Compartilhar' (canto superior direito)")
    print(f"   3. Adicione o email: dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com")
    print(f"   4. Defina permissão como 'Editor'")
    print(f"   5. Clique em 'Enviar'")
    print(f"   6. Aguarde 2-3 minutos para propagação")
    
    print(f"\\n🧪 APÓS COMPARTILHAR, EXECUTE:")
    print(f"   python test_jonnattan.py")

def create_manual_import():
    """Cria importação manual dos dados"""
    print(f"\\n📊 DADOS IDENTIFICADOS NA PLANILHA:")
    print("=" * 50)
    
    print(f"📅 Outubro:")
    print(f"   - Consultas Marcadas: 1")
    print(f"   - Faturamento: R$ 500,00")
    print(f"   - Valor Gasto: R$ 284,31")
    
    print(f"\\n💡 SOLUÇÃO ALTERNATIVA:")
    print(f"   Se o compartilhamento não funcionar, posso criar")
    print(f"   um script para importar os dados manualmente")

def main():
    """Função principal"""
    print("🏥 CORREÇÃO DE ACESSO - DR. JONNATTAN")
    print("=" * 60)
    
    # Testar diferentes métodos
    success = test_different_access_methods()
    
    if success:
        print(f"\\n🎉 SUCESSO! Planilha acessível!")
        print(f"   Execute: python check_empty_clinics.py")
    else:
        print(f"\\n❌ Ainda não acessível")
        check_sharing_status()
        create_manual_import()

if __name__ == "__main__":
    main()
