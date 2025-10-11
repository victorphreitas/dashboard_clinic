"""
Script para importar dados de múltiplas planilhas do Google Sheets.
Configurado para importar dados de ambas as clínicas.
"""

import gspread
import pandas as pd
from database import db_manager, cliente_crud, dados_crud
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', '{}')

# Configuração das planilhas
SHEETS_CONFIG = {
    "joao": {
        "name": "Dr. João Silva",
        "email": "joao@clinicaestetica.com",
        "sheet_id": "1hJDvihxFPWnqjGlp-QFOB6vjExlskBHPNbA3j7SxgPA",  # ID da planilha do João
        "url": "https://docs.google.com/spreadsheets/d/1hJDvihxFPWnqjGlp-QFOB6vjExlskBHPNbA3j7SxgPA/edit?gid=614972599#gid=614972599"
    },
    "taynah": {
        "name": "Dra Taynah Bastos",
        "email": "taynah@cirurgiaplastica.com", 
        "sheet_id": "1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs",  # ID da planilha da Taynah
        "url": "https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk"
    }
}

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

def is_dashboard_data_structure(data):
    """Verifica se uma aba tem a estrutura de dados do dashboard"""
    if not data or len(data) == 0:
        return False
    
    # Verifica se tem pelo menos uma linha com dados de leads
    for row in data:
        # Procura por indicadores de dados do dashboard
        row_values = list(row.values()) if hasattr(row, 'values') else list(row)
        row_str = ' '.join([str(v).lower() for v in row_values if v])
        
        # Indicadores de que é uma aba com dados do dashboard
        dashboard_indicators = [
            'leads totais', 'leads google', 'leads meta', 'faturamento',
            'consultas marcadas', 'fechamentos', 'investimento'
        ]
        
        if any(indicator in row_str for indicator in dashboard_indicators):
            return True
    
    return False

