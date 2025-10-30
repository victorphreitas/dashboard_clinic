"""
Módulo de visualizações e análises do dashboard.
Contém todas as funções de criação de gráficos e métricas.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_kpi_cards(df_filtered):
    """Cria cards com KPIs principais"""
    
    df_ativos = df_filtered # Renomeando para manter a lógica interna
    
    st.subheader(f"📊 KPIs Principais - Período Selecionado")
    
    # Filtra apenas meses com atividade (novo formato)
    df_metrics = df_ativos[(df_ativos['Leads_Totais'] > 0) | (df_ativos['Faturamento'] > 0) | (df_ativos['Valor_Investido_Total'] > 0)]
    
    if df_metrics.empty:
        st.warning("Nenhum dado ativo neste período.")
        return
        
    total_leads = df_metrics['Leads_Totais'].sum()
    total_faturamento = df_metrics['Faturamento'].sum()
    total_fechamentos = df_metrics['Fechamentos_Totais'].sum()
    total_investimento = df_metrics['Valor_Investido_Total'].sum()
    total_consultas_marcadas = df_metrics['Consultas_Marcadas_Totais'].sum()
    total_consultas_comparecidas = df_metrics['Consultas_Comparecidas'].sum()
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total de Leads",
            value=f"{total_leads:,.0f}".replace(",", "."),
            delta=f"{df_metrics['Leads_Totais'].mean():.0f} leads/mês"
        )
    
    with col2:
        st.metric(
            label="Faturamento Total",
            value=f"R$ {total_faturamento:,.0f}".replace(",", "."),
            delta=f"R$ {df_metrics['Faturamento'].mean():,.0f}".replace(",", ".") + "/mês"
        )
    
    with col3:
        st.metric(
            label="Fechamentos Realizados",
            value=f"{total_fechamentos}",
            delta=f"{df_metrics['Fechamentos_Totais'].mean():.0f}/mês"
        )
    
    with col4:
        roas_medio = total_faturamento / total_investimento if total_investimento > 0 else 0
        st.metric(
            label="ROAS Médio",
            value=f"{roas_medio:.1f}x",
            delta=f"Investimento: R$ {total_investimento:,.0f}".replace(",", ".")
        )
    
    with col5:
        st.metric(
            label="Consultas Marcadas",
            value=f"{total_consultas_marcadas}",
            delta=f"{df_metrics['Consultas_Marcadas_Totais'].mean():.0f}/mês"
        )
    
    with col6:
        st.metric(
            label="Consultas Comparecidas",
            value=f"{total_consultas_comparecidas}",
            delta=f"{df_metrics['Consultas_Comparecidas'].mean():.0f}/mês"
        )

def create_funnel_analysis(df_filtered):
    """Análise do funil de conversão"""
    st.subheader("🔄 Análise do Funil de Conversão")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Valor_Investido_Total'] > 0)]
    
    if df_ativos.empty:
        st.info("Nenhum Lead registrado no período selecionado.")
        return
        
    # Dados consolidados do funil
    total_leads = df_ativos['Leads_Totais'].sum()
    total_consultas_marcadas = df_ativos['Consultas_Marcadas_Totais'].sum()
    total_consultas_comparecidas = df_ativos['Consultas_Comparecidas'].sum()
    total_fechamentos = df_ativos['Fechamentos_Totais'].sum()
    
    # Taxas de conversão CONSOLIDADAS (corrigindo o erro de usar média simples de percentuais)
    taxa_leads_consulta = (total_consultas_marcadas / total_leads * 100) if total_leads > 0 else 0
    taxa_consulta_comparecida = (total_consultas_comparecidas / total_consultas_marcadas * 100) if total_consultas_marcadas > 0 else 0
    taxa_comparecida_fechamento = (total_fechamentos / total_consultas_comparecidas * 100) if total_consultas_comparecidas > 0 else 0
    taxa_leads_fechamento = (total_fechamentos / total_leads * 100) if total_leads > 0 else 0

    
    # Gráfico de funil usa valores médios para visualização do fluxo, mas os KPIs usam totais.
    fig_funnel = go.Figure(go.Funnel(
        y=["Leads", "Consultas Marcadas", "Consultas Comparecidas", "Fechamentos"],
        x=[df_ativos['Leads_Totais'].mean(), df_ativos['Consultas_Marcadas_Totais'].mean(), 
           df_ativos['Consultas_Comparecidas'].mean(), df_ativos['Fechamentos_Totais'].mean()],
        textinfo="value+percent initial",
        opacity=0.8,
        marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]}
    ))
    
    fig_funnel.update_layout(
        title="Funil de Vendas - Valores Médios Mensais",
        height=400
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(fig_funnel)
    
    with col2:
        st.markdown("### 📈 Taxas de Conversão Consolidadas")
        st.metric("Leads → Consultas", f"{taxa_leads_consulta:.1f}%")
        st.metric("Consultas → Comparecimentos", f"{taxa_consulta_comparecida:.1f}%")
        st.metric("Comparecimentos → Fechamentos", f"{taxa_comparecida_fechamento:.1f}%")
        st.metric("Leads → Fechamentos", f"{taxa_leads_fechamento:.1f}%")

def create_revenue_analysis(df_filtered):
    """Análise de faturamento e investimento"""
    st.subheader("💰 Análise Financeira")
    
    df_ativos = df_filtered[df_filtered['Faturamento'] > 0]
    
    if df_ativos.empty:
        st.info("Nenhum faturamento registrado no período selecionado.")
        return
        
    col1, col2 = st.columns(2)
    
    with col1:
        # Faturamento vs Investimento
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Bar(
            x=df_ativos['Meses'],
            y=df_ativos['Faturamento'],
            name='Faturamento',
            marker_color='#2ca02c'
        ))
        fig_revenue.add_trace(go.Scatter(
            x=df_ativos['Meses'],
            y=df_ativos['Valor_Investido_Total'],
            name='Investimento Total',
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=3),
            yaxis='y2'
        ))
        
        fig_revenue.update_layout(
            title="Faturamento vs Investimento por Mês",
            yaxis=dict(title="Faturamento (R$)"),
            yaxis2=dict(title="Investimento (R$)", overlaying='y', side='right'),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_revenue)
    
    with col2:
        # ROAS e Ticket Médio
        fig_roas = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_roas.add_trace(
            go.Bar(x=df_ativos['Meses'], y=df_ativos['ROAS'], name="ROAS", marker_color='#17becf'),
            secondary_y=False,
        )
        
        fig_roas.add_trace(
            go.Scatter(x=df_ativos['Meses'], y=df_ativos['Ticket_Medio'], 
                      name="Ticket Médio", line=dict(color='#e377c2', width=3)),
            secondary_y=True,
        )
        
        fig_roas.update_layout(
            title="ROAS e Ticket Médio",
            height=400
        )
        
        fig_roas.update_yaxes(title_text="ROAS (x)", secondary_y=False)
        fig_roas.update_yaxes(title_text="Ticket Médio (R$)", secondary_y=True)
        
        st.plotly_chart(fig_roas)

def create_channel_analysis(df_filtered):
    """Análise de performance por canal"""
    st.subheader("📱 Performance por Canal de Aquisição")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Valor_Investido_Total'] > 0)]
    
    if df_ativos.empty:
        st.info("Nenhum dado de Leads disponível no período selecionado.")
        return
        
    # Agrupa dados totais por canal
    channels_data = {
        'Canal': ['Instagram Orgânico', 'Meta Ads', 'Google Ads', 'Indicação', 'Outros'],
        'Leads': [
            df_ativos['Leads_Instagram_Organico'].sum(),
            df_ativos['Leads_Meta_Ads'].sum(),
            df_ativos['Leads_Google_Ads'].sum(),
            df_ativos['Leads_Indicacao'].sum(),
            df_ativos['Leads_Origem_Desconhecida'].sum()
        ],
        'Fechamentos': [
            df_ativos['Fechamentos_IG_Organico'].sum(),
            df_ativos['Fechamentos_Meta_Ads'].sum(),
            df_ativos['Fechamentos_Google_Ads'].sum(),
            df_ativos['Fechamentos_Indicacao'].sum(),
            df_ativos['Fechamentos_Outros'].sum()
        ]
    }
    
    channels_df = pd.DataFrame(channels_data)
    # Recalculando Taxa de Conversão Consolidada
    channels_df['Taxa_Conversao'] = np.where(channels_df['Leads'] != 0, 
                                            (channels_df['Fechamentos'] / channels_df['Leads'] * 100), 0).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Leads por canal
        fig_leads = px.pie(
            channels_df, 
            values='Leads', 
            names='Canal',
            title='Distribuição de Leads por Canal',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_leads)
    
    with col2:
        # Taxa de conversão por canal
        fig_conversion = px.bar(
            channels_df,
            x='Canal',
            y='Taxa_Conversao',
            title='Taxa de Conversão por Canal (%)',
            color='Taxa_Conversao',
            color_continuous_scale='Viridis',
            text_auto='.1f' 
        )
        fig_conversion.update_layout(showlegend=False)
        st.plotly_chart(fig_conversion)

def create_cost_analysis(df_filtered):
    """Análise de custos e eficiência"""
    st.subheader("💸 Análise de Custos e Eficiência")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Valor_Investido_Total'] > 0)]
    
    if df_ativos.empty:
        st.info("Nenhum dado ativo para análise de custos no período selecionado.")
        return
        
    col1, col2, col3 = st.columns(3)
    
    # CPL Médio (ignorando zeros/indefinidos)
    cpl_medio = df_ativos['Custo_por_Lead_Total'].replace(0, np.nan).mean()
    cpl_min = df_ativos['Custo_por_Lead_Total'].replace(0, np.nan).min()
    with col1:
        st.metric(
            "Custo por Lead Médio",
            f"R$ {cpl_medio:.2f}" if not pd.isna(cpl_medio) else "N/A",
            delta=f"Menor: R$ {cpl_min:.2f}" if not pd.isna(cpl_min) else "N/A"
        )
    
    # CPA Médio (ignorando zeros/indefinidos)
    cpa_medio = df_ativos['Custo_por_Compra_Cirurgias'].replace(0, np.nan).mean()
    cpa_min = df_ativos['Custo_por_Compra_Cirurgias'].replace(0, np.nan).min()
    with col2:
        st.metric(
            "Custo por Compra Médio",
            f"R$ {cpa_medio:.2f}" if not pd.isna(cpa_medio) else "N/A",
            delta=f"Melhor: R$ {cpa_min:.2f}" if not pd.isna(cpa_min) else "N/A"
        )
    
    # Ticket Médio (ignorando zeros/indefinidos)
    ticket_medio_geral = df_ativos['Ticket_Medio'].replace(0, np.nan).mean()
    ticket_max = df_ativos['Ticket_Medio'].max()
    with col3:
        st.metric(
            "Ticket Médio",
            value=f"R$ {ticket_medio_geral:,.0f}".replace(",", ".") if not pd.isna(ticket_medio_geral) else "N/A", 
            delta=f"Maior: R$ {ticket_max:,.0f}".replace(",", ".")
        )
    
    # Evolução dos custos
    fig_costs = go.Figure()
    
    fig_costs.add_trace(go.Scatter(
        x=df_ativos['Meses'], y=df_ativos['Custo_por_Lead_Total'],
        name='Custo por Lead', line=dict(color='#1f77b4', width=3)
    ))
    
    fig_costs.add_trace(go.Scatter(
        x=df_ativos['Meses'], y=df_ativos['Custo_por_Compra_Cirurgias'],
        name='Custo por Compra', line=dict(color='#ff7f0e', width=3)
    ))
    
    fig_costs.add_trace(go.Scatter(
        x=df_ativos['Meses'], y=df_ativos['Custo_por_Consulta_Marcada'],
        name='Custo por Consulta Marcada', line=dict(color='#2ca02c', width=3)
    ))
    
    fig_costs.update_layout(
        title="Evolução dos Custos por Mês",
        yaxis_title="Custo (R$)",
        height=400
    )
    
    st.plotly_chart(fig_costs)

def create_monthly_trends(df_filtered):
    """Tendências mensais e sazonais"""
    st.subheader("📈 Tendências e Sazonalidade")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Valor_Investido_Total'] > 0)]
    
    if df_ativos.empty:
        st.info("Nenhum dado ativo para tendências no período selecionado.")
        return
        
    fig_trends = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Leads Totais', 'Faturamento Mensal', 'Consultas Comparecidas', 'Fechamentos'),
        vertical_spacing=0.12
    )
    
    # Leads
    fig_trends.add_trace(
        go.Bar(x=df_ativos['Meses'], y=df_ativos['Leads_Totais'], name="Leads"),
        row=1, col=1
    )
    
    # Faturamento
    fig_trends.add_trace(
        go.Bar(x=df_ativos['Meses'], y=df_ativos['Faturamento'], name="Faturamento"),
        row=1, col=2
    )
    
    # Consultas Comparecidas
    fig_trends.add_trace(
        go.Bar(x=df_ativos['Meses'], y=df_ativos['Consultas_Comparecidas'], name="Consultas Comparecidas"),
        row=2, col=1
    )
    
    # Fechamentos
    fig_trends.add_trace(
        go.Bar(x=df_ativos['Meses'], y=df_ativos['Fechamentos_Totais'], name="Fechamentos"),
        row=2, col=2
    )
    
    fig_trends.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_trends)

def create_conversion_analysis(df_filtered):
    """Cria análise de conversão com novos KPIs"""
    st.subheader("🔄 Análise de Conversão - Novo Formato")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Valor_Investido_Total'] > 0)]
    
    if df_ativos.empty:
        st.warning("Nenhum dado ativo para análise de conversão.")
        return
    
    # KPIs de conversão
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcular conversões usando totais (não média de percentuais)
    total_leads = df_ativos['Leads_Totais'].sum()
    total_consultas_marcadas = df_ativos['Consultas_Marcadas_Totais'].sum()
    total_consultas_comparecidas = df_ativos['Consultas_Comparecidas'].sum()
    total_fechamentos = df_ativos['Fechamentos_Totais'].sum()
    
    # Conversões calculadas corretamente
    conversao_csm_leads = (total_consultas_marcadas / total_leads * 100) if total_leads > 0 else 0
    conversao_csc_csm = (total_consultas_comparecidas / total_consultas_marcadas * 100) if total_consultas_marcadas > 0 else 0
    conversao_fechamento_csc = (total_fechamentos / total_consultas_comparecidas * 100) if total_consultas_comparecidas > 0 else 0
    conversao_fechamento_leads = (total_fechamentos / total_leads * 100) if total_leads > 0 else 0
    
    with col1:
        st.metric(
            label="% Conversão Csm./Leads",
            value=f"{conversao_csm_leads:.1f}%",
            help="% de leads que se tornaram consultas marcadas"
        )
    
    with col2:
        st.metric(
            label="% Conversão Csc./Csm.",
            value=f"{conversao_csc_csm:.1f}%",
            help="% de consultas marcadas que compareceram"
        )
    
    with col3:
        st.metric(
            label="% Conversão Fechamento/Csc.",
            value=f"{conversao_fechamento_csc:.1f}%",
            help="% de consultas comparecidas que viraram fechamentos"
        )
    
    with col4:
        st.metric(
            label="% Conversão Fechamento/Leads",
            value=f"{conversao_fechamento_leads:.1f}%",
            help="% de leads que viraram fechamentos"
        )
    
    # Taxas ideais vs reais
    st.markdown("### 📊 Taxas Ideais vs Reais")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        taxa_ideal_csm = 10.0
        taxa_real_csm = conversao_csm_leads
        status_csm = "🟢" if taxa_real_csm >= taxa_ideal_csm else "🔴"
        st.metric(
            label=f"{status_csm} Consultas Marcadas",
            value=f"{taxa_real_csm:.1f}%",
            delta=f"Meta: {taxa_ideal_csm}%",
            help="Taxa ideal: >10%"
        )
    
    with col2:
        taxa_ideal_csc = 50.0
        taxa_real_csc = conversao_csc_csm
        status_csc = "🟢" if taxa_real_csc >= taxa_ideal_csc else "🔴"
        st.metric(
            label=f"{status_csc} Consultas Comparecidas",
            value=f"{taxa_real_csc:.1f}%",
            delta=f"Meta: {taxa_ideal_csc}%",
            help="Taxa ideal: >50%"
        )
    
    with col3:
        taxa_ideal_fechamentos = 40.0
        taxa_real_fechamentos = conversao_fechamento_csc
        status_fechamentos = "🟢" if taxa_real_fechamentos >= taxa_ideal_fechamentos else "🔴"
        st.metric(
            label=f"{status_fechamentos} Fechamentos",
            value=f"{taxa_real_fechamentos:.1f}%",
            delta=f"Meta: {taxa_ideal_fechamentos}%",
            help="Taxa ideal: >40%"
        )

def create_budget_analysis(df_filtered):
    """Cria análise de orçamento com novos campos"""
    st.subheader("💰 Análise de Orçamento - Novo Formato")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Valor_Investido_Total'] > 0)]
    
    if df_ativos.empty:
        st.warning("Nenhum dado ativo para análise de orçamento.")
        return
    
    # Resumo de orçamento
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        orcamento_previsto_total = df_ativos['Orcamento_Previsto_Total'].sum()
        st.metric(
            label="Orçamento Previsto Total",
            value=f"R$ {orcamento_previsto_total:,.0f}".replace(",", "."),
            help="Orçamento total planejado"
        )
    
    with col2:
        valor_investido_total = df_ativos['Valor_Investido_Total'].sum()
        st.metric(
            label="Valor Investido Total",
            value=f"R$ {valor_investido_total:,.0f}".replace(",", "."),
            help="Valor total realmente investido"
        )
    
    with col3:
        orcamento_facebook = df_ativos['Orcamento_Realizado_Facebook'].sum()
        st.metric(
            label="Facebook Ads (Realizado)",
            value=f"R$ {orcamento_facebook:,.0f}".replace(",", "."),
            help="Investimento realizado no Facebook"
        )
    
    with col4:
        orcamento_google = df_ativos['Orcamento_Realizado_Google'].sum()
        st.metric(
            label="Google Ads (Realizado)",
            value=f"R$ {orcamento_google:,.0f}".replace(",", "."),
            help="Investimento realizado no Google"
        )
    
    # Gráfico de orçamento vs realizado
    if len(df_ativos) > 1:
        fig_budget = go.Figure()
        
        fig_budget.add_trace(go.Bar(
            x=df_ativos['Meses'],
            y=df_ativos['Orcamento_Previsto_Total'],
            name='Orçamento Previsto',
            marker_color='#1f77b4'
        ))
        
        fig_budget.add_trace(go.Bar(
            x=df_ativos['Meses'],
            y=df_ativos['Valor_Investido_Total'],
            name='Valor Investido',
            marker_color='#ff7f0e'
        ))
        
        fig_budget.update_layout(
            title="Orçamento Previsto vs Valor Investido",
            xaxis_title="Meses",
            yaxis_title="Valor (R$)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_budget)

def create_admin_consolidated_dashboard():
    """Cria dashboard consolidado para administrador"""
    from database import admin_dashboard_crud, cliente_crud
    from styles import apply_modern_styles, create_modern_header, create_metric_card, create_modern_button, create_modern_alert
    
    # Aplicar estilos modernos
    apply_modern_styles()
    
    # Buscar nome do administrador
    admin_user = cliente_crud.get_cliente_by_id(st.session_state.get('cliente_id'))
    admin_name = admin_user.nome if admin_user else "Administrador"
    
    # Header moderno com nome do administrador
    create_modern_header(
        f"Dashboard - {admin_name}", 
        "Visão consolidada de todas as clínicas"
    )
    
    # Botões de navegação modernos
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if create_modern_button("Nova Clínica", "nav_nova_from_dashboard", "secondary"):
            st.session_state['show_admin_register'] = True
            st.session_state['show_admin_dashboard'] = False
            st.rerun()
    
    with col_nav2:
        if create_modern_button("Gerenciar Clínicas", "nav_gerenciar_from_dashboard", "secondary"):
            st.session_state['show_clinic_management'] = True
            st.session_state['show_admin_dashboard'] = False
            st.rerun()
    
    with col_nav3:
        if create_modern_button("Ver Clínicas", "nav_ver_from_dashboard", "secondary"):
            st.session_state['show_admin_dashboard'] = False
            st.rerun()
    
    # Filtros de período
    st.sidebar.title("Filtros de Período")
    st.sidebar.markdown("**Selecione o(s) Mês(es) para Análise**")
    
    # Lista de meses disponíveis
    meses_disponiveis = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    # Filtro de meses (múltipla seleção)
    meses_selecionados = st.sidebar.multiselect(
        "Meses:",
        options=meses_disponiveis,
        default=meses_disponiveis,  # Todos os meses por padrão
        key="admin_meses_filter"
    )
    
    # Busca dados filtrados por meses selecionados
    from database import dados_crud
    
    # Busca todos os dados de todas as clínicas
    all_data = []
    clientes = cliente_crud.get_all_clientes()
    for cliente in clientes:
        if not cliente.is_admin and cliente.ativo:
            dados_cliente = dados_crud.get_dados_by_cliente(cliente.id)
            if dados_cliente:
                df_cliente = dados_crud.dados_to_dataframe(dados_cliente)
                # Filtra pelos meses selecionados
                df_filtrado = df_cliente[df_cliente['Meses'].isin(meses_selecionados)]
                if not df_filtrado.empty:
                    all_data.append(df_filtrado)
    
    if not all_data:
        create_modern_alert("Nenhuma clínica ativa encontrada para exibir métricas consolidadas.", "warning")
        return
    
    # Concatena todos os dados filtrados
    import pandas as pd
    df_consolidado = pd.concat(all_data, ignore_index=True)
    
    # Calcula métricas consolidadas filtradas
    metrics = {
        'total_leads': df_consolidado['Leads_Totais'].sum(),
        'total_consultas_marcadas': df_consolidado['Consultas_Marcadas_Totais'].sum(),
        'total_consultas_comparecidas': df_consolidado['Consultas_Comparecidas'].sum(),
        'total_fechamentos': df_consolidado['Fechamentos_Totais'].sum(),
        'total_faturamento': df_consolidado['Faturamento'].sum(),
        'total_investimento': df_consolidado['Valor_Investido_Total'].sum(),
        'roas_medio': (df_consolidado['Faturamento'].sum() / df_consolidado['Valor_Investido_Total'].sum()) if df_consolidado['Valor_Investido_Total'].sum() > 0 else 0,
        'custo_por_lead_medio': (df_consolidado['Valor_Investido_Total'].sum() / df_consolidado['Leads_Totais'].sum()) if df_consolidado['Leads_Totais'].sum() > 0 else 0,
        'ticket_medio': (df_consolidado['Faturamento'].sum() / df_consolidado['Fechamentos_Totais'].sum()) if df_consolidado['Fechamentos_Totais'].sum() > 0 else 0,
        'clinicas_ativas': len(set(df_consolidado['Cliente_ID'])),
        'meses_ativos': len(set(df_consolidado['Meses']))
    }
    
    # KPIs principais consolidados com design moderno
    st.markdown("### Métricas Principais")
    
    # Primeira linha de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            value=f"{metrics['total_leads']:,.0f}".replace(",", "."),
            label="Total de Leads"
        )
    
    with col2:
        create_metric_card(
            value=f"R$ {metrics['total_faturamento']:,.0f}".replace(",", "."),
            label="Faturamento Total"
        )
    
    with col3:
        create_metric_card(
            value=f"{metrics['roas_medio']:.1f}x",
            label="ROAS Médio"
        )
    
    with col4:
        create_metric_card(
            value=f"{metrics['clinicas_ativas']}",
            label="Clínicas Ativas"
        )
    
    # Segunda linha de métricas
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        create_metric_card(
            value=f"{metrics['total_consultas_marcadas']:,.0f}".replace(",", "."),
            label="Consultas Marcadas"
        )
    
    with col6:
        create_metric_card(
            value=f"{metrics['total_fechamentos']:,.0f}".replace(",", "."),
            label="Fechamentos"
        )
    
    with col7:
        create_metric_card(
            value=f"R$ {metrics['custo_por_lead_medio']:,.0f}".replace(",", "."),
            label="Custo por Lead Médio"
        )
    
    with col8:
        create_metric_card(
            value=f"R$ {metrics['ticket_medio']:,.0f}".replace(",", "."),
            label="Ticket Médio"
        )
    
    # Gráfico de evolução mensal consolidada
    st.subheader("📈 Evolução Mensal Consolidada")
    
    monthly_data = admin_dashboard_crud.get_monthly_evolution()
    if monthly_data:
        df_monthly = pd.DataFrame(monthly_data)
        
        # Ordena os meses corretamente
        mes_order = {
            'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
            'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
            'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
        }
        df_monthly['mes_order'] = df_monthly['mes'].map(mes_order)
        df_monthly = df_monthly.sort_values(['ano', 'mes_order']).drop('mes_order', axis=1)
        
        # Cria gráfico de evolução
        fig_evolution = go.Figure()
        
        fig_evolution.add_trace(go.Scatter(
            x=df_monthly['mes'] + ' ' + df_monthly['ano'].astype(str),
            y=df_monthly['total_leads'],
            name='Leads',
            line=dict(color='#1f77b4', width=3)
        ))
        
        fig_evolution.add_trace(go.Scatter(
            x=df_monthly['mes'] + ' ' + df_monthly['ano'].astype(str),
            y=df_monthly['total_faturamento'],
            name='Faturamento',
            line=dict(color='#2ca02c', width=3),
            yaxis='y2'
        ))
        
        fig_evolution.update_layout(
            title="Evolução Mensal - Leads e Faturamento",
            xaxis_title="Meses",
            yaxis_title="Leads",
            yaxis2=dict(title="Faturamento (R$)", overlaying="y", side="right"),
            height=400
        )
        
        st.plotly_chart(fig_evolution)
    else:
        st.info("Nenhum dado mensal encontrado para exibir evolução.")
    
    st.markdown("---")
    
    # Comparativo entre clínicas
    st.subheader("🏥 Comparativo entre Clínicas")
    
    clinics_data = admin_dashboard_crud.get_clinics_comparison()
    if clinics_data:
        df_clinics = pd.DataFrame(clinics_data)
        
        # Gráfico de barras comparativo - Leads vs Fechamentos (escalas similares)
        fig_comparison = go.Figure()
        
        fig_comparison.add_trace(go.Bar(
            x=df_clinics['nome_da_clinica'],
            y=df_clinics['total_leads'],
            name='Leads',
            marker_color='#3B82F6',
            text=df_clinics['total_leads'],
            textposition='auto'
        ))
        
        fig_comparison.add_trace(go.Bar(
            x=df_clinics['nome_da_clinica'],
            y=df_clinics['total_fechamentos'],
            name='Fechamentos',
            marker_color='#10B981',
            text=df_clinics['total_fechamentos'],
            textposition='auto'
        ))
        
        fig_comparison.update_layout(
            title="Comparativo de Performance entre Clínicas",
            xaxis_title="Clínicas",
            yaxis_title="Quantidade",
            barmode='group',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig_comparison)
        
        # Gráfico de faturamento separado
        st.markdown("### 💰 Faturamento por Clínica")
        fig_faturamento = go.Figure()
        
        fig_faturamento.add_trace(go.Bar(
            x=df_clinics['nome_da_clinica'],
            y=df_clinics['total_faturamento'],
            name='Faturamento',
            marker_color='#F59E0B',
            text=[f"R$ {x:,.0f}".replace(",", ".") for x in df_clinics['total_faturamento']],
            textposition='auto'
        ))
        
        fig_faturamento.update_layout(
            title="Faturamento Total por Clínica",
            xaxis_title="Clínicas",
            yaxis_title="Faturamento (R$)",
            height=400
        )
        
        st.plotly_chart(fig_faturamento)
        
        # Tabela de ranking
        st.markdown("### 🏆 Ranking de Performance")
        
        # Calcula ranking por faturamento
        df_clinics_ranking = df_clinics.sort_values('total_faturamento', ascending=False)
        
        col_ranking1, col_ranking2 = st.columns(2)
        
        with col_ranking1:
            st.markdown("**💰 Ranking por Faturamento**")
            for i, (_, row) in enumerate(df_clinics_ranking.iterrows(), 1):
                st.write(f"{i}º **{row['nome_da_clinica']}** - R$ {row['total_faturamento']:,.0f}".replace(",", "."))
        
        with col_ranking2:
            st.markdown("**📊 Ranking por Leads**")
            df_leads_ranking = df_clinics.sort_values('total_leads', ascending=False)
            for i, (_, row) in enumerate(df_leads_ranking.iterrows(), 1):
                st.write(f"{i}º **{row['nome_da_clinica']}** - {row['total_leads']:,.0f} leads".replace(",", "."))
    else:
        st.info("Nenhum dado de clínicas encontrado para comparação.")
    
    st.markdown("---")
    
    # Análise por canal
    st.subheader("📊 Análise por Canal de Marketing")
    
    channel_data = admin_dashboard_crud.get_channel_analysis()
    if channel_data:
        # Gráfico de pizza para leads por canal
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Google Ads', 'Meta Ads', 'Instagram Orgânico', 'Indicação', 'Origem Desconhecida'],
            values=[
                channel_data['leads_google'],
                channel_data['leads_meta'],
                channel_data['leads_instagram'],
                channel_data['leads_indicacao'],
                channel_data['leads_desconhecida']
            ],
            hole=0.3
        )])
        
        fig_pie.update_layout(
            title="Distribuição de Leads por Canal",
            height=400
        )
        
        st.plotly_chart(fig_pie)
        
        # Gráfico de investimento vs retorno
        fig_investment = go.Figure()
        
        fig_investment.add_trace(go.Bar(
            x=['Google Ads', 'Meta Ads'],
            y=[channel_data['investimento_google'], channel_data['investimento_facebook']],
            name='Investimento',
            marker_color='#ff7f0e'
        ))
        
        fig_investment.update_layout(
            title="Investimento por Canal",
            xaxis_title="Canal",
            yaxis_title="Valor Investido (R$)",
            height=300
        )
        
        st.plotly_chart(fig_investment)
    else:
        st.info("Nenhum dado de canais encontrado para análise.")
    
    st.markdown("---")
    
    # Análise de Procedimentos Consolidada
    st.subheader("🏥 Análise de Procedimentos Consolidada")
    
    # Busca dados de procedimentos de todas as clínicas
    from database import procedimento_crud
    
    all_procedimentos_data = []
    for cliente in clientes:
        if not cliente.is_admin and cliente.ativo:
            procedimentos = procedimento_crud.get_procedimentos_by_cliente(cliente.id)
            if procedimentos:
                df_procedimentos = procedimento_crud.procedimentos_to_dataframe(procedimentos)
                # Filtra pelos meses selecionados
                if 'Mes_Referencia' in df_procedimentos.columns:
                    df_procedimentos_filtrado = df_procedimentos[df_procedimentos['Mes_Referencia'].isin(meses_selecionados)]
                    if not df_procedimentos_filtrado.empty:
                        df_procedimentos_filtrado['Cliente_ID'] = cliente.id
                        df_procedimentos_filtrado['Nome_Clinica'] = cliente.nome_da_clinica
                        all_procedimentos_data.append(df_procedimentos_filtrado)
    
    if all_procedimentos_data:
        # Concatena todos os dados de procedimentos
        df_procedimentos_consolidado = pd.concat(all_procedimentos_data, ignore_index=True)
        
        # Calcula métricas consolidadas de procedimentos
        procedimentos_metrics = {
            'total_procedimentos': len(df_procedimentos_consolidado),
            'total_faturamento_procedimentos': df_procedimentos_consolidado['Valor_da_Venda'].sum(),
            'ticket_medio_procedimentos': df_procedimentos_consolidado['Valor_da_Venda'].mean(),
            'procedimentos_fechados': len(df_procedimentos_consolidado[df_procedimentos_consolidado['Data_Fechou_Cirurgia'].notna()]),
            'clinicas_com_procedimentos': len(set(df_procedimentos_consolidado['Cliente_ID'])),
            'procedimentos_por_clinica': len(df_procedimentos_consolidado) / len(set(df_procedimentos_consolidado['Cliente_ID'])) if len(set(df_procedimentos_consolidado['Cliente_ID'])) > 0 else 0
        }
        
        # KPIs de procedimentos
        st.markdown("### 📊 Métricas de Procedimentos")
        
        col_proc1, col_proc2, col_proc3, col_proc4 = st.columns(4)
        
        with col_proc1:
            create_metric_card(
                value=f"{procedimentos_metrics['total_procedimentos']:,.0f}".replace(",", "."),
                label="Total de Procedimentos"
            )
        
        with col_proc2:
            create_metric_card(
                value=f"R$ {procedimentos_metrics['total_faturamento_procedimentos']:,.0f}".replace(",", "."),
                label="Faturamento Procedimentos"
            )
        
        with col_proc3:
            create_metric_card(
                value=f"R$ {procedimentos_metrics['ticket_medio_procedimentos']:,.0f}".replace(",", "."),
                label="Ticket Médio Procedimentos"
            )
        
        with col_proc4:
            create_metric_card(
                value=f"{procedimentos_metrics['procedimentos_fechados']:,.0f}".replace(",", "."),
                label="Procedimentos Fechados"
            )
        
        # Gráfico de procedimentos por clínica
        st.markdown("### 🏥 Procedimentos por Clínica")
        
        procedimentos_por_clinica = df_procedimentos_consolidado.groupby('Nome_Clinica').agg({
            'Procedimento': 'count',
            'Valor_da_Venda': 'sum'
        }).reset_index()
        procedimentos_por_clinica.columns = ['Clinica', 'Total_Procedimentos', 'Faturamento_Total']
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Gráfico de quantidade de procedimentos
            fig_procedimentos_qty = go.Figure()
            fig_procedimentos_qty.add_trace(go.Bar(
                x=procedimentos_por_clinica['Clinica'],
                y=procedimentos_por_clinica['Total_Procedimentos'],
                name='Procedimentos',
                marker_color='#3B82F6',
                text=procedimentos_por_clinica['Total_Procedimentos'],
                textposition='auto'
            ))
            
            fig_procedimentos_qty.update_layout(
                title="Quantidade de Procedimentos por Clínica",
                xaxis_title="Clínicas",
                yaxis_title="Número de Procedimentos",
                height=400
            )
            
            st.plotly_chart(fig_procedimentos_qty)
        
        with col_chart2:
            # Gráfico de faturamento de procedimentos
            fig_procedimentos_fat = go.Figure()
            fig_procedimentos_fat.add_trace(go.Bar(
                x=procedimentos_por_clinica['Clinica'],
                y=procedimentos_por_clinica['Faturamento_Total'],
                name='Faturamento',
                marker_color='#10B981',
                text=[f"R$ {x:,.0f}".replace(",", ".") for x in procedimentos_por_clinica['Faturamento_Total']],
                textposition='auto'
            ))
            
            fig_procedimentos_fat.update_layout(
                title="Faturamento de Procedimentos por Clínica",
                xaxis_title="Clínicas",
                yaxis_title="Faturamento (R$)",
                height=400
            )
            
            st.plotly_chart(fig_procedimentos_fat)
        
        # Análise por tipo de procedimento
        if 'Tipo' in df_procedimentos_consolidado.columns and df_procedimentos_consolidado['Tipo'].notna().any():
            st.markdown("### 📋 Análise por Tipo de Procedimento")
            
            tipo_analysis = df_procedimentos_consolidado.groupby('Tipo').agg({
                'Procedimento': 'count',
                'Valor_da_Venda': 'sum'
            }).reset_index()
            tipo_analysis.columns = ['Tipo', 'Quantidade', 'Faturamento']
            tipo_analysis = tipo_analysis.sort_values('Quantidade', ascending=False)
            
            col_tipo1, col_tipo2 = st.columns(2)
            
            with col_tipo1:
                # Gráfico de pizza - distribuição por tipo
                fig_tipo_pie = go.Figure(data=[go.Pie(
                    labels=tipo_analysis['Tipo'],
                    values=tipo_analysis['Quantidade'],
                    hole=0.3
                )])
                
                fig_tipo_pie.update_layout(
                    title="Distribuição por Tipo de Procedimento",
                    height=400
                )
                
                st.plotly_chart(fig_tipo_pie)
            
            with col_tipo2:
                # Gráfico de barras - faturamento por tipo
                fig_tipo_bar = go.Figure()
                fig_tipo_bar.add_trace(go.Bar(
                    x=tipo_analysis['Tipo'],
                    y=tipo_analysis['Faturamento'],
                    name='Faturamento',
                    marker_color='#F59E0B',
                    text=[f"R$ {x:,.0f}".replace(",", ".") for x in tipo_analysis['Faturamento']],
                    textposition='auto'
                ))
                
                fig_tipo_bar.update_layout(
                    title="Faturamento por Tipo de Procedimento",
                    xaxis_title="Tipo",
                    yaxis_title="Faturamento (R$)",
                    height=400
                )
                
                st.plotly_chart(fig_tipo_bar)
        
        # Análise temporal de procedimentos
        if 'Mes_Referencia' in df_procedimentos_consolidado.columns:
            st.markdown("### 📅 Evolução Temporal de Procedimentos")
            
            procedimentos_mensais = df_procedimentos_consolidado.groupby('Mes_Referencia').agg({
                'Procedimento': 'count',
                'Valor_da_Venda': 'sum'
            }).reset_index()
            procedimentos_mensais.columns = ['Mes', 'Quantidade', 'Faturamento']
            
            # Ordena os meses corretamente
            mes_order = {
                'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
                'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
                'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
            }
            procedimentos_mensais['mes_order'] = procedimentos_mensais['Mes'].map(mes_order)
            procedimentos_mensais = procedimentos_mensais.sort_values('mes_order').drop('mes_order', axis=1)
            
            fig_procedimentos_temporal = go.Figure()
            
            fig_procedimentos_temporal.add_trace(go.Scatter(
                x=procedimentos_mensais['Mes'],
                y=procedimentos_mensais['Quantidade'],
                name='Quantidade de Procedimentos',
                line=dict(color='#3B82F6', width=3),
                mode='lines+markers'
            ))
            
            fig_procedimentos_temporal.add_trace(go.Scatter(
                x=procedimentos_mensais['Mes'],
                y=procedimentos_mensais['Faturamento'],
                name='Faturamento (R$)',
                line=dict(color='#10B981', width=3),
                mode='lines+markers',
                yaxis='y2'
            ))
            
            fig_procedimentos_temporal.update_layout(
                title="Evolução Mensal de Procedimentos",
                xaxis_title="Meses",
                yaxis_title="Quantidade de Procedimentos",
                yaxis2=dict(title="Faturamento (R$)", overlaying="y", side="right"),
                height=400
            )
            
            st.plotly_chart(fig_procedimentos_temporal)
        
        # Tabela de ranking de procedimentos
        st.markdown("### 🏆 Ranking de Procedimentos por Clínica")
        
        ranking_procedimentos = procedimentos_por_clinica.sort_values('Total_Procedimentos', ascending=False)
        
        col_rank1, col_rank2 = st.columns(2)
        
        with col_rank1:
            st.markdown("**📊 Ranking por Quantidade**")
            for i, (_, row) in enumerate(ranking_procedimentos.iterrows(), 1):
                st.write(f"{i}º **{row['Clinica']}** - {row['Total_Procedimentos']:,.0f} procedimentos".replace(",", "."))
        
        with col_rank2:
            st.markdown("**💰 Ranking por Faturamento**")
            ranking_fat = procedimentos_por_clinica.sort_values('Faturamento_Total', ascending=False)
            for i, (_, row) in enumerate(ranking_fat.iterrows(), 1):
                st.write(f"{i}º **{row['Clinica']}** - R$ {row['Faturamento_Total']:,.0f}".replace(",", "."))
    
    else:
        st.info("Nenhum dado de procedimentos encontrado para análise consolidada.")

def create_executive_summary(df_filtered):
    """Cria seção de resumo executivo com 10 KPIs mais importantes"""
    st.subheader("🎯 Resumo Executivo - Visão Geral")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Valor_Investido_Total'] > 0)]
    
    if df_ativos.empty:
        st.warning("Nenhum dado ativo para resumo executivo.")
        return
    
    # Ordena por mês para comparação
    df_ativos = df_ativos.sort_values('Meses')
    
    # Calcula métricas principais
    total_leads = df_ativos['Leads_Totais'].sum()
    total_faturamento = df_ativos['Faturamento'].sum()
    total_fechamentos = df_ativos['Fechamentos_Totais'].sum()
    total_investimento = df_ativos['Valor_Investido_Total'].sum()
    total_consultas_marcadas = df_ativos['Consultas_Marcadas_Totais'].sum()
    total_consultas_comparecidas = df_ativos['Consultas_Comparecidas'].sum()
    
    # Métricas calculadas
    roas = total_faturamento / total_investimento if total_investimento > 0 else 0
    taxa_conversao_leads = (total_fechamentos / total_leads * 100) if total_leads > 0 else 0
    taxa_comparecimento = (total_consultas_comparecidas / total_consultas_marcadas * 100) if total_consultas_marcadas > 0 else 0
    ticket_medio = total_faturamento / total_fechamentos if total_fechamentos > 0 else 0
    custo_por_lead = total_investimento / total_leads if total_leads > 0 else 0
    
    # Comparação com mês anterior (se houver mais de 1 mês)
    comparacao_mes_anterior = {}
    if len(df_ativos) > 1:
        mes_atual = df_ativos.iloc[-1]
        mes_anterior = df_ativos.iloc[-2]
        
        # Calcula ROAS de forma segura
        roas_atual = mes_atual['Faturamento'] / mes_atual['Valor_Investido_Total'] if mes_atual['Valor_Investido_Total'] > 0 else 0
        roas_anterior = mes_anterior['Faturamento'] / mes_anterior['Valor_Investido_Total'] if mes_anterior['Valor_Investido_Total'] > 0 else 0
        
        # Calcula variação de ROAS de forma segura
        variacao_roas = 0
        if roas_anterior > 0:
            variacao_roas = ((roas_atual - roas_anterior) / roas_anterior) * 100
        
        comparacao_mes_anterior = {
            'leads': ((mes_atual['Leads_Totais'] - mes_anterior['Leads_Totais']) / mes_anterior['Leads_Totais'] * 100) if mes_anterior['Leads_Totais'] > 0 else 0,
            'faturamento': ((mes_atual['Faturamento'] - mes_anterior['Faturamento']) / mes_anterior['Faturamento'] * 100) if mes_anterior['Faturamento'] > 0 else 0,
            'fechamentos': ((mes_atual['Fechamentos_Totais'] - mes_anterior['Fechamentos_Totais']) / mes_anterior['Fechamentos_Totais'] * 100) if mes_anterior['Fechamentos_Totais'] > 0 else 0,
            'roas': variacao_roas
        }
    
    # Função para criar alertas visuais
    def get_alert_color(value, threshold_good=0, threshold_warning=-10):
        if value >= threshold_good:
            return "🟢"  # Verde - bom
        elif value >= threshold_warning:
            return "🟡"  # Amarelo - atenção
        else:
            return "🔴"  # Vermelho - crítico
    
    # Layout principal - 2 linhas de 5 KPIs cada
    st.markdown("### 📊 Top 10 KPIs Executivos")
    
    # Primeira linha - KPIs principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🎯 Total de Leads",
            value=f"{total_leads:,.0f}".replace(",", "."),
            delta=f"{comparacao_mes_anterior.get('leads', 0):+.1f}%" if comparacao_mes_anterior else None,
            help="Total de leads gerados no período"
        )
    
    with col2:
        st.metric(
            label="💰 Faturamento Total",
            value=f"R$ {total_faturamento:,.0f}".replace(",", "."),
            delta=f"{comparacao_mes_anterior.get('faturamento', 0):+.1f}%" if comparacao_mes_anterior else None,
            help="Receita total gerada"
        )
    
    with col3:
        st.metric(
            label="🎉 Fechamentos",
            value=f"{total_fechamentos}",
            delta=f"{comparacao_mes_anterior.get('fechamentos', 0):+.1f}%" if comparacao_mes_anterior else None,
            help="Total de vendas realizadas"
        )
    
    with col4:
        st.metric(
            label="📈 ROAS",
            value=f"{roas:.1f}x",
            delta=f"{comparacao_mes_anterior.get('roas', 0):+.1f}%" if comparacao_mes_anterior else None,
            help="Retorno sobre investimento em anúncios"
        )
    
    with col5:
        st.metric(
            label="💵 Ticket Médio",
            value=f"R$ {ticket_medio:,.0f}".replace(",", "."),
            help="Valor médio por venda"
        )
    
    # Segunda linha - KPIs de conversão e eficiência
    col6, col7, col8, col9, col10 = st.columns(5)
    
    with col6:
        st.metric(
            label="🔄 Taxa de Conversão",
            value=f"{taxa_conversao_leads:.1f}%",
            help="% de leads que se tornaram clientes"
        )
    
    with col7:
        st.metric(
            label="📅 Consultas Marcadas",
            value=f"{total_consultas_marcadas}",
            help="Total de consultas agendadas"
        )
    
    with col8:
        st.metric(
            label="✅ Consultas Comparecidas",
            value=f"{total_consultas_comparecidas}",
            help="Consultas que realmente aconteceram"
        )
    
    with col9:
        st.metric(
            label="📊 Taxa de Comparecimento",
            value=f"{taxa_comparecimento:.1f}%",
            help="% de consultas que compareceram"
        )
    
    with col10:
        st.metric(
            label="💸 Custo por Lead",
            value=f"R$ {custo_por_lead:,.0f}".replace(",", "."),
            help="Custo médio para gerar 1 lead"
        )
    
    # Seção de Alertas e Insights
    st.markdown("---")
    st.markdown("### 🚨 Alertas e Insights Automáticos")
    
    # Alertas baseados em thresholds
    alertas = []
    
    # Alertas de performance
    if roas < 3:
        alertas.append("🔴 **ROAS Baixo**: ROAS abaixo de 3x - considere otimizar campanhas")
    elif roas > 10:
        alertas.append("🟢 **ROAS Excelente**: ROAS acima de 10x - considere aumentar investimento")
    
    if taxa_conversao_leads < 2:
        alertas.append("🔴 **Conversão Baixa**: Taxa de conversão abaixo de 2% - revise processo de vendas")
    elif taxa_conversao_leads > 8:
        alertas.append("🟢 **Conversão Excelente**: Taxa de conversão acima de 8% - processo otimizado")
    
    if taxa_comparecimento < 50:
        alertas.append("🟡 **Comparecimento Baixo**: Taxa de comparecimento abaixo de 50% - revise agendamentos")
    elif taxa_comparecimento > 80:
        alertas.append("🟢 **Comparecimento Excelente**: Taxa de comparecimento acima de 80%")
    
    if custo_por_lead > 100:
        alertas.append("🔴 **Custo Alto por Lead**: Custo acima de R$ 100 - otimize campanhas")
    elif custo_por_lead < 30:
        alertas.append("🟢 **Custo Otimizado**: Custo por lead abaixo de R$ 30 - excelente!")
    
    # Alertas de comparação mensal
    if comparacao_mes_anterior:
        if comparacao_mes_anterior.get('leads', 0) < -20:
            alertas.append("🔴 **Queda de Leads**: Redução de mais de 20% vs mês anterior")
        elif comparacao_mes_anterior.get('leads', 0) > 20:
            alertas.append("🟢 **Crescimento de Leads**: Aumento de mais de 20% vs mês anterior")
        
        if comparacao_mes_anterior.get('faturamento', 0) < -15:
            alertas.append("🔴 **Queda de Faturamento**: Redução de mais de 15% vs mês anterior")
        elif comparacao_mes_anterior.get('faturamento', 0) > 15:
            alertas.append("🟢 **Crescimento de Faturamento**: Aumento de mais de 15% vs mês anterior")
    
    # Exibe alertas
    if alertas:
        for alerta in alertas:
            st.markdown(alerta)
    else:
        st.success("🟢 **Todas as métricas estão dentro dos parâmetros esperados!**")
    
    # Resumo de performance geral
    st.markdown("---")
    st.markdown("### 📈 Resumo de Performance")
    
    col_resumo1, col_resumo2, col_resumo3 = st.columns(3)
    
    with col_resumo1:
        st.markdown("**🎯 Performance Geral**")
        if roas > 5 and taxa_conversao_leads > 3:
            st.success("**Excelente** - Performance acima da média")
        elif roas > 3 and taxa_conversao_leads > 2:
            st.info("**Boa** - Performance dentro do esperado")
        else:
            st.warning("**Atenção** - Performance abaixo do esperado")
    
    with col_resumo2:
        st.markdown("**💰 Eficiência Financeira**")
        if custo_por_lead < 50 and roas > 4:
            st.success("**Otimizada** - Custos controlados e bom retorno")
        elif custo_por_lead < 100 and roas > 2:
            st.info("**Adequada** - Custos e retorno equilibrados")
        else:
            st.warning("**Revisar** - Custos altos ou retorno baixo")
    
    with col_resumo3:
        st.markdown("**🔄 Processo de Vendas**")
        if taxa_comparecimento > 70 and taxa_conversao_leads > 3:
            st.success("**Eficiente** - Processo bem estruturado")
        elif taxa_comparecimento > 50 and taxa_conversao_leads > 2:
            st.info("**Regular** - Processo funcionando")
        else:
            st.warning("**Melhorar** - Processo precisa de otimização")

def create_insights_section(df_filtered):
    """Cria seção de insights e recomendações"""
    st.subheader("💡 Insights e Recomendações")
    st.markdown("*(Os insights abaixo são baseados no período selecionado)*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Pontos Fortes")
        st.markdown("""
        - **Instagram Orgânico** é o canal mais eficiente
        - **ROAS excelente** em períodos de alta performance
        - **Custo por lead** otimizado ao longo do tempo
        - **Ticket médio** consistentemente alto
        """)
    
    with col2:
        st.markdown("### 📋 Recomendações")
        st.markdown("""
        - **Aumentar investimento** em canais de alta conversão
        - **Otimizar campanhas** com baixa performance
        - **Fortalecer programa** de indicações
        - **Padronizar processo** de follow-up de leads
        """)

def create_procedimentos_analysis(df_procedimentos):
    """Cria análise detalhada de procedimentos"""
    st.subheader("🏥 Análise de Procedimentos")
    
    if df_procedimentos.empty:
        st.info("Nenhum procedimento encontrado para análise.")
        return
    
    # KPIs principais de procedimentos
    col1, col2, col3, col4 = st.columns(4)
    
    total_procedimentos = len(df_procedimentos)
    total_faturamento_procedimentos = df_procedimentos['Valor_da_Venda'].sum()
    ticket_medio_procedimentos = df_procedimentos['Valor_da_Venda'].mean()
    procedimentos_fechados = len(df_procedimentos[df_procedimentos['Data_Fechou_Cirurgia'].notna()])
    
    with col1:
        st.metric(
            label="Total de Procedimentos",
            value=f"{total_procedimentos}",
            help="Total de procedimentos registrados"
        )
    
    with col2:
        st.metric(
            label="Faturamento Total",
            value=f"R$ {total_faturamento_procedimentos:,.0f}".replace(",", "."),
            help="Faturamento total dos procedimentos"
        )
    
    with col3:
        st.metric(
            label="Ticket Médio",
            value=f"R$ {ticket_medio_procedimentos:,.0f}".replace(",", "."),
            help="Valor médio por procedimento"
        )
    
    with col4:
        st.metric(
            label="Procedimentos Fechados",
            value=f"{procedimentos_fechados}",
            delta=f"{procedimentos_fechados/total_procedimentos*100:.1f}%" if total_procedimentos > 0 else "0%",
            help="Procedimentos com cirurgia fechada"
        )
    
    # Análise por tipo de procedimento
    st.markdown("### 📊 Análise por Tipo de Procedimento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza - Distribuição por tipo
        if 'Tipo' in df_procedimentos.columns and df_procedimentos['Tipo'].notna().any():
            tipo_counts = df_procedimentos['Tipo'].value_counts()
            fig_tipo = px.pie(
                values=tipo_counts.values,
                names=tipo_counts.index,
                title="Distribuição por Tipo de Procedimento",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_tipo)
        else:
            st.info("Dados de tipo não disponíveis")
    
    with col2:
        # Gráfico de barras - Faturamento por tipo
        if 'Tipo' in df_procedimentos.columns and df_procedimentos['Tipo'].notna().any():
            tipo_faturamento = df_procedimentos.groupby('Tipo')['Valor_da_Venda'].sum().sort_values(ascending=False)
            fig_faturamento_tipo = px.bar(
                x=tipo_faturamento.index,
                y=tipo_faturamento.values,
                title="Faturamento por Tipo de Procedimento",
                color=tipo_faturamento.values,
                color_continuous_scale='Viridis',
                text=[f"R$ {x:,.0f}".replace(",", ".") for x in tipo_faturamento.values]
            )
            fig_faturamento_tipo.update_layout(showlegend=False)
            st.plotly_chart(fig_faturamento_tipo)
        else:
            st.info("Dados de tipo não disponíveis")
    
    # Análise temporal
    st.markdown("### 📅 Análise Temporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Procedimentos por mês
        if 'Mes_Referencia' in df_procedimentos.columns:
            procedimentos_mes = df_procedimentos['Mes_Referencia'].value_counts()
            fig_mes = px.bar(
                x=procedimentos_mes.index,
                y=procedimentos_mes.values,
                title="Procedimentos por Mês",
                color=procedimentos_mes.values,
                color_continuous_scale='Blues',
                text=procedimentos_mes.values
            )
            fig_mes.update_layout(showlegend=False)
            st.plotly_chart(fig_mes)
    
    with col2:
        # Faturamento por mês
        if 'Mes_Referencia' in df_procedimentos.columns:
            faturamento_mes = df_procedimentos.groupby('Mes_Referencia')['Valor_da_Venda'].sum()
            fig_faturamento_mes = px.bar(
                x=faturamento_mes.index,
                y=faturamento_mes.values,
                title="Faturamento por Mês",
                color=faturamento_mes.values,
                color_continuous_scale='Greens',
                text=[f"R$ {x:,.0f}".replace(",", ".") for x in faturamento_mes.values]
            )
            fig_faturamento_mes.update_layout(showlegend=False)
            st.plotly_chart(fig_faturamento_mes)
    
    # Análise de formas de pagamento
    st.markdown("### 💳 Análise de Formas de Pagamento")
    
    if 'Forma_Pagamento' in df_procedimentos.columns and df_procedimentos['Forma_Pagamento'].notna().any():
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por forma de pagamento
            pagamento_counts = df_procedimentos['Forma_Pagamento'].value_counts()
            fig_pagamento = px.pie(
                values=pagamento_counts.values,
                names=pagamento_counts.index,
                title="Distribuição por Forma de Pagamento",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pagamento)
        
        with col2:
            # Faturamento por forma de pagamento
            pagamento_faturamento = df_procedimentos.groupby('Forma_Pagamento')['Valor_da_Venda'].sum().sort_values(ascending=False)
            fig_pagamento_fat = px.bar(
                x=pagamento_faturamento.index,
                y=pagamento_faturamento.values,
                title="Faturamento por Forma de Pagamento",
                color=pagamento_faturamento.values,
                color_continuous_scale='Oranges',
                text=[f"R$ {x:,.0f}".replace(",", ".") for x in pagamento_faturamento.values]
            )
            fig_pagamento_fat.update_layout(showlegend=False)
            st.plotly_chart(fig_pagamento_fat)
    else:
        st.info("Dados de forma de pagamento não disponíveis")
    
    # Tabela detalhada de procedimentos
    st.markdown("### 📋 Detalhamento dos Procedimentos")
    
    # Prepara dados para exibição
    df_display = df_procedimentos.copy()
    
    # Formata datas
    date_columns = ['Data_Primeiro_Contato', 'Data_Compareceu_Consulta', 'Data_Fechou_Cirurgia']
    for col in date_columns:
        if col in df_display.columns:
            df_display[col] = df_display[col].dt.strftime('%d/%m/%Y').fillna('')
    
    # Formata valores monetários
    currency_columns = ['Valor_da_Venda', 'Valor_Parcelado']
    for col in currency_columns:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: f"R$ {x:,.2f}".replace(",", ".") if pd.notna(x) and x > 0 else "")
    
    # Seleciona colunas para exibição
    display_columns = [
        'Mes_Referencia', 'Procedimento', 'Tipo', 'Data_Primeiro_Contato',
        'Data_Compareceu_Consulta', 'Data_Fechou_Cirurgia', 'Forma_Pagamento',
        'Valor_da_Venda', 'Valor_Parcelado', 'Quantidade_na_Mesma_Venda'
    ]
    
    # Filtra colunas que existem no DataFrame
    available_columns = [col for col in display_columns if col in df_display.columns]
    df_display = df_display[available_columns]
    
    # Renomeia colunas para exibição
    column_mapping = {
        'Mes_Referencia': 'Mês',
        'Procedimento': 'Procedimento',
        'Tipo': 'Tipo',
        'Data_Primeiro_Contato': '1° Contato',
        'Data_Compareceu_Consulta': 'Compareceu Consulta',
        'Data_Fechou_Cirurgia': 'Fechou Cirurgia',
        'Forma_Pagamento': 'Forma de Pagamento',
        'Valor_da_Venda': 'Valor da Venda',
        'Valor_Parcelado': 'Valor Parcelado',
        'Quantidade_na_Mesma_Venda': 'Qtd. na Venda'
    }
    
    df_display = df_display.rename(columns=column_mapping)
    
    # Exibe tabela com paginação
    st.dataframe(
        df_display,
        height=400,
        hide_index=True
    )

def load_data_from_database(cliente_id: int, meses_selecionados: list = None) -> pd.DataFrame:
    """
    Carrega dados do banco de dados para um cliente específico
    
    Args:
        cliente_id: ID do cliente
        meses_selecionados: Lista de meses para filtrar (opcional)
    
    Returns:
        pd.DataFrame: DataFrame com os dados do dashboard
    """
    from database import dados_crud
    
    if meses_selecionados:
        dados = dados_crud.get_dados_by_cliente_and_period(cliente_id, meses_selecionados)
    else:
        dados = dados_crud.get_dados_by_cliente(cliente_id)
    
    return dados_crud.dados_to_dataframe(dados)

def load_procedimentos_from_database(cliente_id: int, meses_selecionados: list = None) -> pd.DataFrame:
    """
    Carrega dados de procedimentos do banco de dados para um cliente específico
    
    Args:
        cliente_id: ID do cliente
        meses_selecionados: Lista de meses para filtrar (opcional)
    
    Returns:
        pd.DataFrame: DataFrame com os dados de procedimentos
    """
    from database import procedimento_crud
    
    if meses_selecionados:
        procedimentos = procedimento_crud.get_procedimentos_by_period(cliente_id, meses_selecionados)
    else:
        procedimentos = procedimento_crud.get_procedimentos_by_cliente(cliente_id)
    
    return procedimento_crud.procedimentos_to_dataframe(procedimentos)

