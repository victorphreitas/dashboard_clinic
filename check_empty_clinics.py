"""
Script para verificar e corrigir clínicas sem dados
"""

from database import dados_crud, cliente_crud, db_manager
from import_multiple_sheets import import_from_google_sheets, process_controle_leads_data
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

def check_empty_clinics():
    """Verifica clínicas sem dados e tenta importar"""
    print("🔍 Verificando clínicas sem dados...")
    
    # Buscar todas as clínicas
    clientes = cliente_crud.get_all_clientes()
    empty_clinics = []
    
    for cliente in clientes:
        if not cliente.is_admin and hasattr(cliente, 'link_empresa') and cliente.link_empresa:
            # Verificar se tem dados
            dados = dados_crud.get_dados_by_cliente(cliente.id)
            
            if len(dados) == 0:
                empty_clinics.append(cliente)
                print(f"⚠️ {cliente.nome_da_clinica}: Sem dados")
            else:
                print(f"✅ {cliente.nome_da_clinica}: {len(dados)} registros")
    
    if not empty_clinics:
        print("\n🎉 Todas as clínicas têm dados!")
        return True
    
    print(f"\n📊 Clínicas sem dados: {len(empty_clinics)}")
    
    # Tentar importar dados para clínicas vazias
    success_count = 0
    for cliente in empty_clinics:
        print(f"\n🔄 Tentando importar dados para {cliente.nome_da_clinica}...")
        
        # Extrair ID da planilha
        sheet_id = extract_sheet_id_from_url(cliente.link_empresa)
        if not sheet_id:
            print(f"❌ Não foi possível extrair ID da planilha: {cliente.link_empresa}")
            continue
        
        try:
            # Tentar importar dados
            df = import_from_google_sheets(sheet_id, cliente.nome_da_clinica)
            
            if df is None or df.empty:
                print(f"❌ Não foi possível acessar planilha de {cliente.nome_da_clinica}")
                print(f"💡 Verifique se a planilha foi compartilhada com:")
                print(f"   dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com")
                continue
            
            # Remover dados existentes (se houver)
            dados_existentes = dados_crud.get_dados_by_cliente(cliente.id)
            for dados in dados_existentes:
                dados_crud.delete_dados_dashboard(dados.id)
            
            # Inserir novos dados
            success_count_clinic = 0
            for _, row in df.iterrows():
                if row['leads_totais'] > 0 or row['faturamento'] > 0 or row['investimento_total'] > 0:
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
                        investimento_total=float(row['investimento_total']),
                        investimento_facebook=float(row['investimento_facebook']),
                        investimento_google=float(row['investimento_google'])
                    )
                    
                    if dados:
                        success_count_clinic += 1
            
            if success_count_clinic > 0:
                print(f"✅ {cliente.nome_da_clinica}: {success_count_clinic} meses importados")
                success_count += 1
            else:
                print(f"⚠️ {cliente.nome_da_clinica}: Nenhum dado válido encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao importar dados de {cliente.nome_da_clinica}: {e}")
            continue
    
    print(f"\n🎉 Resultado: {success_count}/{len(empty_clinics)} clínicas corrigidas")
    
    if success_count < len(empty_clinics):
        print(f"\n💡 Clínicas que ainda precisam de atenção:")
        for cliente in empty_clinics:
            dados = dados_crud.get_dados_by_cliente(cliente.id)
            if len(dados) == 0:
                print(f"   - {cliente.nome_da_clinica}")
                print(f"     Link: {cliente.link_empresa}")
                print(f"     Ação: Compartilhar planilha com service account")
    
    return success_count > 0

if __name__ == "__main__":
    check_empty_clinics()