def process_controle_leads_data(data):
    """Processa dados da aba 'Controle de Leads' para formato do dashboard"""
    
    processed_data = []
    
    # Mapeia os dados da planilha para o formato do dashboard
    meses_map = {
        'Janeiro': 'Janeiro',
        'Fevereiro': 'Fevereiro', 
        'Março': 'Março',
        'Abril': 'Abril',
        'Maio': 'Maio',
        'Junho': 'Junho',
        'Julho': 'Julho',
        'Agosto': 'Agosto',
        'Setembro': 'Setembro',
        'Outubro': 'Outubro',
        'Novembro': 'Novembro',
        'Dezembro': 'Dezembro'
    }
    
    # Mapeia as linhas da planilha para os campos do dashboard (novo formato)
    row_mapping = {
        # Leads
        'Leads Totais': 'leads_totais',
        'Leads Google Ads': 'leads_google_ads',
        'Leads Meta Ads': 'leads_meta_ads',
        'Leads Instagram Orgânico': 'leads_instagram_organico',
        'Leads Indicação': 'leads_indicacao',
        'Leads Origem Desconhecida': 'leads_origem_desconhecida',
        
        # Consultas Marcadas
        'Consultas Marcadas Totais': 'consultas_marcadas_totais',
        'Consultas Marcadas Google Ads': 'consultas_marcadas_google_ads',
        'Consultas Marcadas Meta Ads': 'consultas_marcadas_meta_ads',
        'Consultas Marcadas IG Orgânico': 'consultas_marcadas_ig_organico',
        'Consultas Marcadas Indicação': 'consultas_marcadas_indicacao',
        'Consultas Marcadas Outros': 'consultas_marcadas_outros',
        
        # Consultas Comparecidas
        'Consultas Comparecidas': 'consultas_comparecidas',
        
        # Fechamentos
        'Fechamentos Protocolos/Cirurgias': 'fechamentos_totais',
        'Fechamentos Google Ads': 'fechamentos_google_ads',
        'Fechamentos Meta Ads': 'fechamentos_meta_ads',
        'Fechamentos IG Orgânico': 'fechamentos_ig_organico',
        'Fechamentos Indicação': 'fechamentos_indicacao',
        'Fechamentos Outros': 'fechamentos_outros',
        
        # Dados Financeiros
        'Faturamento': 'faturamento',
        'Valor Investido Total (Realizado)': 'valor_investido_total',
        'Orçamento Previsto Total': 'orcamento_previsto_total',
        'Orçamento Realizado Facebook Ads': 'orcamento_realizado_facebook',
        'Orçamento Previsto Facebook Ads': 'orcamento_previsto_facebook',
        'Orçamento Realizado Google Ads': 'orcamento_realizado_google',
        'Orçamento Previsto Google Ads': 'orcamento_previsto_google',
        
        # KPIs de Conversão
        '% de conversão Csm./leads': 'conversao_csm_leads',
        '% de conversão Csc./Csm.': 'conversao_csc_csm',
        '% de conversão fechamento/Csc.': 'conversao_fechamento_csc',
        '% de conversão fechamento/leads': 'conversao_fechamento_leads',
        
        # KPIs Financeiros
        'Custo por Compra (Cirurgias)': 'custo_por_compra_cirurgias',
        'Retorno Sobre Investimento (ROAS)': 'roas',
        'Custo por Lead Total': 'custo_por_lead_total',
        'Custo por Consulta Marcada': 'custo_por_consulta_marcada',
        'Custo por Consulta Comparecida': 'custo_por_consulta_comparecida',
        'Ticket Médio': 'ticket_medio'
    }
    
    # Cria um dicionário para armazenar dados por mês
    meses_data = {}
    
    # Processa cada linha da planilha
    for row in data:
        # Tenta diferentes nomes de coluna para a primeira coluna
        row_name = None
        for col_name in ['Meses', 'm', 'Categoria', 'Tipo']:
            if row.get(col_name) and row.get(col_name) != col_name:
                row_name = row[col_name]
                break
        
        if row_name:
            print(f"   🔍 Processando linha: {row_name}")
            
            # Verifica se é uma linha que mapeamos
            if row_name in row_mapping:
                field_name = row_mapping[row_name]
                
                # Processa cada mês
                for mes_planilha, mes_dashboard in meses_map.items():
                    if mes_planilha in row and row[mes_planilha]:
                        # Inicializa o mês se não existir
                        if mes_dashboard not in meses_data:
                            meses_data[mes_dashboard] = {
                                'mes': mes_dashboard,
                                # Leads
                                'leads_totais': 0,
                                'leads_google_ads': 0,
                                'leads_meta_ads': 0,
                                'leads_instagram_organico': 0,
                                'leads_indicacao': 0,
                                'leads_origem_desconhecida': 0,
                                
                                # Consultas Marcadas
                                'consultas_marcadas_totais': 0,
                                'consultas_marcadas_google_ads': 0,
                                'consultas_marcadas_meta_ads': 0,
                                'consultas_marcadas_ig_organico': 0,
                                'consultas_marcadas_indicacao': 0,
                                'consultas_marcadas_outros': 0,
                                
                                # Consultas Comparecidas
                                'consultas_comparecidas': 0,
                                
                                # Fechamentos
                                'fechamentos_totais': 0,
                                'fechamentos_google_ads': 0,
                                'fechamentos_meta_ads': 0,
                                'fechamentos_ig_organico': 0,
                                'fechamentos_indicacao': 0,
                                'fechamentos_outros': 0,
                                
                                # Dados Financeiros
                                'faturamento': 0.0,
                                'valor_investido_total': 0.0,
                                'orcamento_previsto_total': 0.0,
                                'orcamento_realizado_facebook': 0.0,
                                'orcamento_previsto_facebook': 0.0,
                                'orcamento_realizado_google': 0.0,
                                'orcamento_previsto_google': 0.0,
                                
                                # KPIs de Conversão
                                'conversao_csm_leads': 0.0,
                                'conversao_csc_csm': 0.0,
                                'conversao_fechamento_csc': 0.0,
                                'conversao_fechamento_leads': 0.0,
                                
                                # KPIs Financeiros
                                'custo_por_compra_cirurgias': 0.0,
                                'roas': 0.0,
                                'custo_por_lead_total': 0.0,
                                'custo_por_consulta_marcada': 0.0,
                                'custo_por_consulta_comparecida': 0.0,
                                'ticket_medio': 0.0,
                                
                                # Taxas Ideais
                                'taxa_ideal_csm': 10.0,
                                'taxa_ideal_csc': 50.0,
                                'taxa_ideal_fechamentos': 40.0
                            }
                        
                        # Converte o valor para o tipo correto
                        valor = row[mes_planilha]
                        if valor and valor != 0 and valor != '-':
                            print(f"     📅 {mes_planilha}: {valor} ({field_name})")
                            if field_name in ['faturamento', 'valor_investido_total', 'orcamento_realizado_facebook', 'orcamento_realizado_google']:
                                # Remove formatação de moeda e converte para float
                                if isinstance(valor, str):
                                    valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
                                    # Remove caracteres não numéricos exceto ponto e vírgula
                                    valor = ''.join(c for c in valor if c.isdigit() or c in '.,-')
                                    # Trata valores negativos
                                    if valor.startswith('-'):
                                        valor = '0'
                                try:
                                    meses_data[mes_dashboard][field_name] = float(valor) if valor else 0.0
                                except (ValueError, TypeError):
                                    meses_data[mes_dashboard][field_name] = 0.0
                            else:
                                try:
                                    meses_data[mes_dashboard][field_name] = int(valor) if valor else 0
                                except (ValueError, TypeError):
                                    meses_data[mes_dashboard][field_name] = 0
    
    # Converte para lista
    processed_data = list(meses_data.values())
    
    print(f"📊 Dados processados: {len(processed_data)} meses")
    for mes_data in processed_data:
        if mes_data['leads_totais'] > 0:
            print(f"   📅 {mes_data['mes']}: {mes_data['leads_totais']} leads, R$ {mes_data['faturamento']:,.2f}")
    
    return processed_data

