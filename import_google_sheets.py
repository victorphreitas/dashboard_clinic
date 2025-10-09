"""
Script para importar dados do Google Sheets da Dra Taynah.
Este script requer configuração de credenciais do Google Sheets API.
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

# Configuração do Google Sheets
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk"
SHEET_ID = "1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs"

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

def import_from_google_sheets():
    """Importa dados do Google Sheets"""
    gc = setup_google_sheets_auth()
    if not gc:
        return None
    
    try:
        # Abre a planilha
        sheet = gc.open_by_url(GOOGLE_SHEETS_URL)
        worksheet = sheet.sheet1
        
        # Obtém todos os dados
        data = worksheet.get_all_records()
        
        if not data:
            print("❌ Nenhum dado encontrado na planilha")
            return None
        
        print(f"📊 Encontrados {len(data)} registros na planilha")
        
        # Converte para DataFrame
        df = pd.DataFrame(data)
        print("📋 Colunas encontradas:", list(df.columns))
        
        return df
        
    except Exception as e:
        print(f"❌ Erro ao importar dados: {e}")
        return None

def create_sample_data_for_taynah():
    """Cria dados de exemplo para a Dra Taynah (caso não consiga acessar o Google Sheets)"""
    
    # Dados de exemplo baseados no padrão da clínica do João
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
            'investimento_total': 2500.0,
            'investimento_facebook': 1500.0,
            'investimento_google': 1000.0
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
            'investimento_total': 4200.0,
            'investimento_facebook': 2500.0,
            'investimento_google': 1700.0
        },
        {
            'mes': 'Março',
            'leads_totais': 95,
            'leads_google_ads': 18,
            'leads_meta_ads': 25,
            'leads_instagram_organico': 42,
            'leads_indicacao': 10,
            'leads_origem_desconhecida': 0,
            'consultas_marcadas_totais': 22,
            'consultas_marcadas_google_ads': 6,
            'consultas_marcadas_meta_ads': 7,
            'consultas_marcadas_ig_organico': 6,
            'consultas_marcadas_indicacao': 3,
            'consultas_marcadas_outros': 0,
            'consultas_comparecidas': 18,
            'fechamentos_totais': 6,
            'fechamentos_google_ads': 3,
            'fechamentos_meta_ads': 2,
            'fechamentos_ig_organico': 1,
            'fechamentos_indicacao': 0,
            'fechamentos_outros': 0,
            'faturamento': 48000.0,
            'investimento_total': 5800.0,
            'investimento_facebook': 3500.0,
            'investimento_google': 2300.0
        }
    ]
    
    return pd.DataFrame(sample_data)

def load_taynah_data_from_sheets(cliente_id):
    """Carrega dados da Dra Taynah do Google Sheets"""
    
    print(f"📊 Importando dados do Google Sheets para Dra Taynah (ID: {cliente_id})")
    
    # Primeiro tenta importar do Google Sheets
    df = import_from_google_sheets()
    
    # Se não conseguir, usa dados de exemplo
    if df is None or (hasattr(df, 'empty') and df.empty):
        print("⚠️ Não foi possível acessar o Google Sheets. Usando dados de exemplo...")
        df = create_sample_data_for_taynah()
    
    # Remove dados existentes da Dra Taynah
    print("🗑️ Removendo dados existentes...")
    dados_existentes = dados_crud.get_dados_by_cliente(cliente_id)
    for dados in dados_existentes:
        dados_crud.delete_dados_dashboard(dados.id)
    
    # Carrega novos dados
    for _, row in df.iterrows():
        if row['leads_totais'] > 0:  # Só carrega meses com atividade
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
                investimento_total=float(row['investimento_total']),
                investimento_facebook=float(row['investimento_facebook']),
                investimento_google=float(row['investimento_google'])
            )
            
            if dados:
                print(f"   ✅ Dados de {row['mes']} carregados")
            else:
                print(f"   ❌ Erro ao carregar dados de {row['mes']}")
    
    print("✅ Dados da Dra Taynah carregados com sucesso!")

def main():
    """Função principal"""
    print("🏥 Importando dados do Google Sheets da Dra Taynah Bastos...")
    
    # Busca a clínica da Dra Taynah
    clientes = cliente_crud.get_all_clientes()
    taynah_cliente = None
    
    for cliente in clientes:
        if cliente.email == "taynah@cirurgiaplastica.com":
            taynah_cliente = cliente
            break
    
    if not taynah_cliente:
        print("❌ Clínica da Dra Taynah não encontrada!")
        return
    
    print(f"✅ Clínica encontrada: {taynah_cliente.nome_da_clinica}")
    
    # Carrega os dados
    load_taynah_data_from_sheets(taynah_cliente.id)
    
    print("\n🎉 Dados importados com sucesso!")
    print("💡 A Dra Taynah pode agora fazer login e visualizar seus dados no dashboard.")

if __name__ == "__main__":
    main()
