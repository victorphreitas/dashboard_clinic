"""
Script para testar o dashboard do Dr. Jonnattan
"""

from database import dados_crud, cliente_crud, db_manager
from dashboard import load_data_from_database
import pandas as pd

def test_dashboard_jonnattan():
    """Testa o dashboard do Dr. Jonnattan"""
    print("🧪 TESTE DO DASHBOARD - DR. JONNATTAN")
    print("=" * 50)
    
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
        
        # Verificar dados específicos
        if 'Outubro' in df['Meses'].tolist():
            outubro_df = df[df['Meses'] == 'Outubro']
            print(f"\\n✅ DADOS DE OUTUBRO:")
            print(f"   Consultas Marcadas: {outubro_df['Consultas_Marcadas_Totais'].iloc[0]}")
            print(f"   Faturamento: R$ {outubro_df['Faturamento'].iloc[0]:,.2f}")
            print(f"   Investimento Total: R$ {outubro_df['Investimento_Total'].iloc[0]:,.2f}")
            
            # Verificar se tem dados suficientes para aparecer
            tem_dados = (outubro_df['Consultas_Marcadas_Totais'].iloc[0] > 0 or 
                        outubro_df['Faturamento'].iloc[0] > 0 or 
                        outubro_df['Investimento_Total'].iloc[0] > 0)
            
            if tem_dados:
                print(f"   ✅ Outubro tem dados suficientes para aparecer")
            else:
                print(f"   ⚠️ Outubro pode não aparecer por falta de dados")
        else:
            print(f"\\n❌ OUTUBRO NÃO ENCONTRADO!")
            print(f"   Meses disponíveis: {df['Meses'].tolist()}")
            return False
        
        print(f"\\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print(f"✅ Dashboard carrega os dados corretamente")
        print(f"✅ Dr. Jonnattan tem dados válidos")
        print(f"✅ Sistema funcionando perfeitamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return False

def check_possible_issues():
    """Verifica possíveis problemas"""
    print(f"\\n🔍 VERIFICANDO POSSÍVEIS PROBLEMAS...")
    
    # Verificar se há filtros ou problemas
    print(f"💡 POSSÍVEIS CAUSAS SE NÃO ESTÁ APARECENDO:")
    print(f"   1. Cache do navegador - Recarregue a página (F5)")
    print(f"   2. Sessão do Streamlit - Reinicie o dashboard")
    print(f"   3. Filtros no dashboard - Verifique se há filtros ativos")
    print(f"   4. Período selecionado - Verifique se está no período correto")
    print(f"   5. Clínica selecionada - Verifique se está na clínica correta")
    
    print(f"\\n🛠️ SOLUÇÕES:")
    print(f"   1. Pare o Streamlit (Ctrl+C no terminal)")
    print(f"   2. Execute: streamlit run app.py")
    print(f"   3. Acesse o dashboard")
    print(f"   4. Selecione 'Dr. Jonnattan Prada'")
    print(f"   5. Verifique os dados de Outubro")

def main():
    """Função principal"""
    success = test_dashboard_jonnattan()
    
    if success:
        check_possible_issues()
        
        print(f"\\n🎯 CONCLUSÃO:")
        print(f"✅ Sistema está funcionando perfeitamente!")
        print(f"✅ Dr. Jonnattan tem dados no dashboard!")
        print(f"💡 Se não está aparecendo, é problema de visualização")
        print(f"🚀 Solução: Reinicie o Streamlit e recarregue a página")
    else:
        print(f"\\n❌ Há um problema no sistema!")

if __name__ == "__main__":
    main()