def import_from_google_sheets(sheet_id, sheet_name):
    """Importa dados de uma planilha específica - TODAS as abas"""
    gc = setup_google_sheets_auth()
    if not gc:
        return None
    
    try:
        print(f"📊 Acessando planilha: {sheet_name}")
        print(f"🔗 ID: {sheet_id}")
        
        # Abre a planilha
        sheet = gc.open_by_key(sheet_id)
        
        # Lista todas as abas
        worksheets = sheet.worksheets()
        print(f"📋 Abas encontradas: {[ws.title for ws in worksheets]}")
        
        all_data = []
        
        # Processa PRIMEIRO a aba "Controle de Leads" (prioridade)
        controle_leads_worksheet = None
        for worksheet in worksheets:
            if "Controle de Leads" in worksheet.title:
                controle_leads_worksheet = worksheet
                break
        
        if controle_leads_worksheet:
            print(f"📄 Processando aba principal: {controle_leads_worksheet.title}")
            
            try:
                # Obtém dados da aba "Controle de Leads"
                data = controle_leads_worksheet.get_all_records()
                
                if data and len(data) > 0:
                    print(f"   📊 {len(data)} registros encontrados na aba {controle_leads_worksheet.title}")
                    
                    # Processa TODOS os dados da aba "Controle de Leads"
                    processed_data = process_controle_leads_data(data)
                    if processed_data:
                        all_data.extend(processed_data)
                        print(f"   📈 {len(processed_data)} meses processados da aba {controle_leads_worksheet.title}")
                    else:
                        print(f"   ⚠️ Nenhum dado válido processado da aba {controle_leads_worksheet.title}")
                else:
                    print(f"   ⚠️ Aba {controle_leads_worksheet.title} vazia")
            except Exception as e:
                print(f"   ❌ Erro ao processar aba {controle_leads_worksheet.title}: {e}")
        else:
            print("   ❌ Aba 'Controle de Leads' não encontrada")
        
        # Se não encontrou dados na aba "Controle de Leads", procura em outras abas
        if not all_data:
            print(f"🔍 Aba 'Controle de Leads' vazia, procurando em outras abas...")
            
            for worksheet in worksheets:
                if "Controle de Leads" in worksheet.title:
                    continue  # Já processou
                    
                print(f"📄 Processando aba: {worksheet.title}")
                
                try:
                    data = worksheet.get_all_records()
                    
                    if data and len(data) > 0:
                        print(f"   📊 {len(data)} registros encontrados na aba {worksheet.title}")
                        
                        if is_dashboard_data_structure(data):
                            print(f"   ✅ Estrutura de dados válida encontrada!")
                            
                            processed_data = process_controle_leads_data(data)
                            if processed_data:
                                all_data.extend(processed_data)
                                print(f"   📈 {len(processed_data)} meses processados da aba {worksheet.title}")
                                break  # Para na primeira aba com dados válidos
                        else:
                            print(f"   ⚠️ Aba {worksheet.title} não tem estrutura de dados do dashboard")
                    else:
                        print(f"   ⚠️ Aba {worksheet.title} vazia ou sem dados")
                        
                except Exception as e:
                    print(f"   ❌ Erro ao processar aba {worksheet.title}: {e}")
                    continue
        
        if not all_data:
            print(f"❌ Nenhum dado encontrado em nenhuma aba da planilha {sheet_name}")
            return None
        
        print(f"📊 Total de registros encontrados: {len(all_data)}")
        
        # Converte para DataFrame
        df = pd.DataFrame(all_data)
        print(f"📋 Colunas encontradas: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro ao importar dados de {sheet_name}: {e}")
        return None

