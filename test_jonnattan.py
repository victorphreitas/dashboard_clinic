"""
Script específico para testar acesso à planilha do Dr. Jonnattan
"""

import gspread
from google.oauth2.service_account import Credentials

def test_jonnattan_access():
    """Testa acesso específico à planilha do Dr. Jonnattan"""
    print("🧪 TESTE ESPECÍFICO - DR. JONNATTAN")
    print("=" * 50)
    
    # Configurar credenciais
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file('google_credentials.json', scopes=SCOPES)
    gc = gspread.authorize(creds)
    
    # ID da planilha do Dr. Jonnattan
    sheet_id = '1ZhqhpA1agIKo2w92X8h0NqLSJy1QJKt2'
    
    print(f"📊 Testando acesso à planilha ID: {sheet_id}")
    print(f"🔗 Link: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
    
    try:
        # Tentar abrir a planilha
        spreadsheet = gc.open_by_key(sheet_id)
        print(f"✅ SUCESSO! Planilha aberta: {spreadsheet.title}")
        
        # Listar abas
        worksheets = spreadsheet.worksheets()
        print(f"📋 Abas encontradas: {[ws.title for ws in worksheets]}")
        
        # Testar primeira aba
        if worksheets:
            first_sheet = worksheets[0]
            print(f"\\n📊 Testando aba: {first_sheet.title}")
            
            # Pegar dados
            data = first_sheet.get_all_records()
            print(f"📈 Dados encontrados: {len(data)} registros")
            
            if data:
                print(f"\\n📋 Primeiras 3 linhas:")
                for i, row in enumerate(data[:3]):
                    print(f"   Linha {i+1}: {row}")
                
                # Verificar se há dados de Janeiro
                janeiro_found = False
                for row in data:
                    if 'Janeiro' in str(row.values()):
                        janeiro_found = True
                        print(f"\\n📅 Dados de Janeiro encontrados!")
                        break
                
                if not janeiro_found:
                    print(f"\\n⚠️ Nenhum dado de Janeiro encontrado")
            else:
                print(f"⚠️ Nenhum dado encontrado na aba")
        
        print(f"\\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print(f"✅ A planilha está acessível")
        print(f"✅ Dados podem ser importados")
        print(f"\\n💡 Próximo passo: Execute 'python check_empty_clinics.py'")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print(f"\\n💡 SOLUÇÕES:")
        print(f"   1. Verificar se a planilha foi compartilhada com:")
        print(f"      dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com")
        print(f"   2. Verificar se a permissão é 'Editor'")
        print(f"   3. Aguardar alguns minutos para propagação")
        print(f"   4. Verificar se a planilha não está em modo privado")
        print(f"   5. Tentar compartilhar novamente")
        
        return False

if __name__ == "__main__":
    success = test_jonnattan_access()
    
    if success:
        print(f"\\n🚀 Execute agora: python check_empty_clinics.py")
    else:
        print(f"\\n🔧 Resolva o problema de compartilhamento primeiro")

