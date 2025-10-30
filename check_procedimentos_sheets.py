"""
Script para verificar se uma planilha tem aba "Procedimentos" e importar apenas se existir.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', '{}')

def setup_google_sheets_auth():
    """Configura autenticação com Google Sheets"""
    try:
        if GOOGLE_SHEETS_CREDENTIALS and GOOGLE_SHEETS_CREDENTIALS != '{}':
            try:
                credentials_json = json.loads(GOOGLE_SHEETS_CREDENTIALS)
                scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
                gc = gspread.authorize(credentials)
                print("✅ Autenticação com Google Sheets configurada!")
                return gc
            except Exception as e:
                print(f"❌ Erro ao usar credenciais das variáveis de ambiente: {e}")
                return None
        else:
            print("❌ GOOGLE_SHEETS_CREDENTIALS não configurado")
            return None
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return None

def check_procedimentos_sheet_exists(sheet_id, sheet_name="Procedimentos"):
    """Verifica se a aba 'Procedimentos' existe na planilha"""
    gc = setup_google_sheets_auth()
    if not gc:
        return False
    
    try:
        # Abre a planilha
        spreadsheet = gc.open_by_key(sheet_id)
        
        # Lista todas as abas
        worksheets = spreadsheet.worksheets()
        worksheet_names = [ws.title for ws in worksheets]
        
        print(f"📋 Abas encontradas: {worksheet_names}")
        
        # Verifica se a aba "Procedimentos" existe
        if sheet_name in worksheet_names:
            print(f"✅ Aba '{sheet_name}' encontrada!")
            return True
        else:
            print(f"❌ Aba '{sheet_name}' não encontrada!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar planilha: {e}")
        return False

def main():
    """Função principal para verificar planilhas"""
    print("🔍 Verificando abas de procedimentos nas planilhas...")
    
    # IDs das planilhas das clínicas
    planilhas = {
        "Prestige Clinic": "1hJDvihxFPWnqjGlp-QFOB6vjExlskBHPNbA3j7SxgPA",
        "Dra Marlei Sangalli": "1hJDvihxFPWnqjGlp-QFOB6vjExlskBHPNbA3j7SxgPA"  # Mesmo ID por enquanto
    }
    
    for nome, sheet_id in planilhas.items():
        print(f"\n📊 Verificando {nome}...")
        exists = check_procedimentos_sheet_exists(sheet_id)
        if exists:
            print(f"✅ {nome} tem aba 'Procedimentos'")
        else:
            print(f"❌ {nome} NÃO tem aba 'Procedimentos'")

if __name__ == "__main__":
    main()
