"""
Sistema de Design Moderno para o Dashboard
Paleta de cores, tipografia e componentes reutilizáveis
"""

import streamlit as st

# Paleta de cores moderna
COLORS = {
    'primary': '#3B82F6',      # Azul moderno
    'primary_dark': '#2563EB',  # Azul escuro
    'primary_light': '#60A5FA', # Azul claro
    'secondary': '#6B7280',     # Cinza neutro
    'success': '#10B981',       # Verde sucesso
    'warning': '#F59E0B',       # Amarelo aviso
    'error': '#EF4444',         # Vermelho erro
    'background': '#F8FAFC',   # Fundo claro
    'surface': '#FFFFFF',      # Superfície branca
    'text_primary': '#1F2937', # Texto principal
    'text_secondary': '#6B7280', # Texto secundário
    'border': '#E5E7EB',      # Bordas
    'border_light': '#F3F4F6' # Bordas claras
}

# Tipografia
TYPOGRAPHY = {
    'font_family': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    'h1_size': '2.5rem',
    'h2_size': '2rem',
    'h3_size': '1.5rem',
    'h4_size': '1.25rem',
    'body_size': '1rem',
    'small_size': '0.875rem'
}

# Espaçamentos
SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'md': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    'xxl': '3rem'
}

def apply_modern_styles():
    """Aplica estilos modernos ao Streamlit"""
    
    st.markdown(f"""
    <style>
    /* Reset e configurações base */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    /* Configuração da fonte */
    html, body, [class*="css"] {{
        font-family: {TYPOGRAPHY['font_family']};
        color: {COLORS['text_primary']};
        background-color: {COLORS['background']};
    }}
    
    /* Header principal */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white;
        padding: {SPACING['lg']} {SPACING['xl']};
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 1rem 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .main-header h1 {{
        font-size: {TYPOGRAPHY['h1_size']};
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.025em;
    }}
    
    .main-header p {{
        font-size: {TYPOGRAPHY['body_size']};
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }}
    
    /* Cards modernos */
    .modern-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 0.75rem;
        padding: {SPACING['lg']};
        margin-bottom: {SPACING['lg']};
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }}
    
    .modern-card:hover {{
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }}
    
    /* Botões modernos */
    .modern-button {{
        background: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: {SPACING['sm']} {SPACING['lg']};
        font-weight: 500;
        font-size: {TYPOGRAPHY['body_size']};
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }}
    
    .modern-button:hover {{
        background: {COLORS['primary_dark']};
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .modern-button-secondary {{
        background: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
    }}
    
    .modern-button-secondary:hover {{
        background: {COLORS['background']};
        border-color: {COLORS['primary']};
    }}
    
    /* Métricas/KPIs */
    .metric-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 0.75rem;
        padding: {SPACING['lg']};
        text-align: center;
        transition: all 0.2s ease;
    }}
    
    .metric-card:hover {{
        border-color: {COLORS['primary']};
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['primary']};
        margin: 0;
    }}
    
    .metric-label {{
        font-size: {TYPOGRAPHY['small_size']};
        color: {COLORS['text_secondary']};
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }}
    
    /* Tabelas modernas */
    .modern-table {{
        background: {COLORS['surface']};
        border-radius: 0.75rem;
        overflow: hidden;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }}
    
    .modern-table th {{
        background: {COLORS['background']};
        color: {COLORS['text_primary']};
        font-weight: 600;
        padding: {SPACING['md']};
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    .modern-table td {{
        padding: {SPACING['md']};
        border-bottom: 1px solid {COLORS['border_light']};
    }}
    
    .modern-table tr:hover {{
        background: {COLORS['background']};
    }}
    
    /* Navegação lateral moderna */
    .sidebar .sidebar-content {{
        background: {COLORS['surface']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    .sidebar .sidebar-content .block-container {{
        padding: {SPACING['lg']};
    }}
    
    /* Botões de navegação */
    .nav-button {{
        background: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 0.5rem;
        padding: {SPACING['sm']} {SPACING['md']};
        margin: {SPACING['xs']} 0;
        width: 100%;
        text-align: center;
        font-weight: 500;
        transition: all 0.2s ease;
        cursor: pointer;
    }}
    
    .nav-button:hover {{
        background: {COLORS['primary']};
        color: white;
        border-color: {COLORS['primary']};
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    }}
    
    .nav-button.active {{
        background: {COLORS['primary']};
        color: white;
        border-color: {COLORS['primary']};
    }}
    
    /* Status badges */
    .status-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: {TYPOGRAPHY['small_size']};
        font-weight: 500;
    }}
    
    .status-active {{
        background: rgba(16, 185, 129, 0.1);
        color: {COLORS['success']};
    }}
    
    .status-inactive {{
        background: rgba(239, 68, 68, 0.1);
        color: {COLORS['error']};
    }}
    
    /* Formulários modernos */
    .modern-form {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 0.75rem;
        padding: {SPACING['xl']};
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }}
    
    /* Alertas modernos */
    .modern-alert {{
        padding: {SPACING['md']};
        border-radius: 0.5rem;
        margin: {SPACING['md']} 0;
        border-left: 4px solid;
    }}
    
    .alert-success {{
        background: rgba(16, 185, 129, 0.1);
        border-color: {COLORS['success']};
        color: {COLORS['success']};
    }}
    
    .alert-warning {{
        background: rgba(245, 158, 11, 0.1);
        border-color: {COLORS['warning']};
        color: {COLORS['warning']};
    }}
    
    .alert-error {{
        background: rgba(239, 68, 68, 0.1);
        border-color: {COLORS['error']};
        color: {COLORS['error']};
    }}
    
    /* Gráficos */
    .chart-container {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 0.75rem;
        padding: {SPACING['lg']};
        margin: {SPACING['md']} 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }}
    
    /* Responsividade */
    @media (max-width: 768px) {{
        .main-header {{
            padding: {SPACING['md']};
            margin: -1rem -1rem 1rem -1rem;
        }}
        
        .main-header h1 {{
            font-size: {TYPOGRAPHY['h2_size']};
        }}
        
        .modern-card {{
            padding: {SPACING['md']};
        }}
    }}
    
    /* Animações sutis */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.3s ease-out;
    }}
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['background']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['border']};
        border-radius: 3px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['text_secondary']};
    }}
    </style>
    """, unsafe_allow_html=True)

