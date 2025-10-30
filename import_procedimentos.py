"""
Script para importar dados de procedimentos da aba "Procedimentos" do Google Sheets.
Processa dados estruturados com informações detalhadas de cada procedimento.
"""

import gspread
import pandas as pd
from database import db_manager, cliente_crud, procedimento_crud
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import re

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

def parse_date(date_str):
    """Converte string de data para datetime"""
    if not date_str or pd.isna(date_str) or str(date_str).strip() == '':
        return None
    
    try:
        # Tenta diferentes formatos de data
        date_formats = [
            '%d/%m/%Y',
            '%d/%m/%y',
            '%Y-%m-%d',
            '%d-%m-%Y'
        ]
        
        date_str = str(date_str).strip()
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # Se nenhum formato funcionou, tenta parsing automático do pandas
        return pd.to_datetime(date_str, dayfirst=True)
    except:
        return None

def parse_currency(value_str):
    """Converte string de moeda para float"""
    if not value_str or pd.isna(value_str) or str(value_str).strip() == '':
        return 0.0
    
    try:
        # Remove caracteres não numéricos exceto vírgula e ponto
        value_str = str(value_str).strip()
        value_str = re.sub(r'[^\d,.-]', '', value_str)
        
        # Substitui vírgula por ponto se for separador decimal
        if ',' in value_str and '.' in value_str:
            # Formato brasileiro: 1.000,00
            value_str = value_str.replace('.', '').replace(',', '.')
        elif ',' in value_str and value_str.count(',') == 1:
            # Pode ser separador decimal
            parts = value_str.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                value_str = value_str.replace(',', '.')
            else:
                value_str = value_str.replace(',', '')
        
        return float(value_str)
    except:
        return 0.0

def import_procedimentos_from_sheets(sheet_id, sheet_name="Procedimentos"):
    """Importa dados de procedimentos do Google Sheets"""
    gc = setup_google_sheets_auth()
    if not gc:
        return None
    
    try:
        # Abre a planilha
        spreadsheet = gc.open_by_key(sheet_id)
        
        # Tenta encontrar a aba "Procedimentos"
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            print(f"❌ Aba '{sheet_name}' não encontrada na planilha")
            return None
        
        # Obtém todos os dados da aba
        all_values = worksheet.get_all_values()
        
        if not all_values or len(all_values) < 2:
            print(f"❌ Nenhum dado encontrado na aba '{sheet_name}'")
            return None
        
        # A estrutura da planilha é:
        # Linha 1: Mês de referência (ex: "Outubro")
        # Linha 2: Cabeçalhos reais
        # Linhas 3+: Dados dos procedimentos
        
        if len(all_values) < 3:
            print(f"❌ Planilha tem menos de 3 linhas. Estrutura esperada: linha 1 (mês), linha 2 (cabeçalhos), linha 3+ (dados)")
            return None
        
        # Extrai o mês de referência da primeira linha
        mes_referencia = all_values[0][0].strip() if all_values[0] and all_values[0][0].strip() else "Outubro"
        print(f"📅 Mês de referência: {mes_referencia}")
        
        # Segunda linha são os cabeçalhos reais
        headers = all_values[1]
        data_rows = all_values[2:]
        
        print(f"📊 Encontrados {len(data_rows)} registros de procedimentos")
        print(f"📋 Cabeçalhos: {headers}")
        
        # Converte para DataFrame
        df = pd.DataFrame(data_rows, columns=headers)
        
        # Remove linhas vazias
        df = df.dropna(how='all')
        
        if df.empty:
            print("❌ Nenhum dado válido encontrado")
            return None
        
        # Processa os dados
        processed_data = []
        
        print(f"📊 Processando {len(df)} linhas de dados...")
        
        for index, row in df.iterrows():
            try:
                print(f"📅 Processando linha {index + 1}/{len(df)}...")
                
                # Processa cada linha de dados usando o mês já extraído
                procedimento_data = {
                    'mes_referencia': mes_referencia,
                    'ano_referencia': 2024,  # Padrão
                    'data_primeiro_contato': parse_date(row.get('Data 1° Contato', '')),
                    'data_compareceu_consulta': parse_date(row.get('Data Compareu na Consulta', '')),
                    'data_fechou_cirurgia': parse_date(row.get('Data Fechou Cirurgia', '')),
                    'procedimento': str(row.get('Procedimento', '')).strip(),
                    'tipo': str(row.get('Tipo', '')).strip(),
                    'quantidade_na_mesma_venda': int(row.get('Quantidade na Mesma Venda', 1)) if str(row.get('Quantidade na Mesma Venda', 1)).isdigit() else 1,
                    'forma_pagamento': str(row.get('Forma de Pagamento', '')).strip(),
                    'valor_da_venda': parse_currency(row.get('Valor da Venda', '')),
                    'valor_parcelado': parse_currency(row.get('Valor do Parcelado', ''))
                }
                
                # Só adiciona se tiver pelo menos o procedimento
                if procedimento_data['procedimento'] and procedimento_data['procedimento'] != 'nan' and procedimento_data['procedimento'] != '':
                    processed_data.append(procedimento_data)
                    print(f"✅ Linha {index + 1}: Procedimento '{procedimento_data['procedimento']}' adicionado")
                else:
                    print(f"⚠️ Linha {index + 1}: Ignorada - sem procedimento válido")
                    
            except Exception as e:
                print(f"⚠️ Erro ao processar linha {index + 1}: {e}")
                print(f"   Dados da linha: {dict(row)}")
                continue
        
        if not processed_data:
            print("❌ Nenhum procedimento válido processado")
            return None
        
        print(f"✅ Processados {len(processed_data)} procedimentos válidos")
        return pd.DataFrame(processed_data)
        
    except Exception as e:
        print(f"❌ Erro ao importar procedimentos: {e}")
        return None