def create_sample_data(clinic_name):
    """Cria dados de exemplo para uma clínica"""
    
    if clinic_name == "joao":
        # Dados de exemplo para Dr. João (baseados no CSV existente)
        sample_data = [
            {
                'mes': 'Março',
                'leads_totais': 69,
                'leads_google_ads': 1,
                'leads_meta_ads': 4,
                'leads_instagram_organico': 47,
                'leads_indicacao': 16,
                'leads_origem_desconhecida': 1,
                'consultas_marcadas_totais': 7,
                'consultas_marcadas_google_ads': 0,
                'consultas_marcadas_meta_ads': 0,
                'consultas_marcadas_ig_organico': 4,
                'consultas_marcadas_indicacao': 1,
                'consultas_marcadas_outros': 2,
                'consultas_comparecidas': 6,
                'fechamentos_totais': 1,
                'fechamentos_google_ads': 0,
                'fechamentos_meta_ads': 2,
                'fechamentos_ig_organico': 0,
                'fechamentos_indicacao': 3,
                'fechamentos_outros': 0,
                'faturamento': 36250.0,
                'valor_investido_total': 3063.21,
                'orcamento_realizado_facebook': 1514.14,
                'orcamento_realizado_google': 1549.07
            },
            {
                'mes': 'Abril',
                'leads_totais': 267,
                'leads_google_ads': 68,
                'leads_meta_ads': 5,
                'leads_instagram_organico': 147,
                'leads_indicacao': 2,
                'leads_origem_desconhecida': 45,
                'consultas_marcadas_totais': 26,
                'consultas_marcadas_google_ads': 1,
                'consultas_marcadas_meta_ads': 4,
                'consultas_marcadas_ig_organico': 13,
                'consultas_marcadas_indicacao': 3,
                'consultas_marcadas_outros': 5,
                'consultas_comparecidas': 38,
                'fechamentos_totais': 8,
                'fechamentos_google_ads': 2,
                'fechamentos_meta_ads': 0,
                'fechamentos_ig_organico': 3,
                'fechamentos_indicacao': 0,
                'fechamentos_outros': 3,
                'faturamento': 360050.0,
                'valor_investido_total': 11730.24,
                'orcamento_realizado_facebook': 7880.25,
                'orcamento_realizado_google': 3849.99
            }
        ]
    else:  # taynah
        # Dados de exemplo para Dra Taynah
        sample_data = [
            {
                'mes': 'Janeiro',
                'leads_totais': 45,
                'leads_google_ads': 8,
                'leads_meta_ads': 12,
                'leads_instagram_organico': 20,
                'leads_indicacao': 5,
                'leads_origem_desconhecida': 0,
                'consultas_marcadas_totais': 8,
                'consultas_marcadas_google_ads': 2,
                'consultas_marcadas_meta_ads': 3,
                'consultas_marcadas_ig_organico': 2,
                'consultas_marcadas_indicacao': 1,
                'consultas_marcadas_outros': 0,
                'consultas_comparecidas': 6,
                'fechamentos_totais': 2,
                'fechamentos_google_ads': 1,
                'fechamentos_meta_ads': 0,
                'fechamentos_ig_organico': 1,
                'fechamentos_indicacao': 0,
                'fechamentos_outros': 0,
                'faturamento': 15000.0,
                'valor_investido_total': 2500.0,
                'orcamento_realizado_facebook': 1500.0,
                'orcamento_realizado_google': 1000.0
            },
            {
                'mes': 'Fevereiro',
                'leads_totais': 78,
                'leads_google_ads': 15,
                'leads_meta_ads': 20,
                'leads_instagram_organico': 35,
                'leads_indicacao': 8,
                'leads_origem_desconhecida': 0,
                'consultas_marcadas_totais': 15,
                'consultas_marcadas_google_ads': 4,
                'consultas_marcadas_meta_ads': 5,
                'consultas_marcadas_ig_organico': 4,
                'consultas_marcadas_indicacao': 2,
                'consultas_marcadas_outros': 0,
                'consultas_comparecidas': 12,
                'fechamentos_totais': 4,
                'fechamentos_google_ads': 2,
                'fechamentos_meta_ads': 1,
                'fechamentos_ig_organico': 1,
                'fechamentos_indicacao': 0,
                'fechamentos_outros': 0,
                'faturamento': 32000.0,
                'valor_investido_total': 4200.0,
                'orcamento_realizado_facebook': 2500.0,
                'orcamento_realizado_google': 1700.0
            }
        ]
    
    return pd.DataFrame(sample_data)

