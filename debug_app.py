#!/usr/bin/env python3
"""
Código de debug para adicionar temporariamente no app.py
"""

import streamlit as st
import os
import json
from dotenv import load_dotenv

def debug_render_environment():
    """Debug das variáveis de ambiente no Render.com"""
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    st.write("🔍 **DEBUG - RENDER.COM**")
    st.write("=" * 50)
    
    # Verificar variáveis
    secret_key = os.getenv('SECRET_KEY', 'NÃO ENCONTRADA')
    database_url = os.getenv('DATABASE_URL', 'NÃO ENCONTRADA')
    google_creds = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'NÃO ENCONTRADA')
    debug = os.getenv('DEBUG', 'NÃO ENCONTRADA')
    
    st.write(f"📋 **SECRET_KEY**: {secret_key[:20]}..." if len(secret_key) > 20 else f"📋 **SECRET_KEY**: {secret_key}")
    st.write(f"📋 **DATABASE_URL**: {database_url}")
    st.write(f"📋 **GOOGLE_SHEETS_CREDENTIALS**: {len(google_creds)} caracteres")
    st.write(f"📋 **DEBUG**: {debug}")
    
    # Testar parse das credenciais
    try:
        credentials_json = json.loads(google_creds)
        st.write("✅ **JSON das credenciais válido!**")
        st.write(f"📧 **Email**: {credentials_json.get('client_email', 'NÃO ENCONTRADO')}")
        st.write(f"🏗️ **Project**: {credentials_json.get('project_id', 'NÃO ENCONTRADO')}")
        
        # Testar autenticação
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
            gc = gspread.authorize(credentials)
            st.write("✅ **Autenticação com Google Sheets funcionando!**")
            
            # Testar acesso à planilha do Dr. João
            try:
                sheet = gc.open_by_key('1hJDvihxFPWnqjGlp-QFOB6vjExlskBHPNbA3j7SxgPA')
                st.write(f"✅ **Planilha acessível**: {sheet.title}")
                
                # Testar aba Controle de Leads
                try:
                    controle_ws = sheet.worksheet('Controle de Leads')
                    data = controle_ws.get_all_values()
                    st.write(f"📊 **Aba Controle de Leads**: {len(data)} linhas")
                    
                    if len(data) > 1:
                        st.write("📋 **Primeira linha**:", data[0][:5])
                    else:
                        st.write("⚠️ **Aba vazia**")
                        
                except Exception as e:
                    st.write(f"❌ **Erro na aba Controle de Leads**: {e}")
                    
            except Exception as e:
                st.write(f"❌ **Erro ao acessar planilha**: {e}")
                
        except Exception as e:
            st.write(f"❌ **Erro na autenticação**: {e}")
            
    except Exception as e:
        st.write(f"❌ **Erro no JSON**: {e}")
    
    st.write("🎯 **Debug concluído!**")

# Para usar, adicione este código no app.py:
# if st.button("🔍 Debug Render.com"):
#     debug_render_environment()