def check_procedimentos_sheet_exists(sheet_id):
    """Verifica se a planilha tem aba 'Procedimentos'"""
    gc = setup_google_sheets_auth()
    if not gc:
        return False
    
    try:
        spreadsheet = gc.open_by_key(sheet_id)
        worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
        return "Procedimentos" in worksheet_names
    except Exception as e:
        print(f"❌ Erro ao verificar abas da planilha: {e}")
        return False

def load_procedimentos_for_cliente(cliente):
    """Carrega procedimentos para uma clínica específica"""
    print(f"🔄 Processando clínica: {cliente.nome_da_clinica} (ID: {cliente.id})")
    
    if not hasattr(cliente, 'link_empresa') or not cliente.link_empresa:
        print(f"⚠️ Clínica {cliente.nome_da_clinica} não tem link_empresa")
        return False
    
    # Extrai ID da planilha
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
    
    # Verifica se a planilha tem aba "Procedimentos"
    print(f"🔍 Verificando se {cliente.nome_da_clinica} tem aba 'Procedimentos'...")
    if not check_procedimentos_sheet_exists(sheet_id):
        print(f"⚠️ Clínica {cliente.nome_da_clinica} não tem aba 'Procedimentos' - pulando importação")
        return False
    
    print(f"✅ Aba 'Procedimentos' encontrada! Importando dados para {cliente.nome_da_clinica}...")
    
    # Importa dados de procedimentos
    df = import_procedimentos_from_sheets(sheet_id)
    if df is None or df.empty:
        print(f"❌ Nenhum procedimento encontrado para {cliente.nome_da_clinica}")
        return False
    
    # Remove procedimentos existentes da clínica
    print(f"🗑️ Removendo procedimentos existentes de {cliente.nome_da_clinica} (ID: {cliente.id})...")
    procedimento_crud.delete_procedimentos_by_cliente(cliente.id)
    
    # Insere novos procedimentos
    success_count = 0
    for _, row in df.iterrows():
        try:
            procedimento = procedimento_crud.create_procedimento(
                cliente_id=cliente.id,
                procedimento=row['procedimento'],
                mes_referencia=row['mes_referencia'],
                ano_referencia=row['ano_referencia'],
                data_primeiro_contato=row['data_primeiro_contato'],
                data_compareceu_consulta=row['data_compareceu_consulta'],
                data_fechou_cirurgia=row['data_fechou_cirurgia'],
                tipo=row['tipo'],
                quantidade_na_mesma_venda=row['quantidade_na_mesma_venda'],
                forma_pagamento=row['forma_pagamento'],
                valor_da_venda=row['valor_da_venda'],
                valor_parcelado=row['valor_parcelado']
            )
            
            if procedimento:
                success_count += 1
                
        except Exception as e:
            print(f"⚠️ Erro ao inserir procedimento: {e}")
            continue
    
    print(f"✅ Importados {success_count} procedimentos para {cliente.nome_da_clinica} (ID: {cliente.id})")
    return success_count > 0

def main():
    """Função principal para importar procedimentos de todas as clínicas"""
    print("🚀 Iniciando importação de procedimentos...")
    
    # Busca todas as clínicas ativas (exceto admin)
    clientes = cliente_crud.get_all_clientes()
    clinicas_ativas = [c for c in clientes if not c.is_admin and c.ativo]
    
    if not clinicas_ativas:
        print("❌ Nenhuma clínica ativa encontrada")
        return
    
    print(f"📊 Encontradas {len(clinicas_ativas)} clínicas ativas")
    
    success_count = 0
    for cliente in clinicas_ativas:
        try:
            if load_procedimentos_for_cliente(cliente):
                success_count += 1
        except Exception as e:
            print(f"❌ Erro ao processar {cliente.nome_da_clinica}: {e}")
            continue
    
    print(f"🎉 Importação concluída! {success_count}/{len(clinicas_ativas)} clínicas processadas com sucesso")

if __name__ == "__main__":
    main()