def load_clinic_data_from_sheets(clinic_key, cliente_id):
    """Carrega dados de uma clínica específica"""
    
    config = SHEETS_CONFIG[clinic_key]
    print(f"📊 Importando dados do Google Sheets para {config['name']} (ID: {cliente_id})")
    
    # Tenta importar do Google Sheets
    df = import_from_google_sheets(config['sheet_id'], config['name'])
    
    # Se não conseguir, usa dados de exemplo
    if df is None or (hasattr(df, 'empty') and df.empty):
        print(f"⚠️ Não foi possível acessar o Google Sheets de {config['name']}. Usando dados de exemplo...")
        df = create_sample_data(clinic_key)
    
    # Remove dados existentes da clínica
    print(f"🗑️ Removendo dados existentes de {config['name']}...")
    dados_existentes = dados_crud.get_dados_by_cliente(cliente_id)
    for dados in dados_existentes:
        dados_crud.delete_dados_dashboard(dados.id)
    
    # Carrega novos dados
    for _, row in df.iterrows():
        # Carrega TODOS os meses, mesmo os que têm apenas faturamento
        if row['leads_totais'] > 0 or row['faturamento'] > 0 or row['valor_investido_total'] > 0:
            dados = dados_crud.create_dados_dashboard(
                cliente_id=cliente_id,
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
                orcamento_realizado_facebook=float(row['orcamento_realizado_facebook']),
                orcamento_realizado_google=float(row['orcamento_realizado_google'])
            )
            
            if dados:
                print(f"   ✅ Dados de {row['mes']} carregados para {config['name']}")
            else:
                print(f"   ❌ Erro ao carregar dados de {row['mes']} para {config['name']}")
    
    print(f"✅ Dados de {config['name']} carregados com sucesso!")

