"""
Script de teste para importar dados reais de procedimentos da planilha da Marília.
"""

from database import db_manager, cliente_crud, procedimento_crud
from import_procedimentos import load_procedimentos_for_cliente

def test_import_marilia():
    """Testa a importação de procedimentos da Marília"""
    print("🧪 Testando importação de procedimentos da Marília...")
    
    # Busca a clínica da Marília
    clientes = cliente_crud.get_all_clientes()
    cliente_marilia = None
    for c in clientes:
        if c.id == 4 and not c.is_admin and c.ativo:
            cliente_marilia = c
            break
    
    if not cliente_marilia:
        print("❌ Clínica da Marília não encontrada")
        return False
    
    print(f"📊 Clínica encontrada: {cliente_marilia.nome_da_clinica} (ID: {cliente_marilia.id})")
    print(f"🔗 Link da empresa: {cliente_marilia.link_empresa}")
    
    # Verifica quantos procedimentos existem antes
    procedimentos_antes = procedimento_crud.get_procedimentos_by_cliente(cliente_marilia.id)
    print(f"📈 Procedimentos antes da importação: {len(procedimentos_antes)}")
    
    # Executa a importação
    print("\n🔄 Executando importação...")
    success = load_procedimentos_for_cliente(cliente_marilia)
    
    if success:
        # Verifica quantos procedimentos existem depois
        procedimentos_depois = procedimento_crud.get_procedimentos_by_cliente(cliente_marilia.id)
        print(f"📈 Procedimentos depois da importação: {len(procedimentos_depois)}")
        
        # Mostra alguns exemplos
        print("\n📋 Exemplos de procedimentos importados:")
        for i, proc in enumerate(procedimentos_depois[:5]):
            print(f"  {i+1}. {proc.procedimento} - {proc.mes_referencia} - R$ {proc.valor_da_venda:,.2f}")
        
        return True
    else:
        print("❌ Falha na importação")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando teste de importação de procedimentos...")
    
    if test_import_marilia():
        print("\n✅ Teste concluído com sucesso!")
    else:
        print("\n❌ Teste falhou!")

if __name__ == "__main__":
    main()

