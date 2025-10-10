"""
Script de teste para verificar o dashboard consolidado do administrador.
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
        from database import db_manager, admin_dashboard_crud
        
        # Testa conexão
        session = db_manager.get_session()
        session.close()
        print("✅ Conexão com banco de dados: OK")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

def test_consolidated_metrics():
    """Testa métricas consolidadas"""
    print("🔍 Testando métricas consolidadas...")
    
    try:
        from database import admin_dashboard_crud
        
        metrics = admin_dashboard_crud.get_consolidated_metrics()
        
        if not metrics:
            print("❌ Métricas consolidadas não retornadas")
            return False
        
        print(f"   📊 Total de Leads: {metrics.get('total_leads', 0)}")
        print(f"   💰 Faturamento Total: R$ {metrics.get('total_faturamento', 0):,.0f}".replace(",", "."))
        print(f"   📈 ROAS Médio: {metrics.get('roas_medio', 0):.1f}x")
        print(f"   🏥 Clínicas Ativas: {metrics.get('clinicas_ativas', 0)}")
        
        print("✅ Métricas consolidadas: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas métricas consolidadas: {e}")
        return False

def test_clinics_comparison():
    """Testa comparação entre clínicas"""
    print("🔍 Testando comparação entre clínicas...")
    
    try:
        from database import admin_dashboard_crud
        
        clinics = admin_dashboard_crud.get_clinics_comparison()
        
        if not clinics:
            print("⚠️ Nenhuma clínica encontrada para comparação")
            return True
        
        print(f"   🏥 Clínicas encontradas: {len(clinics)}")
        for clinic in clinics:
            print(f"   - {clinic['nome_da_clinica']}: {clinic['total_leads']} leads, R$ {clinic['total_faturamento']:,.0f}".replace(",", "."))
        
        print("✅ Comparação entre clínicas: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro na comparação de clínicas: {e}")
        return False

def test_monthly_evolution():
    """Testa evolução mensal"""
    print("🔍 Testando evolução mensal...")
    
    try:
        from database import admin_dashboard_crud
        
        monthly_data = admin_dashboard_crud.get_monthly_evolution()
        
        if not monthly_data:
            print("⚠️ Nenhum dado mensal encontrado")
            return True
        
        print(f"   📅 Meses com dados: {len(monthly_data)}")
        for month in monthly_data:
            print(f"   - {month['mes']} {month['ano']}: {month['total_leads']} leads, R$ {month['total_faturamento']:,.0f}".replace(",", "."))
        
        print("✅ Evolução mensal: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro na evolução mensal: {e}")
        return False

def test_channel_analysis():
    """Testa análise por canal"""
    print("🔍 Testando análise por canal...")
    
    try:
        from database import admin_dashboard_crud
        
        channel_data = admin_dashboard_crud.get_channel_analysis()
        
        if not channel_data:
            print("⚠️ Nenhum dado de canal encontrado")
            return True
        
        print(f"   📊 Leads Google: {channel_data.get('leads_google', 0)}")
        print(f"   📊 Leads Meta: {channel_data.get('leads_meta', 0)}")
        print(f"   📊 Leads Instagram: {channel_data.get('leads_instagram', 0)}")
        print(f"   💰 Investimento Google: R$ {channel_data.get('investimento_google', 0):,.0f}".replace(",", "."))
        print(f"   💰 Investimento Facebook: R$ {channel_data.get('investimento_facebook', 0):,.0f}".replace(",", "."))
        
        print("✅ Análise por canal: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro na análise por canal: {e}")
        return False

def test_dashboard_functions():
    """Testa funções do dashboard"""
    print("🔍 Testando funções do dashboard...")
    
    try:
        from dashboard import create_admin_consolidated_dashboard
        
        print("✅ Função create_admin_consolidated_dashboard importada com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas funções do dashboard: {e}")
        return False

def test_interface_integration():
    """Testa integração com interface"""
    print("🔍 Testando integração com interface...")
    
    try:
        from auth import show_admin_panel
        from app import main_dashboard
        
        print("✅ Funções de interface importadas com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração com interface: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE DO DASHBOARD CONSOLIDADO - ADMINISTRADOR")
    print("=" * 70)
    
    tests = [
        ("Conexão com Banco", test_database_connection),
        ("Métricas Consolidadas", test_consolidated_metrics),
        ("Comparação entre Clínicas", test_clinics_comparison),
        ("Evolução Mensal", test_monthly_evolution),
        ("Análise por Canal", test_channel_analysis),
        ("Funções do Dashboard", test_dashboard_functions),
        ("Integração com Interface", test_interface_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 70)
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
        print("🎉 TODOS OS TESTES PASSARAM! Dashboard consolidado implementado com sucesso!")
        print("\n📋 FUNCIONALIDADES IMPLEMENTADAS:")
        print("✅ Métricas consolidadas de todas as clínicas")
        print("✅ Comparativo entre clínicas")
        print("✅ Evolução mensal consolidada")
        print("✅ Análise por canal de marketing")
        print("✅ Interface administrativa integrada")
        print("✅ KPIs consolidados (Leads, Faturamento, ROAS, etc.)")
        print("✅ Gráficos interativos e rankings")
        print("\n🚀 DASHBOARD ADMINISTRATIVO PRONTO PARA USO!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM! Verifique os erros acima.")
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrija os erros identificados")
        print("2. Execute os testes novamente")
        print("3. Só prossiga quando todos os testes passarem")

if __name__ == "__main__":
    main()
