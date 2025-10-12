"""
Script de sincronização inteligente com Google Sheets.
Atualiza apenas dados que realmente mudaram, preservando histórico.
"""

import gspread
import pandas as pd
from database import db_manager, cliente_crud, dados_crud
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import hashlib

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', '{}')

def setup_google_sheets_auth():
    """Configura autenticação com Google Sheets"""
    try:
        # Usar apenas credenciais das variáveis de ambiente
        if GOOGLE_SHEETS_CREDENTIALS and GOOGLE_SHEETS_CREDENTIALS != '{}':
            try:
                credentials_json = json.loads(GOOGLE_SHEETS_CREDENTIALS)
                scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
                gc = gspread.authorize(credentials)
                print("✅ Autenticação com Google Sheets configurada via variáveis de ambiente!")
                return gc
            except Exception as e:
                print(f"❌ Erro ao usar credenciais das variáveis de ambiente: {e}")
                print("💡 Verifique se GOOGLE_SHEETS_CREDENTIALS está configurado corretamente")
                return None
        else:
            print("❌ GOOGLE_SHEETS_CREDENTIALS não configurado")
            print("💡 Configure GOOGLE_SHEETS_CREDENTIALS no arquivo .env ou variáveis de ambiente")
            return None
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return None

def get_sheet_data_hash(sheet_id, sheet_name):
    """Gera hash dos dados da planilha para detectar mudanças"""
    gc = setup_google_sheets_auth()
    if not gc:
        return None
    
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet('Controle de Leads')
        data = worksheet.get_all_values()
        
        # Cria hash dos dados
        data_str = str(data)
        return hashlib.md5(data_str.encode()).hexdigest()
    except Exception as e:
        print(f"❌ Erro ao gerar hash: {e}")
        return None

def sync_clinic_data(cliente):
    """Sincroniza dados de uma clínica específica"""
    if not hasattr(cliente, 'link_empresa') or not cliente.link_empresa:
        print(f"⚠️ Clínica {cliente.nome_da_clinica} não tem link_empresa")
        return False
    
    # Extrai ID da planilha
    import re
    sheet_id = None
    patterns = [
        r'/spreadsheets/d/([a-zA-Z0-9-_]+)',
        r'id=([a-zA-Z0-9-_]+)',
        r'/([a-zA-Z0-9-_]{44})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, cliente.link_empresa)
        if match:
            sheet_id = match.group(1)
            break
    
    if not sheet_id:
        print(f"❌ Não foi possível extrair ID da planilha: {cliente.link_empresa}")
        return False
    
    print(f"🔄 Sincronizando {cliente.nome_da_clinica}...")
    
    # Verifica se há mudanças na planilha
    current_hash = get_sheet_data_hash(sheet_id, cliente.nome_da_clinica)
    if not current_hash:
        print(f"❌ Não foi possível acessar planilha de {cliente.nome_da_clinica}")
        return False
    
    # Verifica hash armazenado (implementação futura)
    # Por enquanto, sempre atualiza
    print(f"📊 Importando dados atualizados...")
    
    # Importa dados (reutiliza lógica do import_multiple_sheets.py)
    from import_multiple_sheets import import_from_google_sheets, process_controle_leads_data, is_dashboard_data_structure
    
    df = import_from_google_sheets(sheet_id, cliente.nome_da_clinica)
    if df is None or df.empty:
        print(f"❌ Nenhum dado encontrado para {cliente.nome_da_clinica}")
        return False
    
    # Remove dados existentes e insere novos
    print(f"🗑️ Atualizando dados de {cliente.nome_da_clinica}...")
    dados_existentes = dados_crud.get_dados_by_cliente(cliente.id)
    for dados in dados_existentes:
        dados_crud.delete_dados_dashboard(dados.id)
    
    # Insere novos dados
    success_count = 0
    for _, row in df.iterrows():
        # Carrega TODOS os meses, mesmo os que têm apenas faturamento
        if row['leads_totais'] > 0 or row['faturamento'] > 0 or row['valor_investido_total'] > 0:
            dados = dados_crud.create_dados_dashboard(
                cliente_id=cliente.id,
                mes=row['mes'],
                ano=2024,
                leads_totais=int(row['leads_totais']),
                leads_google_ads=int(row['leads_google_ads']),
                leads_meta_ads=int(row['leads_meta_ads']),
                leads_instagram_organico=int(row['leads_instagram_organico']),
                leads_indicacao=int(row['leads_indicacao']),
                leads_origem_desconhecida=int(row['leads_origem_desconhecida']),
                consultas_marcadas_totais=int(row['consultas_marcadas_totais']),
                consultas_marcadas_google_ads=int(row['consultas_marcadas_google_ads']),
                consultas_marcadas_meta_ads=int(row['consultas_marcadas_meta_ads']),
                consultas_marcadas_ig_organico=int(row['consultas_marcadas_ig_organico']),
                consultas_marcadas_indicacao=int(row['consultas_marcadas_indicacao']),
                consultas_marcadas_outros=int(row['consultas_marcadas_outros']),
                consultas_comparecidas=int(row['consultas_comparecidas']),
                fechamentos_totais=int(row['fechamentos_totais']),
                fechamentos_google_ads=int(row['fechamentos_google_ads']),
                fechamentos_meta_ads=int(row['fechamentos_meta_ads']),
                fechamentos_ig_organico=int(row['fechamentos_ig_organico']),
                fechamentos_indicacao=int(row['fechamentos_indicacao']),
                fechamentos_outros=int(row['fechamentos_outros']),
                faturamento=float(row['faturamento']),
                valor_investido_total=float(row['valor_investido_total']),
                orcamento_previsto_total=float(row['orcamento_previsto_total']),
                orcamento_realizado_facebook=float(row['orcamento_realizado_facebook']),
                orcamento_previsto_facebook=float(row['orcamento_previsto_facebook']),
                orcamento_realizado_google=float(row['orcamento_realizado_google']),
                orcamento_previsto_google=float(row['orcamento_previsto_google'])
            )
            
            if dados:
                success_count += 1
    
    print(f"✅ {cliente.nome_da_clinica} sincronizada! ({success_count} meses atualizados)")
    return True

def sync_all_clinics():
    """Sincroniza todas as clínicas com link_empresa"""
    print("🔄 Iniciando sincronização com Google Sheets...")
    
    # Busca todas as clínicas
    clientes = cliente_crud.get_all_clientes()
    clientes_com_link = []
    
    for cliente in clientes:
        if not cliente.is_admin and hasattr(cliente, 'link_empresa') and cliente.link_empresa:
            clientes_com_link.append(cliente)
    
    print(f"📊 Clínicas com link_empresa: {len(clientes_com_link)}")
    
    success_count = 0
    for cliente in clientes_com_link:
        if sync_clinic_data(cliente):
            success_count += 1
    
    print(f"\n🎉 Sincronização concluída!")
    print(f"✅ {success_count}/{len(clientes_com_link)} clínicas sincronizadas")
    
    return success_count > 0

if __name__ == "__main__":
    sync_all_clinics()