def extract_sheet_id_from_url(url):
    """Extrai o ID da planilha de uma URL do Google Sheets"""
    if not url:
        return None
    
    # Padrões de URL do Google Sheets
    patterns = [
        r'/spreadsheets/d/([a-zA-Z0-9-_]+)',
        r'id=([a-zA-Z0-9-_]+)',
        r'/([a-zA-Z0-9-_]{44})'  # IDs do Google Sheets têm 44 caracteres
    ]
    
    import re
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def load_clinic_data_from_url(cliente):
    """Carrega dados de uma clínica usando seu link_empresa"""
    
    if not hasattr(cliente, 'link_empresa') or not cliente.link_empresa:
        print(f"⚠️ Clínica {cliente.nome_da_clinica} não tem link_empresa configurado")
        return False
    
    print(f"📊 Importando dados do Google Sheets para {cliente.nome_da_clinica} (ID: {cliente.id})")
    print(f"🔗 Link: {cliente.link_empresa}")
    
    # Extrai ID da planilha
    sheet_id = extract_sheet_id_from_url(cliente.link_empresa)
    if not sheet_id:
        print(f"❌ Não foi possível extrair ID da planilha de: {cliente.link_empresa}")
        return False
    
    print(f"📊 ID extraído: {sheet_id}")
    
    # Tenta importar do Google Sheets
    df = import_from_google_sheets(sheet_id, cliente.nome_da_clinica)
    
    if df is None or (hasattr(df, 'empty') and df.empty):
        print(f"❌ Não foi possível acessar o Google Sheets de {cliente.nome_da_clinica}")
        return False
    
    # Remove dados existentes da clínica
    print(f"🗑️ Removendo dados existentes de {cliente.nome_da_clinica}...")
    dados_existentes = dados_crud.get_dados_by_cliente(cliente.id)
    for dados in dados_existentes:
        dados_crud.delete_dados_dashboard(dados.id)
    
    # Carrega novos dados
    success_count = 0
    for _, row in df.iterrows():
        if row['leads_totais'] > 0:  # Só carrega meses com atividade
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
                orcamento_realizado_facebook=float(row['orcamento_realizado_facebook']),
                orcamento_realizado_google=float(row['orcamento_realizado_google'])
            )
            
            if dados:
                print(f"   ✅ Dados de {row['mes']} carregados para {cliente.nome_da_clinica}")
                success_count += 1
            else:
                print(f"   ❌ Erro ao carregar dados de {row['mes']} para {cliente.nome_da_clinica}")
    
    if success_count > 0:
        print(f"✅ Dados de {cliente.nome_da_clinica} carregados com sucesso! ({success_count} meses)")
        return True
    else:
        print(f"❌ Nenhum dado foi carregado para {cliente.nome_da_clinica}")
        return False

def main():
    """Função principal"""
    print("🏥 Importando dados de múltiplas planilhas do Google Sheets...")
    
    # Busca todas as clínicas
    clientes = cliente_crud.get_all_clientes()
    
    # Mapeia clínicas por email (excluindo admin)
    clientes_map = {}
    for cliente in clientes:
        if not cliente.is_admin:  # Exclui admin
            if cliente.email == "joao@clinicaestetica.com":
                clientes_map["joao"] = cliente
            elif cliente.email == "taynah@cirurgiaplastica.com":
                clientes_map["taynah"] = cliente
    
    print(f"📊 Clínicas configuradas: {len(clientes_map)}")
    
    # Importa dados de cada clínica configurada
    for clinic_key, cliente in clientes_map.items():
        print(f"\n🏥 Processando {cliente.nome_da_clinica}...")
        load_clinic_data_from_sheets(clinic_key, cliente.id)
    
    # Agora processa TODAS as clínicas que têm link_empresa configurado
    print(f"\n🔍 Verificando clínicas com link_empresa configurado...")
    clientes_com_link = []
    for cliente in clientes:
        if not cliente.is_admin and hasattr(cliente, 'link_empresa') and cliente.link_empresa:
            clientes_com_link.append(cliente)
    
    print(f"📊 Clínicas com link_empresa: {len(clientes_com_link)}")
    
    for cliente in clientes_com_link:
        print(f"\n🏥 Processando {cliente.nome_da_clinica}...")
        load_clinic_data_from_url(cliente)
    
    print("\n🎉 Importação concluída!")
    print("💡 Todas as clínicas podem agora fazer login e visualizar seus dados no dashboard.")
    print("\n📋 Credenciais:")
    print("   👑 Admin: admin@prestigeclinic.com / admin123")
    print("   🏥 Dr. João: joao@clinicaestetica.com / clinica123")
    print("   🏥 Dra Taynah: taynah@cirurgiaplastica.com / taynah2024")

if __name__ == "__main__":
    main()
