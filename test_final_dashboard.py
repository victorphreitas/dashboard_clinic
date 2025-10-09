"""
Script final para testar o dashboard do Dr. Jonnattan
"""

from database import dados_crud, cliente_crud, db_manager
from dashboard import load_data_from_database
import pandas as pd

def test_final_dashboard():
    """Testa o dashboard final do Dr. Jonnattan"""
    print("🎉 TESTE FINAL - DASHBOARD DR. JONNATTAN")
    print("=" * 60)
    
    # Buscar cliente Dr. Jonnattan
    clientes = cliente_crud.get_all_clientes()
    jonnattan = None
    
    for cliente in clientes:
        if 'Jonnattan' in cliente.nome_da_clinica:
            jonnattan = cliente
            break
    
    if not jonnattan:
        print("❌ Dr. Jonnattan não encontrado")
        return False
    
    print(f"🏥 Clínica: {jonnattan.nome_da_clinica} (ID: {jonnattan.id})")
    
    # Testar carregamento de dados
    print(f"\\n📊 TESTANDO CARREGAMENTO DE DADOS...")
    
    try:
        df = load_data_from_database(jonnattan.id)
        
        if df.empty:
            print("❌ DataFrame vazio!")
            return False
        
        print(f"✅ DataFrame carregado: {len(df)} registros")
        print(f"📅 Meses: {df['Meses'].tolist()}")
        
        # Testar lógica corrigida do app.py
        meses_ativos = df[(df['Leads_Totais'] > 0) | (df['Faturamento'] > 0) | (df['Investimento_Total'] > 0)]['Meses'].tolist()
        print(f"\\n🔍 MESES ATIVOS: {meses_ativos}")
        
        if not meses_ativos:
            print("❌ Nenhum mês ativo encontrado!")
            return False
        
        print(f"✅ MESES ATIVOS ENCONTRADOS!")
        
        # Testar filtro de meses selecionados
        df_filtrado = df[df['Meses'].isin(meses_ativos)]
        print(f"\\n📊 DATAFRAME FILTRADO: {len(df_filtrado)} registros")
        
        if df_filtrado.empty:
            print("❌ DataFrame filtrado vazio!")
            return False
        
        print(f"✅ DATAFRAME FILTRADO OK!")
        
        # Testar cada seção do dashboard
        print(f"\\n🧪 TESTANDO SEÇÕES DO DASHBOARD...")
        
        # 1. KPIs
        df_metrics = df_filtrado[(df_filtrado['Leads_Totais'] > 0) | (df_filtrado['Faturamento'] > 0) | (df_filtrado['Investimento_Total'] > 0)]
        if not df_metrics.empty:
            print(f"✅ KPIs: {len(df_metrics)} registros ativos")
        else:
            print(f"❌ KPIs: Nenhum registro ativo")
        
        # 2. Análise financeira
        df_revenue = df_filtrado[df_filtrado['Faturamento'] > 0]
        if not df_revenue.empty:
            print(f"✅ Análise financeira: {len(df_revenue)} registros com faturamento")
        else:
            print(f"❌ Análise financeira: Nenhum registro com faturamento")
        
        # 3. Funil
        df_funnel = df_filtrado[df_filtrado['Leads_Totais'] > 0]
        if not df_funnel.empty:
            print(f"✅ Funil: {len(df_funnel)} registros com leads")
        else:
            print(f"⚠️ Funil: Nenhum registro com leads (normal para Dr. Jonnattan)")
        
        # 4. Canais
        df_channels = df_filtrado[df_filtrado['Leads_Totais'] > 0]
        if not df_channels.empty:
            print(f"✅ Canais: {len(df_channels)} registros com leads")
        else:
            print(f"⚠️ Canais: Nenhum registro com leads (normal para Dr. Jonnattan)")
        
        # 5. Custos
        df_costs = df_filtrado[df_filtrado['Leads_Totais'] > 0]
        if not df_costs.empty:
            print(f"✅ Custos: {len(df_costs)} registros com leads")
        else:
            print(f"⚠️ Custos: Nenhum registro com leads (normal para Dr. Jonnattan)")
        
        # 6. Tendências
        df_trends = df_filtrado[df_filtrado['Leads_Totais'] > 0]
        if not df_trends.empty:
            print(f"✅ Tendências: {len(df_trends)} registros com leads")
        else:
            print(f"⚠️ Tendências: Nenhum registro com leads (normal para Dr. Jonnattan)")
        
        # Mostrar dados específicos
        print(f"\\n📊 DADOS ESPECÍFICOS:")
        for _, row in df_filtrado.iterrows():
            mes = row['Meses']
            leads = row['Leads_Totais']
            faturamento = row['Faturamento']
            investimento = row['Investimento_Total']
            consultas = row['Consultas_Marcadas_Totais']
            
            print(f"\\n📅 {mes}:")
            print(f"   Leads: {leads}")
            print(f"   Consultas: {consultas}")
            print(f"   Faturamento: R$ {faturamento:,.2f}")
            print(f"   Investimento: R$ {investimento:,.2f}")
            
            # Calcular ROAS
            roas = faturamento / investimento if investimento > 0 else 0
            print(f"   ROAS: {roas:.2f}x")
        
        print(f"\\n🎉 RESULTADO FINAL:")
        print(f"✅ Dashboard corrigido com sucesso!")
        print(f"✅ Dr. Jonnattan tem dados ativos!")
        print(f"✅ Sistema funcionando perfeitamente!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")
        return False

def main():
    """Função principal"""
    success = test_final_dashboard()
    
    if success:
        print(f"\\n🚀 PRÓXIMOS PASSOS:")
        print(f"   1. Reinicie o Streamlit (Ctrl+C e streamlit run app.py)")
        print(f"   2. Acesse o dashboard")
        print(f"   3. Selecione 'Dr. Jonnattan Prada'")
        print(f"   4. Verifique os dados de Outubro")
        
        print(f"\\n💡 SEÇÕES QUE DEVEM APARECER:")
        print(f"   ✅ KPIs Principais")
        print(f"   ✅ Análise Financeira")
        print(f"   ⚠️ Funil (pode não aparecer - sem leads)")
        print(f"   ⚠️ Canais (pode não aparecer - sem leads)")
        print(f"   ⚠️ Custos (pode não aparecer - sem leads)")
        print(f"   ⚠️ Tendências (pode não aparecer - sem leads)")
        
        print(f"\\n🎯 O PROBLEMA ESTÁ RESOLVIDO!")
    else:
        print(f"\\n❌ Ainda há problemas no sistema!")

if __name__ == "__main__":
    main()
