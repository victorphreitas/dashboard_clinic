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
    
    # Filtra apenas meses com atividade (aqui deve ser usado apenas para cálculo de média,
    # pois o df_filtered já deve ter apenas meses relevantes, mas mantemos a coerência)
    df_metrics = df_ativos[(df_ativos['Leads_Totais'] > 0) | (df_ativos['Faturamento'] > 0) | (df_ativos['Investimento_Total'] > 0)]
    
    if df_metrics.empty:
        st.warning("Nenhum dado ativo neste período.")
        return
        
    total_leads = df_metrics['Leads_Totais'].sum()
    total_faturamento = df_metrics['Faturamento'].sum()
    total_fechamentos = df_metrics['Fechamentos_Totais'].sum()
    total_investimento = df_metrics['Investimento_Total'].sum()
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
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Investimento_Total'] > 0)]
    
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
        st.plotly_chart(fig_funnel, use_container_width=True)
    
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
            y=df_ativos['Investimento_Total'],
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
        st.plotly_chart(fig_revenue, use_container_width=True)
    
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
        
        st.plotly_chart(fig_roas, use_container_width=True)

def create_channel_analysis(df_filtered):
    """Análise de performance por canal"""
    st.subheader("📱 Performance por Canal de Aquisição")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Investimento_Total'] > 0)]
    
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
        st.plotly_chart(fig_leads, use_container_width=True)
    
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
        st.plotly_chart(fig_conversion, use_container_width=True)

def create_cost_analysis(df_filtered):
    """Análise de custos e eficiência"""
    st.subheader("💸 Análise de Custos e Eficiência")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Investimento_Total'] > 0)]
    
    if df_ativos.empty:
        st.info("Nenhum dado ativo para análise de custos no período selecionado.")
        return
        
    col1, col2, col3 = st.columns(3)
    
    # CPL Médio (ignorando zeros/indefinidos)
    cpl_medio = df_ativos['Custo_por_Lead'].replace(0, np.nan).mean()
    cpl_min = df_ativos['Custo_por_Lead'].replace(0, np.nan).min()
    with col1:
        st.metric(
            "Custo por Lead Médio",
            f"R$ {cpl_medio:.2f}" if not pd.isna(cpl_medio) else "N/A",
            delta=f"Menor: R$ {cpl_min:.2f}" if not pd.isna(cpl_min) else "N/A"
        )
    
    # CPA Médio (ignorando zeros/indefinidos)
    cpa_medio = df_ativos['Custo_por_Compra'].replace(0, np.nan).mean()
    cpa_min = df_ativos['Custo_por_Compra'].replace(0, np.nan).min()
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
        x=df_ativos['Meses'], y=df_ativos['Custo_por_Lead'],
        name='Custo por Lead', line=dict(color='#1f77b4', width=3)
    ))
    
    fig_costs.add_trace(go.Scatter(
        x=df_ativos['Meses'], y=df_ativos['Custo_por_Compra'],
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
    
    st.plotly_chart(fig_costs, use_container_width=True)

def create_monthly_trends(df_filtered):
    """Tendências mensais e sazonais"""
    st.subheader("📈 Tendências e Sazonalidade")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Investimento_Total'] > 0)]
    
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
    st.plotly_chart(fig_trends, use_container_width=True)

def create_executive_summary(df_filtered):
    """Cria seção de resumo executivo com 10 KPIs mais importantes"""
    st.subheader("🎯 Resumo Executivo - Visão Geral")
    
    df_ativos = df_filtered[(df_filtered['Leads_Totais'] > 0) | (df_filtered['Faturamento'] > 0) | (df_filtered['Investimento_Total'] > 0)]
    
    if df_ativos.empty:
        st.warning("Nenhum dado ativo para resumo executivo.")
        return
    
    # Ordena por mês para comparação
    df_ativos = df_ativos.sort_values('Meses')
    
    # Calcula métricas principais
    total_leads = df_ativos['Leads_Totais'].sum()
    total_faturamento = df_ativos['Faturamento'].sum()
    total_fechamentos = df_ativos['Fechamentos_Totais'].sum()
    total_investimento = df_ativos['Investimento_Total'].sum()
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
        roas_atual = mes_atual['Faturamento'] / mes_atual['Investimento_Total'] if mes_atual['Investimento_Total'] > 0 else 0
        roas_anterior = mes_anterior['Faturamento'] / mes_anterior['Investimento_Total'] if mes_anterior['Investimento_Total'] > 0 else 0
        
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

