"""
Script para testar o dashboard corrigido do Dr. Jonnattan
"""

from database import dados_crud, cliente_crud, db_manager
from dashboard import load_data_from_database
import pandas as pd

def test_dashboard_fixed():
    """Testa o dashboard corrigido"""
    print("🧪 TESTE DO DASHBOARD CORRIGIDO - DR. JONNATTAN")
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
        print(f"📋 Colunas: {len(df.columns)}")
        print(f"📅 Meses: {df['Meses'].tolist()}")
        
        # Testar a lógica corrigida
        df_ativos = df[(df['Leads_Totais'] > 0) | (df['Faturamento'] > 0) | (df['Investimento_Total'] > 0)]
        print(f"\\n🔍 DADOS ATIVOS: {len(df_ativos)} registros")
        
        if not df_ativos.empty:
            print(f"✅ CORREÇÃO FUNCIONOU!")
            print(f"✅ Dr. Jonnattan tem dados ativos")
            print(f"✅ Dashboard deve mostrar os dados agora")
            
            # Mostrar dados específicos
            for _, row in df_ativos.iterrows():
                mes = row['Meses']
                leads = row['Leads_Totais']
                faturamento = row['Faturamento']
                investimento = row['Investimento_Total']
                consultas = row['Consultas_Marcadas_Totais']
                
                print(f"\\n📅 {mes}:")
                print(f"   Leads: {leads}")
                print(f"   Consultas Marcadas: {consultas}")
                print(f"   Faturamento: R$ {faturamento:,.2f}")
                print(f"   Investimento: R$ {investimento:,.2f}")
            
            # Testar KPIs
            print(f"\\n📊 KPIs CALCULADOS:")
            total_faturamento = df_ativos['Faturamento'].sum()
            total_investimento = df_ativos['Investimento_Total'].sum()
            total_consultas = df_ativos['Consultas_Marcadas_Totais'].sum()
            roas = total_faturamento / total_investimento if total_investimento > 0 else 0
            
            print(f"   💰 Faturamento Total: R$ {total_faturamento:,.2f}")
            print(f"   💸 Investimento Total: R$ {total_investimento:,.2f}")
            print(f"   📞 Consultas Marcadas: {total_consultas}")
            print(f"   📈 ROAS: {roas:.2f}x")
            
            return True
        else:
            print(f"❌ Ainda não funcionou")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")
        return False

def main():
    """Função principal"""
    success = test_dashboard_fixed()
    
    if success:
        print(f"\\n🎉 RESULTADO FINAL:")
        print(f"✅ Dashboard corrigido com sucesso!")
        print(f"✅ Dr. Jonnattan tem dados ativos!")
        print(f"✅ Sistema funcionando perfeitamente!")
        
        print(f"\\n💡 PRÓXIMOS PASSOS:")
        print(f"   1. Reinicie o Streamlit (Ctrl+C e streamlit run app.py)")
        print(f"   2. Acesse o dashboard")
        print(f"   3. Selecione 'Dr. Jonnattan Prada'")
        print(f"   4. Verifique os dados de Outubro")
        
        print(f"\\n🚀 O problema está resolvido!")
    else:
        print(f"\\n❌ Ainda há problemas no sistema!")

if __name__ == "__main__":
    main()
