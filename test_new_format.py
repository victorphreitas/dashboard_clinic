"""
Script de teste para verificar se o novo formato está funcionando corretamente.
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("🔍 Testando conexão com banco de dados...")
    
    try:
        from database import db_manager, dados_crud
        
        # Testa conexão
        session = db_manager.get_session()
        session.close()
        print("✅ Conexão com banco de dados: OK")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

def test_new_fields():
    """Testa se os novos campos estão disponíveis"""
    print("🔍 Testando novos campos...")
    
    try:
        from database import db_manager
        from sqlalchemy import text
        
        session = db_manager.get_session()
        
        # Verifica se as novas colunas existem
        result = session.execute(text("PRAGMA table_info(dados_dashboard)"))
        columns = [row[1] for row in result.fetchall()]
        
        new_columns = [
            'valor_investido_total',
            'orcamento_previsto_total',
            'orcamento_realizado_facebook',
            'orcamento_previsto_facebook',
            'orcamento_realizado_google',
            'orcamento_previsto_google',
            'conversao_csm_leads',
            'conversao_csc_csm',
            'conversao_fechamento_csc',
            'conversao_fechamento_leads',
            'custo_por_compra_cirurgias',
            'custo_por_lead_total',
            'taxa_ideal_csm',
            'taxa_ideal_csc',
            'taxa_ideal_fechamentos'
        ]
        
        missing_columns = [col for col in new_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Colunas faltando: {missing_columns}")
            return False
        else:
            print("✅ Todos os novos campos estão disponíveis")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar campos: {e}")
        return False
    finally:
        session.close()

def test_google_sheets_auth():
    """Testa autenticação com Google Sheets"""
    print("🔍 Testando autenticação com Google Sheets...")
    
    try:
        from import_multiple_sheets import setup_google_sheets_auth
        
        gc = setup_google_sheets_auth()
        if gc:
            print("✅ Autenticação com Google Sheets: OK")
            return True
        else:
            print("❌ Falha na autenticação com Google Sheets")
            return False
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return False

def test_dashboard_functions():
    """Testa se as funções do dashboard estão funcionando"""
    print("🔍 Testando funções do dashboard...")
    
    try:
        from dashboard import (
            create_conversion_analysis, 
            create_budget_analysis,
            create_executive_summary,
            create_kpi_cards
        )
        print("✅ Funções do dashboard: OK")
        return True
    except Exception as e:
        print(f"❌ Erro nas funções do dashboard: {e}")
        return False

def test_data_processing():
    """Testa processamento de dados"""
    print("🔍 Testando processamento de dados...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # Cria DataFrame de teste
        test_data = {
            'Meses': ['Janeiro', 'Fevereiro'],
            'Leads_Totais': [100, 120],
            'Faturamento': [5000, 6000],
            'Valor_Investido_Total': [1000, 1200],
            'Consultas_Marcadas_Totais': [20, 25],
            'Consultas_Comparecidas': [15, 20],
            'Fechamentos_Totais': [10, 12]
        }
        
        df = pd.DataFrame(test_data)
        
        # Testa cálculos de KPIs
        df['Conversao_Csm_Leads'] = (df['Consultas_Marcadas_Totais'] / df['Leads_Totais']) * 100
        df['Conversao_Csc_Csm'] = (df['Consultas_Comparecidas'] / df['Consultas_Marcadas_Totais']) * 100
        df['ROAS'] = df['Faturamento'] / df['Valor_Investido_Total']
        
        print("✅ Processamento de dados: OK")
        return True
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE DO NOVO FORMATO - SISTEMA ATUALIZADO")
    print("=" * 60)
    
    tests = [
        ("Conexão com Banco", test_database_connection),
        ("Novos Campos", test_new_fields),
        ("Autenticação Google Sheets", test_google_sheets_auth),
        ("Funções Dashboard", test_dashboard_functions),
        ("Processamento de Dados", test_data_processing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema atualizado com sucesso!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Faça commit e push das alterações")
        print("2. Teste o sistema localmente")
        print("3. Faça deploy em produção")
        print("4. Teste com dados reais da planilha")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM! Verifique os erros acima.")
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrija os erros identificados")
        print("2. Execute os testes novamente")
        print("3. Só prossiga quando todos os testes passarem")

if __name__ == "__main__":
    main()