def create_modern_header(title: str, subtitle: str = ""):
    """Cria header moderno para páginas"""
    st.markdown(f"""
    <div class="main-header fade-in">
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(value: str, label: str, delta: str = None):
    """Cria card de métrica moderno"""
    delta_html = f'<div style="color: {COLORS["success"]}; font-size: 0.875rem; margin-top: 0.25rem;">{delta}</div>' if delta else ''
    
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_status_badge(status: str, is_active: bool = True):
    """Cria badge de status moderno"""
    status_class = "status-active" if is_active else "status-inactive"
    status_text = "Ativo" if is_active else "Inativo"
    
    st.markdown(f"""
    <span class="status-badge {status_class}">{status_text}</span>
    """, unsafe_allow_html=True)

def create_modern_button(text: str, key: str = None, variant: str = "primary", use_container_width: bool = True):
    """Cria botão moderno"""
    button_class = "modern-button" if variant == "primary" else "modern-button modern-button-secondary"
    
    if st.button(text, key=key, use_container_width=use_container_width):
        return True
    return False

def create_modern_alert(message: str, alert_type: str = "info"):
    """Cria alerta moderno"""
    alert_class = f"modern-alert alert-{alert_type}"
    
    st.markdown(f"""
    <div class="{alert_class}">
        {message}
    </div>
    """, unsafe_allow_html=True)
