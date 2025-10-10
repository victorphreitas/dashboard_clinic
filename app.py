# app.py
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from database import db_manager, cliente_crud, dados_crud
from auth import AuthManager, show_auth_page, show_logout_button, show_admin_panel, show_admin_register_clinic_form, show_clinic_management_panel
from dashboard import (
    create_executive_summary, create_kpi_cards, create_funnel_analysis, create_revenue_analysis,
    create_channel_analysis, create_cost_analysis, create_monthly_trends,
    create_insights_section, load_data_from_database, create_conversion_analysis, create_budget_analysis,
    create_admin_consolidated_dashboard
)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
SECRET_KEY = os.getenv('SECRET_KEY', 'chave_padrao_para_desenvolvimento')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///prestige_clinic.db')
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', '{}')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

st.set_page_config(page_title="Dashboard Clínica Estética", layout="wide", page_icon="🏥")

# Inicializa o banco de dados
@st.cache_resource
def init_database():
    """Inicializa o banco de dados e cria as tabelas"""
    db_manager.create_tables()
    return True

# Inicializa o banco na primeira execução
init_database()

def main_dashboard():
    """Função principal do dashboard"""
    auth = AuthManager()
    
    # Verifica autenticação
    if not auth.is_authenticated():
        show_auth_page()
        return
    
    # Obtém dados do usuário atual
    user = auth.get_current_user()
    
    # Determina qual cliente visualizar (admin pode escolher)
    cliente_id = auth.get_cliente_id()
    if auth.is_admin():
        selected_cliente_id = show_admin_panel()
        if selected_cliente_id == 'admin_register':
            # Mostrar formulário de cadastro de clínica
            show_admin_register_clinic_form()
            return
        elif selected_cliente_id == 'clinic_management':
            # Mostrar painel de gerenciamento de clínicas
            show_clinic_management_panel()
            return
        elif selected_cliente_id == 'admin_dashboard':
            # Mostrar dashboard consolidado do administrador
            create_admin_consolidated_dashboard()
            return
        elif selected_cliente_id:
            cliente_id = selected_cliente_id
    
    # Informações de última atualização
    dados = dados_crud.get_dados_by_cliente(cliente_id)
    if dados:
        ultima_atualizacao = max([d.data_criacao for d in dados])
        st.info(f"📅 Última atualização: {ultima_atualizacao.strftime('%d/%m/%Y às %H:%M')}")
    
    # Botão de atualização de dados
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Atualizar Dados do Google Sheets", type="primary", use_container_width=True):
            with st.spinner("🔄 Sincronizando dados do Google Sheets..."):
                try:
                    # Usa script de sincronização inteligente
                    import subprocess
                    import sys
                    import os
                    
                    result = subprocess.run([sys.executable, "sync_sheets.py"], 
                                          capture_output=True, text=True, cwd=".", timeout=60)
                    
                    if result.returncode == 0:
                        st.success("✅ Dados sincronizados com sucesso!")
                        st.info("🔄 Recarregue a página para ver os dados atualizados")
                        
                        # Mostra resumo da sincronização
                        if "sincronizada!" in result.stdout:
                            lines = result.stdout.split('\n')
                            for line in lines:
                                if "sincronizada!" in line:
                                    st.info(f"📊 {line}")
                                    break
                    else:
                        st.error(f"❌ Erro ao sincronizar dados (código {result.returncode})")
                        if result.stderr:
                            st.error(f"Detalhes do erro: {result.stderr}")
                        st.code(result.stdout)
                except subprocess.TimeoutExpired:
                    st.error("⏰ Timeout: A sincronização demorou muito para responder")
                except Exception as e:
                    st.error(f"❌ Erro ao executar sincronização: {e}")
                    st.write(f"Tipo do erro: {type(e).__name__}")
    
    # Carrega dados do banco
    df = load_data_from_database(cliente_id)
    
    if df.empty:
        st.warning("Nenhum dado encontrado para esta clínica. Entre em contato com o suporte.")
        return
    
    # Título do dashboard
    st.title("🏥 Dashboard Clínica de Estética - Análise de Performance")
    
    # Se for admin, mostra o nome da clínica selecionada
    if auth.is_admin() and cliente_id != auth.get_cliente_id():
        cliente_selecionado = cliente_crud.get_cliente_by_id(cliente_id)
        if cliente_selecionado:
            st.markdown(f"**Clínica:** {cliente_selecionado.nome_da_clinica}")
        else:
            st.markdown(f"**Clínica:** {user['nome_da_clinica']}")
    else:
        st.markdown(f"**Clínica:** {user['nome_da_clinica']}")
    
    st.markdown("Análise completa do funil de vendas, performance por canal e métricas financeiras")
    
    # Filtros na barra lateral
    st.sidebar.title("Filtros de Período")
    
    # Meses ativos disponíveis para seleção
    meses_ativos = df[(df['Leads_Totais'] > 0) | (df['Faturamento'] > 0) | (df['Valor_Investido_Total'] > 0)]['Meses'].tolist()
    
    if not meses_ativos:
        st.error("Nenhum dado ativo encontrado para esta clínica.")
        return
    
    # Opção para selecionar um ou mais meses
    meses_selecionados = st.sidebar.multiselect(
        "Selecione o(s) Mês(es) para Análise",
        options=meses_ativos,
        default=meses_ativos  # Seleciona todos os meses ativos por padrão
    )
    
    # Aplica o filtro
    df_filtrado = df[df['Meses'].isin(meses_selecionados)]
    
    # Garante que o DataFrame não está vazio
    if df_filtrado.empty:
        st.error("Nenhum dado encontrado para os meses selecionados. Por favor, ajuste o filtro na barra lateral.")
        return
    
    # Cria as seções do dashboard, passando o DataFrame filtrado
    create_executive_summary(df_filtrado)
    st.markdown("---")
    create_kpi_cards(df_filtrado)
    st.markdown("---")
    
    # Novas análises do formato atualizado
    create_conversion_analysis(df_filtrado)
    st.markdown("---")
    create_budget_analysis(df_filtrado)
    st.markdown("---")
    
    # Análises existentes
    create_funnel_analysis(df_filtrado)
    st.markdown("---")
    create_revenue_analysis(df_filtrado)
    st.markdown("---")
    create_channel_analysis(df_filtrado)
    st.markdown("---")
    create_cost_analysis(df_filtrado)
    st.markdown("---")
    create_monthly_trends(df_filtrado)
    st.markdown("---")
    create_insights_section(df_filtrado)

def main():
    """Função principal da aplicação"""
    # Exibe botão de logout na sidebar
    show_logout_button()
    
    # Executa o dashboard principal
    main_dashboard()

if __name__ == "__main__":
    main()