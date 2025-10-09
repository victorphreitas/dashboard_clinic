#!/usr/bin/env python3
"""
Script para testar credenciais em produção
Execute este script no Render.com para diagnosticar problemas
"""

import os
import json
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_production_credentials():
    """Testa credenciais em produção"""
    print("🔍 TESTE DE CREDENCIAIS EM PRODUÇÃO")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar variáveis
    secret_key = os.getenv('SECRET_KEY', 'NÃO ENCONTRADA')
    database_url = os.getenv('DATABASE_URL', 'NÃO ENCONTRADA')
    google_creds = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'NÃO ENCONTRADA')
    debug = os.getenv('DEBUG', 'NÃO ENCONTRADA')
    
    print(f"📋 SECRET_KEY: {secret_key[:20]}..." if len(secret_key) > 20 else f"📋 SECRET_KEY: {secret_key}")
    print(f"📋 DATABASE_URL: {database_url}")
    print(f"📋 GOOGLE_SHEETS_CREDENTIALS: {len(google_creds)} caracteres")
    print(f"📋 DEBUG: {debug}")
    
    # Testar parse das credenciais
    try:
        credentials_json = json.loads(google_creds)
        print(f"✅ JSON válido!")
        print(f"📧 Email: {credentials_json.get('client_email', 'NÃO ENCONTRADO')}")
        print(f"🏗️ Project: {credentials_json.get('project_id', 'NÃO ENCONTRADO')}")
    except Exception as e:
        print(f"❌ Erro no JSON: {e}")
        return False
    
    # Testar autenticação
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
        gc = gspread.authorize(credentials)
        print("✅ Autenticação com Google Sheets funcionando!")
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return False
    
    # Testar acesso às planilhas
    planilhas_teste = [
        {'nome': 'Dr. João Silva', 'id': '1hJDvihxFPWnqjGlp-QFOB6vjExlskBHPNbA3j7SxgPA'},
        {'nome': 'Dra Taynah Bastos', 'id': '1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs'}
    ]
    
    print("\n🔍 TESTANDO ACESSO ÀS PLANILHAS:")
    for planilha in planilhas_teste:
        try:
            sheet = gc.open_by_key(planilha['id'])
            print(f"✅ {planilha['nome']}: Acessível")
            print(f"   📋 Título: {sheet.title}")
            
            # Testar aba Controle de Leads
            try:
                controle_ws = sheet.worksheet('Controle de Leads')
                data = controle_ws.get_all_values()
                print(f"   📊 Aba Controle de Leads: {len(data)} linhas")
                
                if len(data) > 1:
                    print(f"   📋 Primeira linha: {data[0][:5]}...")
                else:
                    print("   ⚠️ Aba vazia")
                    
            except Exception as e:
                print(f"   ❌ Erro na aba Controle de Leads: {e}")
                
        except Exception as e:
            print(f"❌ {planilha['nome']}: ERRO - {e}")
    
    print("\n🎯 TESTE CONCLUÍDO!")
    return True

if __name__ == "__main__":
    test_production_credentials()
