"""
Script para debugar o dashboard e verificar se os dados estão sendo mostrados corretamente
"""

import pandas as pd
from database import dados_crud, cliente_crud, db_manager
from dashboard import load_data_from_database

def debug_dashboard():
    """Debuga o dashboard para verificar se os dados estão sendo mostrados"""
    print("🔍 DEBUG DO DASHBOARD")
    print("=" * 50)
    
    # Buscar cliente Dra Marlei
    clientes = cliente_crud.get_all_clientes()
    dra_marlei = None
    for cliente in clientes:
        if 'Marlei' in cliente.nome_da_clinica:
            dra_marlei = cliente
            break
    
    if not dra_marlei:
        print("❌ Clínica Dra Marlei não encontrada")
        return
    
    print(f"🏥 Clínica: {dra_marlei.nome_da_clinica} (ID: {dra_marlei.id})")
    
    # 1. Verificar dados no banco
    print("\n📊 1. DADOS NO BANCO:")
    dados_crud_instance = dados_crud
    dados = dados_crud_instance.get_dados_by_cliente(dra_marlei.id)
    
    print(f"   Total de registros: {len(dados)}")
    for dado in dados:
        print(f"   📅 {dado.mes}: {dado.leads_totais} leads, R$ {dado.faturamento:,.2f}")
    
    # 2. Verificar DataFrame do dashboard
    print("\n📊 2. DATAFRAME DO DASHBOARD:")
    df = load_data_from_database(dra_marlei.id)
    
    print(f"   Total de registros: {len(df)}")
    if not df.empty:
        print(f"   Colunas: {len(df.columns)}")
        print(f"   Meses: {df['Meses'].tolist()}")
        
        # Verificar Março especificamente
        marcos_df = df[df['Meses'] == 'Março']
        if not marcos_df.empty:
            print(f"\n✅ MARÇO ENCONTRADO NO DASHBOARD:")
            print(f"   Leads Totais: {marcos_df['Leads_Totais'].iloc[0]}")
            print(f"   Faturamento: R$ {marcos_df['Faturamento'].iloc[0]:,.2f}")
            print(f"   Investimento Total: R$ {marcos_df['Investimento_Total'].iloc[0]:,.2f}")
        else:
            print(f"\n❌ MARÇO NÃO ENCONTRADO NO DASHBOARD!")
            print(f"   Meses disponíveis: {df['Meses'].tolist()}")
    
    # 3. Verificar se há filtros ou problemas
    print("\n📊 3. ANÁLISE DE POSSÍVEIS PROBLEMAS:")
    
    if len(dados) != len(df):
        print(f"   ⚠️ Inconsistência: {len(dados)} registros no banco vs {len(df)} no DataFrame")
    else:
        print(f"   ✅ Consistência: {len(dados)} registros em ambos")
    
    # Verificar se Março tem dados significativos
    marcos_banco = [d for d in dados if d.mes == 'Março']
    if marcos_banco:
        marcos_dados = marcos_banco[0]
        print(f"\n📊 4. ANÁLISE DO MARÇO:")
        print(f"   Leads Totais: {marcos_dados.leads_totais}")
        print(f"   Faturamento: R$ {marcos_dados.faturamento:,.2f}")
        print(f"   Investimento Total: R$ {marcos_dados.investimento_total:,.2f}")
        
        # Verificar se tem dados suficientes para aparecer
        tem_dados = (marcos_dados.leads_totais > 0 or 
                    marcos_dados.faturamento > 0 or 
                    marcos_dados.investimento_total > 0)
        
        if tem_dados:
            print(f"   ✅ Março tem dados suficientes para aparecer")
        else:
            print(f"   ⚠️ Março pode não aparecer por falta de dados")
    
    print("\n🎯 CONCLUSÃO:")
    if len(dados) >= 3 and 'Março' in [d.mes for d in dados]:
        print("   ✅ Sistema está funcionando corretamente!")
        print("   ✅ Março está no banco e no dashboard!")
        print("   💡 Se não está aparecendo, pode ser:")
        print("      - Cache do navegador (recarregue F5)")
        print("      - Sessão do Streamlit (reinicie)")
        print("      - Filtros no dashboard (verifique)")
    else:
        print("   ❌ Há um problema no sistema!")

if __name__ == "__main__":
    debug_dashboard()

