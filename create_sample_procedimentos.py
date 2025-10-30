"""
Script de teste para importar dados de procedimentos de exemplo.
"""

from database import db_manager, cliente_crud, procedimento_crud
from datetime import datetime
import pandas as pd

def create_sample_procedimentos():
    """Cria dados de exemplo de procedimentos"""
    print("🔄 Criando dados de exemplo de procedimentos...")
    
    # Busca a clínica da Marília (ID 4) ou a primeira clínica ativa (não admin)
    clientes = cliente_crud.get_all_clientes()
    
    # Tenta encontrar a clínica da Marília primeiro
    cliente_marilia = None
    for c in clientes:
        if c.id == 4 and not c.is_admin and c.ativo:
            cliente_marilia = c
            break
    
    if cliente_marilia:
        cliente = cliente_marilia
        print(f"📊 Criando procedimentos para: {cliente.nome_da_clinica} (ID: {cliente.id})")
    else:
        # Se não encontrar a Marília, usa a primeira clínica ativa
        clinicas_ativas = [c for c in clientes if not c.is_admin and c.ativo]
        if not clinicas_ativas:
            print("❌ Nenhuma clínica ativa encontrada")
            return False
        cliente = clinicas_ativas[0]
        print(f"📊 Criando procedimentos para: {cliente.nome_da_clinica} (ID: {cliente.id})")
    
    # Remove procedimentos existentes
    procedimento_crud.delete_procedimentos_by_cliente(cliente.id)
    
    # Dados de exemplo baseados na estrutura fornecida
    sample_procedimentos = [
        {
            'procedimento': 'Mommy Makeover, Lipo HD',
            'tipo': 'Cosmiatria, Cirúrgico',
            'quantidade_na_mesma_venda': 2,
            'forma_pagamento': 'Parcelado no Pix (Financiamento)',
            'valor_da_venda': 20000.00,
            'valor_parcelado': 1000.00,
            'mes_referencia': 'Outubro',
            'ano_referencia': 2024,
            'data_primeiro_contato': datetime(2024, 10, 16),
            'data_compareceu_consulta': datetime(2024, 10, 16),
            'data_fechou_cirurgia': datetime(2024, 10, 16)
        },
        {
            'procedimento': 'Mommy Makeover, Lipo HD, Blefaroplastia',
            'tipo': 'Cosmiatria, Cirúrgico',
            'quantidade_na_mesma_venda': 2,
            'forma_pagamento': 'Parcelado no Pix (Financiamento)',
            'valor_da_venda': 20000.00,
            'valor_parcelado': 1000.00,
            'mes_referencia': 'Outubro',
            'ano_referencia': 2024,
            'data_primeiro_contato': datetime(2024, 10, 16),
            'data_compareceu_consulta': datetime(2024, 10, 16),
            'data_fechou_cirurgia': datetime(2024, 10, 16)
        },
        {
            'procedimento': 'Rinoplastia',
            'tipo': 'Cirúrgico',
            'quantidade_na_mesma_venda': 1,
            'forma_pagamento': 'À vista',
            'valor_da_venda': 15000.00,
            'valor_parcelado': 0.00,
            'mes_referencia': 'Novembro',
            'ano_referencia': 2024,
            'data_primeiro_contato': datetime(2024, 11, 5),
            'data_compareceu_consulta': datetime(2024, 11, 8),
            'data_fechou_cirurgia': datetime(2024, 11, 10)
        },
        {
            'procedimento': 'Lipoaspiração Abdômen',
            'tipo': 'Cirúrgico',
            'quantidade_na_mesma_venda': 1,
            'forma_pagamento': 'Cartão de Crédito',
            'valor_da_venda': 12000.00,
            'valor_parcelado': 2000.00,
            'mes_referencia': 'Novembro',
            'ano_referencia': 2024,
            'data_primeiro_contato': datetime(2024, 11, 12),
            'data_compareceu_consulta': datetime(2024, 11, 15),
            'data_fechou_cirurgia': None  # Ainda não fechou
        },
        {
            'procedimento': 'Botox Facial',
            'tipo': 'Cosmiatria',
            'quantidade_na_mesma_venda': 3,
            'forma_pagamento': 'Dinheiro',
            'valor_da_venda': 3000.00,
            'valor_parcelado': 0.00,
            'mes_referencia': 'Dezembro',
            'ano_referencia': 2024,
            'data_primeiro_contato': datetime(2024, 12, 1),
            'data_compareceu_consulta': datetime(2024, 12, 3),
            'data_fechou_cirurgia': datetime(2024, 12, 3)
        }
    ]
    
    # Insere os procedimentos
    success_count = 0
    for proc_data in sample_procedimentos:
        try:
            procedimento = procedimento_crud.create_procedimento(
                cliente_id=cliente.id,
                **proc_data
            )
            if procedimento:
                success_count += 1
                print(f"✅ Procedimento criado: {proc_data['procedimento']}")
        except Exception as e:
            print(f"❌ Erro ao criar procedimento {proc_data['procedimento']}: {e}")
    
    print(f"🎉 {success_count}/{len(sample_procedimentos)} procedimentos criados com sucesso!")
    return success_count > 0

def main():
    """Função principal"""
    print("🚀 Iniciando criação de dados de exemplo de procedimentos...")
    
    # Cria dados de exemplo
    if create_sample_procedimentos():
        print("✅ Dados de exemplo criados com sucesso!")
        print("📊 Você pode agora visualizar a análise de procedimentos no dashboard")
    else:
        print("❌ Falha ao criar dados de exemplo")

if __name__ == "__main__":
    main()
