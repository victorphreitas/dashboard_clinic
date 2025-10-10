"""
Sistema de autenticação e controle de sessão.
Gerencia login, logout, registro e controle de acesso.
"""

import streamlit as st
from typing import Optional, Dict, Any
import re
import os
from dotenv import load_dotenv
from database import cliente_crud, Cliente

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
SECRET_KEY = os.getenv('SECRET_KEY', 'chave_padrao_para_desenvolvimento')

class AuthManager:
    """Gerenciador de autenticação e sessão"""
    
    def __init__(self):
        self.session_key = "user"
        self.admin_key = "is_admin"
        self.cliente_id_key = "cliente_id"
    
    def is_authenticated(self) -> bool:
        """Verifica se o usuário está autenticado"""
        return self.session_key in st.session_state and st.session_state[self.session_key] is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Retorna dados do usuário atual"""
        if self.is_authenticated():
            return st.session_state[self.session_key]
        return None
    
    def is_admin(self) -> bool:
        """Verifica se o usuário atual é administrador"""
        return st.session_state.get(self.admin_key, False)
    
    def get_cliente_id(self) -> Optional[int]:
        """Retorna o ID do cliente atual"""
        return st.session_state.get(self.cliente_id_key)
    
    def login(self, email: str, senha: str) -> bool:
        """
        Realiza login do usuário
        
        Args:
            email: Email do usuário
            senha: Senha do usuário
            
        Returns:
            bool: True se login bem-sucedido, False caso contrário
        """
        try:
            cliente = cliente_crud.authenticate_cliente(email, senha)
            if cliente:
                # Armazena dados do usuário na sessão
                st.session_state[self.session_key] = {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "email": cliente.email,
                    "nome_da_clinica": cliente.nome_da_clinica,
                    "is_admin": cliente.is_admin
                }
                st.session_state[self.admin_key] = cliente.is_admin
                st.session_state[self.cliente_id_key] = cliente.id
                return True
            return False
        except Exception as e:
            st.error(f"Erro no login: {str(e)}")
            return False
    
    def logout(self):
        """Realiza logout do usuário"""
        # Limpa todas as variáveis de sessão relacionadas à autenticação
        keys_to_clear = [self.session_key, self.admin_key, self.cliente_id_key]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        # Força rerun para limpar a interface
        st.rerun()
    
    def register(self, nome: str, email: str, senha: str, confirmar_senha: str,
                cnpj: str = "", nome_da_clinica: str = "", telefone: str = "",
                endereco: str = "", link_empresa: str = "") -> tuple[bool, str]:
        """
        Registra um novo cliente
        
        Args:
            nome: Nome do cliente
            email: Email do cliente
            senha: Senha do cliente
            confirmar_senha: Confirmação da senha
            cnpj: CNPJ da clínica
            nome_da_clinica: Nome da clínica
            telefone: Telefone de contato
            endereco: Endereço da clínica
            
        Returns:
            tuple: (sucesso, mensagem)
        """
        # Validações
        if not self._validate_email(email):
            return False, "Email inválido"
        
        if not self._validate_password(senha):
            return False, "Senha deve ter pelo menos 6 caracteres"
        
        if senha != confirmar_senha:
            return False, "Senhas não coincidem"
        
        if not nome.strip():
            return False, "Nome é obrigatório"
        
        if not nome_da_clinica.strip():
            return False, "Nome da clínica é obrigatório"
        
        try:
            cliente = cliente_crud.create_cliente(
                nome=nome.strip(),
                email=email.strip().lower(),
                senha=senha,
                cnpj=cnpj.strip() if cnpj else None,
                nome_da_clinica=nome_da_clinica.strip(),
                telefone=telefone.strip() if telefone else None,
                endereco=endereco.strip() if endereco else None,
                link_empresa=link_empresa.strip() if link_empresa else None
            )
            
            if cliente:
                return True, "Cliente registrado com sucesso!"
            else:
                return False, "Email já cadastrado"
        except Exception as e:
            return False, f"Erro no registro: {str(e)}"
    
    def update_cliente(self, cliente_id: int, **kwargs) -> tuple[bool, str]:
        """
        Atualiza dados de um cliente
        
        Args:
            cliente_id: ID do cliente
            **kwargs: Campos para atualizar
            
        Returns:
            tuple: (sucesso, mensagem)
        """
        try:
            # Validações específicas
            if 'email' in kwargs and not self._validate_email(kwargs['email']):
                return False, "Email inválido"
            
            if 'senha' in kwargs and kwargs['senha'] and not self._validate_password(kwargs['senha']):
                return False, "Senha deve ter pelo menos 6 caracteres"
            
            # Remove campos vazios
            kwargs = {k: v for k, v in kwargs.items() if v is not None and v != ""}
            
            success = cliente_crud.update_cliente(cliente_id, **kwargs)
            if success:
                return True, "Cliente atualizado com sucesso!"
            else:
                return False, "Cliente não encontrado"
        except Exception as e:
            return False, f"Erro ao atualizar cliente: {str(e)}"
    
    def delete_cliente(self, cliente_id: int, hard_delete: bool = False) -> tuple[bool, str]:
        """
        Remove um cliente
        
        Args:
            cliente_id: ID do cliente
            hard_delete: Se True, remove permanentemente
            
        Returns:
            tuple: (sucesso, mensagem)
        """
        try:
            if hard_delete:
                success = cliente_crud.hard_delete_cliente(cliente_id)
                message = "Cliente removido permanentemente!"
            else:
                success = cliente_crud.delete_cliente(cliente_id)
                message = "Cliente desativado com sucesso!"
            
            if success:
                return True, message
            else:
                return False, "Cliente não encontrado"
        except Exception as e:
            return False, f"Erro ao remover cliente: {str(e)}"
    
    def _validate_email(self, email: str) -> bool:
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_password(self, senha: str) -> bool:
        """Valida senha (mínimo 6 caracteres)"""
        return len(senha) >= 6

def show_login_form() -> bool:
    """
    Exibe formulário de login
    
    Returns:
        bool: True se login bem-sucedido, False caso contrário
    """
    auth = AuthManager()
    
    st.subheader("🔐 Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="seu@email.com")
        senha = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Entrar", use_container_width=True)
        
        if submit_button:
            if not email or not senha:
                st.error("Por favor, preencha todos os campos")
                return False
            
            if auth.login(email, senha):
                st.success("Login realizado com sucesso!")
                st.rerun()
                return True
            else:
                st.error("Email ou senha incorretos")
                return False
    
    return False

def show_register_form() -> bool:
    """
    Exibe formulário de registro
    
    Returns:
        bool: True se registro bem-sucedido, False caso contrário
    """
    auth = AuthManager()
    
    st.subheader("📝 Cadastro de Nova Clínica")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *", placeholder="Seu nome completo")
            email = st.text_input("Email *", placeholder="seu@email.com")
            senha = st.text_input("Senha *", type="password", placeholder="Mínimo 6 caracteres")
            confirmar_senha = st.text_input("Confirmar Senha *", type="password")
        
        with col2:
            nome_da_clinica = st.text_input("Nome da Clínica *", placeholder="Nome da sua clínica")
            cnpj = st.text_input("CNPJ", placeholder="00.000.000/0000-00")
            telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")
            endereco = st.text_input("Endereço", placeholder="Endereço completo")
            link_empresa = st.text_input("Link Google Sheets", placeholder="https://docs.google.com/spreadsheets/d/...")
        
        submit_button = st.form_submit_button("Cadastrar", use_container_width=True)
        
        if submit_button:
            sucesso, mensagem = auth.register(
                nome=nome,
                email=email,
                senha=senha,
                confirmar_senha=confirmar_senha,
                cnpj=cnpj,
                nome_da_clinica=nome_da_clinica,
                telefone=telefone,
                endereco=endereco,
                link_empresa=link_empresa
            )
            
            if sucesso:
                st.success(mensagem)
                st.info("Agora você pode fazer login com suas credenciais")
                return True
            else:
                st.error(mensagem)
                return False
    
    return False


def show_admin_register_clinic_form() -> bool:
    """
    Exibe formulário para administrador cadastrar nova clínica
    (sem campos de autenticação)
    
    Returns:
        bool: True se cadastro bem-sucedido, False caso contrário
    """
    auth = AuthManager()
    
    # Botões de navegação
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("🏥 Gerenciar Clínicas", use_container_width=True, key="nav_gerenciar_from_register"):
            st.session_state['show_admin_register'] = False
            st.session_state['show_clinic_management'] = True
            st.rerun()
    
    with col_nav2:
        if st.button("📊 Dashboard Consolidado", use_container_width=True, key="nav_dashboard_from_register"):
            st.session_state['show_admin_register'] = False
            st.session_state['show_admin_dashboard'] = True
            st.rerun()
    
    with col_nav3:
        if st.button("👥 Ver Clínicas", use_container_width=True, key="nav_ver_from_register"):
            st.session_state['show_admin_register'] = False
            st.rerun()
    
    st.subheader("🏥 Cadastrar Nova Clínica (Admin)")
    st.info("Como administrador, você está cadastrando uma nova clínica no sistema.")
    
    with st.form("admin_register_clinic_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_responsavel = st.text_input("Nome do Responsável *", placeholder="Nome do responsável pela clínica")
            email_clinica = st.text_input("Email da Clínica *", placeholder="email@clinica.com")
            senha_clinica = st.text_input("Senha da Clínica *", type="password", placeholder="Senha para acesso da clínica")
        
        with col2:
            nome_da_clinica = st.text_input("Nome da Clínica *", placeholder="Nome da clínica")
            cnpj = st.text_input("CNPJ", placeholder="00.000.000/0000-00")
            telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")
            endereco = st.text_input("Endereço", placeholder="Endereço completo")
            link_empresa = st.text_input("Link Google Sheets *", placeholder="https://docs.google.com/spreadsheets/d/...")
        
        submit_button = st.form_submit_button("Cadastrar Clínica", use_container_width=True)
        
        if submit_button:
            # Validações básicas
            if not nome_responsavel.strip():
                st.error("Nome do responsável é obrigatório")
                return False
            if not email_clinica.strip():
                st.error("Email da clínica é obrigatório")
                return False
            if not senha_clinica.strip():
                st.error("Senha é obrigatória")
                return False
            if not nome_da_clinica.strip():
                st.error("Nome da clínica é obrigatório")
                return False
            if not link_empresa.strip():
                st.error("Link do Google Sheets é obrigatório")
                return False
            
            # Validar email
            if not auth._validate_email(email_clinica):
                st.error("Email inválido")
                return False
            
            # Validar senha
            if not auth._validate_password(senha_clinica):
                st.error("Senha deve ter pelo menos 6 caracteres")
                return False
            
            try:
                cliente = cliente_crud.create_cliente(
                    nome=nome_responsavel.strip(),
                    email=email_clinica.strip().lower(),
                    senha=senha_clinica,
                    cnpj=cnpj.strip() if cnpj else None,
                    nome_da_clinica=nome_da_clinica.strip(),
                    telefone=telefone.strip() if telefone else None,
                    endereco=endereco.strip() if endereco else None,
                    link_empresa=link_empresa.strip() if link_empresa else None
                )
                
                if cliente:
                    st.success(f"✅ Clínica '{nome_da_clinica}' cadastrada com sucesso!")
                    st.info(f"📧 Email: {email_clinica}")
                    st.info(f"🔑 Senha: {senha_clinica}")
                    st.info("A clínica pode agora fazer login com essas credenciais")
                    return True
                else:
                    st.error("Email já cadastrado")
                    return False
            except Exception as e:
                st.error(f"Erro no cadastro: {str(e)}")
                return False
    
    return False

def show_auth_page():
    """Exibe página de autenticação com opções de login e registro"""
    st.title("🏥 Prestige Clinic Dashboard")
    st.markdown("Sistema de análise de performance para clínicas estéticas")
    
    # Verificar se há admin cadastrado
    clientes = cliente_crud.get_all_clientes()
    has_admin = any(c.is_admin for c in clientes)
    
    if has_admin:
        # Se já existe admin, mostrar apenas login
        st.info("👑 Sistema já configurado. Faça login para acessar.")
        show_login_form()
    else:
        # Se não existe admin, mostrar opções de configuração inicial
        st.warning("⚠️ Primeira execução: Configure o administrador do sistema")
        
        tab1, tab2 = st.tabs(["🔐 Login", "👑 Configurar Admin"])
        
        with tab1:
            show_login_form()
        
        with tab2:
            st.subheader("👑 Configuração do Administrador")
            st.info("Configure o primeiro usuário como administrador do sistema.")
            
            with st.form("admin_setup_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    admin_nome = st.text_input("Nome do Administrador *", placeholder="Seu nome completo")
                    admin_email = st.text_input("Email do Admin *", placeholder="admin@prestigeclinic.com")
                    admin_senha = st.text_input("Senha do Admin *", type="password", placeholder="Mínimo 6 caracteres")
                
                with col2:
                    admin_confirmar_senha = st.text_input("Confirmar Senha *", type="password")
                
                submit_admin = st.form_submit_button("Criar Administrador", use_container_width=True)
                
                if submit_admin:
                    if not admin_nome.strip():
                        st.error("Nome é obrigatório")
                    elif not admin_email.strip():
                        st.error("Email é obrigatório")
                    elif not admin_senha.strip():
                        st.error("Senha é obrigatória")
                    elif admin_senha != admin_confirmar_senha:
                        st.error("Senhas não coincidem")
                    else:
                        try:
                            admin = cliente_crud.create_cliente(
                                nome=admin_nome.strip(),
                                email=admin_email.strip().lower(),
                                senha=admin_senha,
                                nome_da_clinica="Administrador",
                                is_admin=True
                            )
                            
                            if admin:
                                st.success("✅ Administrador criado com sucesso!")
                                st.info("Agora você pode fazer login como administrador")
                                st.rerun()
                            else:
                                st.error("Erro ao criar administrador")
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")

def require_auth(func):
    """
    Decorator para exigir autenticação em funções
    """
    def wrapper(*args, **kwargs):
        auth = AuthManager()
        if not auth.is_authenticated():
            show_auth_page()
            return
        return func(*args, **kwargs)
    return wrapper

def show_logout_button():
    """Exibe botão de logout na sidebar"""
    auth = AuthManager()
    if auth.is_authenticated():
        user = auth.get_current_user()
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Usuário:** {user['nome']}")
        st.sidebar.markdown(f"**Clínica:** {user['nome_da_clinica']}")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            auth.logout()

def show_admin_panel():
    """Exibe painel administrativo para seleção de clientes"""
    auth = AuthManager()
    if not auth.is_admin():
        return None
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("👑 Painel Administrativo")
    
    # Botões sempre visíveis
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("➕ Nova Clínica", use_container_width=True):
            st.session_state['show_admin_register'] = True
            st.session_state['show_clinic_management'] = False
            st.session_state['show_admin_dashboard'] = False
            st.rerun()
    
    with col2:
        if st.button("🏥 Gerenciar", use_container_width=True):
            st.session_state['show_admin_register'] = False
            st.session_state['show_clinic_management'] = True
            st.session_state['show_admin_dashboard'] = False
            st.rerun()
    
    # Botão para dashboard consolidado (largura completa)
    if st.sidebar.button("📊 Dashboard Consolidado", use_container_width=True):
        st.session_state['show_admin_register'] = False
        st.session_state['show_clinic_management'] = False
        st.session_state['show_admin_dashboard'] = True
        st.rerun()
    
    # Se está mostrando o formulário de cadastro
    if st.session_state.get('show_admin_register', False):
        return 'admin_register'
    
    # Se está mostrando o painel de gerenciamento
    if st.session_state.get('show_clinic_management', False):
        return 'clinic_management'
    
    # Se está mostrando o dashboard consolidado
    if st.session_state.get('show_admin_dashboard', False):
        return 'admin_dashboard'
    
    # Lista todos os clientes (excluindo admin)
    clientes = cliente_crud.get_all_clientes()
    clientes_nao_admin = [c for c in clientes if not c.is_admin]
    
    if not clientes_nao_admin:
        st.sidebar.warning("Nenhum cliente cadastrado")
        return None
    
    # Cria opções para seleção (apenas clínicas, não admin)
    opcoes = {f"{c.nome} - {c.nome_da_clinica}": c.id for c in clientes_nao_admin}
    
    cliente_selecionado = st.sidebar.selectbox(
        "Selecionar Clínica:",
        options=list(opcoes.keys()),
        index=0
    )
    
    return opcoes[cliente_selecionado]

def show_edit_clinic_form(cliente):
    """Exibe formulário de edição de clínica"""
    st.markdown("### ✏️ Editar Clínica")
    
    with st.form(f"edit_form_{cliente.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome", value=cliente.nome, key=f"edit_nome_{cliente.id}")
            email = st.text_input("Email", value=cliente.email, key=f"edit_email_{cliente.id}")
            cnpj = st.text_input("CNPJ", value=cliente.cnpj or "", key=f"edit_cnpj_{cliente.id}")
            telefone = st.text_input("Telefone", value=cliente.telefone or "", key=f"edit_telefone_{cliente.id}")
        
        with col2:
            nome_da_clinica = st.text_input("Nome da Clínica", value=cliente.nome_da_clinica, key=f"edit_nome_da_clinica_{cliente.id}")
            endereco = st.text_area("Endereço", value=cliente.endereco or "", key=f"edit_endereco_{cliente.id}")
            link_empresa = st.text_input("Link da Empresa", value=cliente.link_empresa or "", key=f"edit_link_empresa_{cliente.id}")
            nova_senha = st.text_input("Nova Senha (deixe em branco para manter)", type="password", key=f"edit_senha_{cliente.id}")
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            if st.form_submit_button("💾 Salvar Alterações", type="primary"):
                # Preparar dados para atualização
                update_data = {
                    'nome': nome.strip(),
                    'email': email.strip().lower(),
                    'cnpj': cnpj.strip() if cnpj else None,
                    'telefone': telefone.strip() if telefone else None,
                    'nome_da_clinica': nome_da_clinica.strip(),
                    'endereco': endereco.strip() if endereco else None,
                    'link_empresa': link_empresa.strip() if link_empresa else None
                }
                
                # Adicionar senha apenas se fornecida
                if nova_senha.strip():
                    update_data['senha'] = nova_senha.strip()
                
                # Atualizar cliente
                auth = AuthManager()
                success, message = auth.update_cliente(cliente.id, **update_data)
                
                if success:
                    st.success(message)
                    st.session_state[f"editing_cliente_{cliente.id}"] = False
                    st.rerun()
                else:
                    st.error(message)
        
        with col_cancel:
            if st.form_submit_button("❌ Cancelar"):
                st.session_state[f"editing_cliente_{cliente.id}"] = False
                st.rerun()

def show_delete_confirmation(cliente):
    """Exibe confirmação de exclusão de clínica"""
    st.markdown("### 🗑️ Confirmar Exclusão")
    st.warning(f"⚠️ Tem certeza que deseja excluir a clínica **{cliente.nome_da_clinica}**?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Sim, Excluir", key=f"confirm_delete_{cliente.id}", type="primary"):
            auth = AuthManager()
            success, message = auth.delete_cliente(cliente.id, hard_delete=False)
            
            if success:
                st.success(message)
                st.session_state[f"confirming_delete_{cliente.id}"] = False
                st.rerun()
            else:
                st.error(message)
    
    with col2:
        if st.button("❌ Cancelar", key=f"cancel_delete_{cliente.id}"):
            st.session_state[f"confirming_delete_{cliente.id}"] = False
            st.rerun()
    
    with col3:
        if st.button("🔥 Exclusão Permanente", key=f"hard_delete_{cliente.id}", type="secondary"):
            auth = AuthManager()
            success, message = auth.delete_cliente(cliente.id, hard_delete=True)
            
            if success:
                st.success(message)
                st.session_state[f"confirming_delete_{cliente.id}"] = False
                st.rerun()
            else:
                st.error(message)

def show_clinic_management_panel():
    """Exibe painel completo de gerenciamento de clínicas"""
    st.title("🏥 Gerenciamento de Clínicas")
    
    # Botões de navegação
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("➕ Nova Clínica", use_container_width=True, key="nav_nova_from_management"):
            st.session_state['show_admin_register'] = True
            st.session_state['show_clinic_management'] = False
            st.rerun()
    
    with col_nav2:
        if st.button("📊 Dashboard Consolidado", use_container_width=True, key="nav_dashboard_from_management"):
            st.session_state['show_admin_register'] = False
            st.session_state['show_clinic_management'] = False
            st.session_state['show_admin_dashboard'] = True
            st.rerun()
    
    with col_nav3:
        if st.button("👥 Ver Clínicas", use_container_width=True, key="nav_ver_from_management"):
            st.session_state['show_clinic_management'] = False
            st.rerun()
    
    st.markdown("---")
    
    # Estatísticas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_clientes = len(cliente_crud.get_all_clientes())
        st.metric("Total de Clínicas", total_clientes)
    
    with col2:
        clientes_ativos = len([c for c in cliente_crud.get_all_clientes() if c.ativo])
        st.metric("Clínicas Ativas", clientes_ativos)
    
    with col3:
        st.metric("Sistema", "✅ Online")
    
    st.markdown("---")
    
    # Lista de clínicas com ações
    st.subheader("📋 Lista de Clínicas")
    
    clientes = cliente_crud.get_all_clientes()
    if clientes:
        # Filtros
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            status_filter = st.selectbox("Filtrar por Status", ["Todos", "Ativos", "Inativos"])
        
        with col_filter2:
            search_term = st.text_input("🔍 Buscar por nome ou clínica")
        
        # Aplicar filtros
        clientes_filtrados = clientes
        if status_filter == "Ativos":
            clientes_filtrados = [c for c in clientes_filtrados if c.ativo]
        elif status_filter == "Inativos":
            clientes_filtrados = [c for c in clientes_filtrados if not c.ativo]
        
        if search_term:
            clientes_filtrados = [c for c in clientes_filtrados 
                                if search_term.lower() in c.nome.lower() 
                                or search_term.lower() in c.nome_da_clinica.lower()]
        
        # Exibir clínicas
        for cliente in clientes_filtrados:
            with st.expander(f"{'✅' if cliente.ativo else '❌'} {cliente.nome_da_clinica} - {cliente.nome}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**📧 Email:** {cliente.email}")
                    st.write(f"**📄 CNPJ:** {cliente.cnpj or 'Não informado'}")
                    st.write(f"**📞 Telefone:** {cliente.telefone or 'Não informado'}")
                    st.write(f"**📍 Endereço:** {cliente.endereco or 'Não informado'}")
                    st.write(f"**🔗 Link da Empresa:** {cliente.link_empresa or 'Não informado'}")
                    st.write(f"**📅 Criado em:** {cliente.data_criacao.strftime('%d/%m/%Y %H:%M')}")
                
                with col2:
                    # Botões de ação
                    if st.button(f"✏️ Editar", key=f"edit_btn_{cliente.id}", type="primary"):
                        st.session_state[f"editing_cliente_{cliente.id}"] = True
                        st.rerun()
                    
                    if st.button(f"🗑️ Excluir", key=f"delete_btn_{cliente.id}", type="secondary"):
                        st.session_state[f"confirming_delete_{cliente.id}"] = True
                        st.rerun()
                    
                    if not cliente.ativo:
                        if st.button(f"🔄 Reativar", key=f"reactivate_btn_{cliente.id}"):
                            auth = AuthManager()
                            success, message = auth.update_cliente(cliente.id, ativo=True)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                
                # Formulário de edição
                if st.session_state.get(f"editing_cliente_{cliente.id}", False):
                    show_edit_clinic_form(cliente)
                
                # Confirmação de exclusão
                if st.session_state.get(f"confirming_delete_{cliente.id}", False):
                    show_delete_confirmation(cliente)
    else:
        st.info("Nenhuma clínica cadastrada")
    
    st.markdown("---")
    
    # Formulário para nova clínica
    st.subheader("➕ Cadastrar Nova Clínica")
    show_admin_register_clinic_form()

