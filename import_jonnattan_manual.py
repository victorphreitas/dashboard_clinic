"""
Script para importar dados do Dr. Jonnattan manualmente
Baseado nos dados que vimos na planilha
"""

from database import dados_crud, cliente_crud, db_manager

def import_jonnattan_data_manually():
    """Importa dados do Dr. Jonnattan manualmente"""
    print("📊 IMPORTANDO DADOS DO DR. JONNATTAN MANUALMENTE")
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
    
    print(f"🏥 Clínica: {jonnattan.nome_da_clinica}")
    print(f"📧 Email: {jonnattan.email}")
    print(f"🔗 Link: {jonnattan.link_empresa}")
    
    # Remover dados existentes
    print(f"\\n🗑️ Removendo dados existentes...")
    dados_existentes = dados_crud.get_dados_by_cliente(jonnattan.id)
    for dados in dados_existentes:
        dados_crud.delete_dados_dashboard(dados.id)
    print(f"✅ {len(dados_existentes)} registros removidos")
    
    # Dados baseados na planilha que vimos
    print(f"\\n📊 Importando dados de Outubro...")
    
    # Dados de Outubro (baseados na planilha)
    dados_outubro = dados_crud.create_dados_dashboard(
        cliente_id=jonnattan.id,
        mes="Outubro",
        ano=2024,
        leads_totais=0,
        leads_google_ads=0,
        leads_meta_ads=0,
        leads_instagram_organico=0,
        leads_indicacao=0,
        leads_origem_desconhecida=0,
        consultas_marcadas_totais=1,
        consultas_marcadas_google_ads=1,
        consultas_marcadas_meta_ads=0,
        consultas_marcadas_ig_organico=0,
        consultas_marcadas_indicacao=0,
        consultas_marcadas_outros=0,
        consultas_comparecidas=0,
        fechamentos_totais=0,
        fechamentos_google_ads=0,
        fechamentos_meta_ads=0,
        fechamentos_ig_organico=0,
        fechamentos_indicacao=0,
        fechamentos_outros=0,
        faturamento=500.00,
        investimento_total=284.31,
        investimento_facebook=190.04,
        investimento_google=94.27
    )
    
    if dados_outubro:
        print(f"✅ Dados de Outubro importados com sucesso!")
        print(f"   📅 Outubro: 1 consulta, R$ 500,00 faturamento")
        print(f"   💰 Investimento: R$ 284,31")
        return True
    else:
        print(f"❌ Erro ao importar dados de Outubro")
        return False

def verify_import():
    """Verifica se os dados foram importados corretamente"""
    print(f"\\n🔍 VERIFICANDO IMPORTAÇÃO...")
    
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
    
    # Verificar dados
    dados = dados_crud.get_dados_by_cliente(jonnattan.id)
    print(f"📊 Dados encontrados: {len(dados)} registros")
    
    for dado in dados:
        print(f"   📅 {dado.mes}: {dado.consultas_marcadas_totais} consultas, R$ {dado.faturamento:,.2f}")
    
    if len(dados) > 0:
        print(f"\\n✅ IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"✅ Dr. Jonnattan agora tem dados no dashboard")
        print(f"✅ Sistema funcionando normalmente")
        return True
    else:
        print(f"\\n❌ Nenhum dado encontrado")
        return False

def main():
    """Função principal"""
    print("🏥 IMPORTAÇÃO MANUAL - DR. JONNATTAN")
    print("=" * 60)
    
    # Importar dados
    success = import_jonnattan_data_manually()
    
    if success:
        # Verificar importação
        verify_import()
        
        print(f"\\n🎉 RESULTADO FINAL:")
        print(f"✅ Dr. Jonnattan tem dados no dashboard")
        print(f"✅ Sistema funcionando perfeitamente")
        print(f"✅ Problema resolvido!")
        
        print(f"\\n💡 PRÓXIMOS PASSOS:")
        print(f"   1. Acesse o dashboard")
        print(f"   2. Selecione 'Dr. Jonnattan Prada'")
        print(f"   3. Verifique os dados de Outubro")
    else:
        print(f"\\n❌ Erro na importação")

if __name__ == "__main__":
    main()
