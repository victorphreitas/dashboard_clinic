                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            """
Script para popular o banco de dados com dados iniciais.
Cria um usuário administrador e dados de exemplo para uma clínica.
"""

import pandas as pd
from database import db_manager, cliente_crud, dados_crud

def create_admin_user():
    """Cria usuário administrador"""
    admin = cliente_crud.create_cliente(
        nome="Administrador",
        email="admin@prestigeclinic.com",
        senha="admin123",
        cnpj="12.345.678/0001-90",
        nome_da_clinica="Prestige Clinic - Administração",
        telefone="(11) 99999-9999",
        endereco="Rua das Clínicas, 123 - São Paulo/SP",
        is_admin=True
    )
    
    if admin:
        print("✅ Usuário administrador criado com sucesso!")
        print(f"   Email: admin@prestigeclinic.com")
        print(f"   Senha: admin123")
    else:
        print("❌ Erro ao criar usuário administrador")
    
    return admin

def create_sample_clinic():
    """Cria uma clínica de exemplo"""
    clinic = cliente_crud.create_cliente(
        nome="Dr. João Silva",
        email="joao@clinicaestetica.com",
        senha="clinica123",
        cnpj="98.765.432/0001-10",
        nome_da_clinica="Clínica Estética Dr. João",
        telefone="(11) 88888-8888",
        endereco="Av. Paulista, 1000 - São Paulo/SP"
    )
    
    if clinic:
        print("✅ Clínica de exemplo criada com sucesso!")
        print(f"   Email: joao@clinicaestetica.com")
        print(f"   Senha: clinica123")
    else:
        print("❌ Erro ao criar clínica de exemplo")
    
    return clinic

def create_dra_taynah_clinic():
    """Cria a clínica Dra Taynah Bastos"""
    clinic = cliente_crud.create_cliente(
        nome="Dra Taynah Bastos",
        email="taynah@cirurgiaplastica.com",
        senha="taynah2024",
        cnpj="11.222.333/0001-44",
        nome_da_clinica="Dra Taynah Bastos (Cirurgia Plástica)",
        telefone="(11) 77777-7777",
        endereco="Rua das Cirurgias, 456 - São Paulo/SP"
    )
    
    if clinic:
        print("✅ Clínica Dra Taynah Bastos criada com sucesso!")
        print(f"   Email: taynah@cirurgiaplastica.com")
        print(f"   Senha: taynah2024")
    else:
        print("❌ Erro ao criar clínica Dra Taynah Bastos")
    
    return clinic

def load_sample_data(cliente_id):
    """Carrega dados de exemplo do CSV"""
    try:
        # Lê dados do CSV
        df = pd.read_csv('data/seed_data.csv')
        
        print(f"📊 Carregando dados para cliente ID: {cliente_id}")
        
        for _, row in df.iterrows():
            if row['leads_totais'] > 0:  # Só carrega meses com atividade
                dados = dados_crud.create_dados_dashboard(
                    cliente_id=cliente_id,
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
                    print(f"   ✅ Dados de {row['mes']} carregados")
                else:
                    print(f"   ❌ Erro ao carregar dados de {row['mes']}")
        
        print("✅ Dados de exemplo carregados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")

def main():
    """Função principal do script de seed"""
    print("🌱 Iniciando população do banco de dados...")
    
    # Cria tabelas
    db_manager.create_tables()
    print("✅ Tabelas criadas")
    
    # Cria usuário administrador
    admin = create_admin_user()
    
    # Cria clínica de exemplo
    clinic = create_sample_clinic()
    
    if clinic:
        # Carrega dados para a clínica de exemplo
        load_sample_data(clinic.id)
    
    # Cria clínica Dra Taynah Bastos
    dra_taynah = create_dra_taynah_clinic()
    
    print("\n🎉 Banco de dados populado com sucesso!")
    print("\n📋 Credenciais de acesso:")
    print("   👑 Administrador:")
    print("      Email: admin@prestigeclinic.com")
    print("      Senha: admin123")
    print("   🏥 Clínica de Exemplo:")
    print("      Email: joao@clinicaestetica.com")
    print("      Senha: clinica123")
    print("   🏥 Dra Taynah Bastos (Cirurgia Plástica):")
    print("      Email: taynah@cirurgiaplastica.com")
    print("      Senha: taynah2024")

if __name__ == "__main__":
    main()

