"""
Sistema de autenticação e controle de sessão.
Gerencia login, logout, registro e controle de acesso.
"""

import streamlit as st
from typing import Optional, Dict, Any
import re
from database import cliente_crud, Cliente

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
    
    # Botão para cadastrar nova clínica
    if st.sidebar.button("➕ Cadastrar Nova Clínica", use_container_width=True):
        st.session_state['show_admin_register'] = True
        st.rerun()
    
    # Se está mostrando o formulário de cadastro
    if st.session_state.get('show_admin_register', False):
        if st.sidebar.button("← Voltar", use_container_width=True):
            st.session_state['show_admin_register'] = False
            st.rerun()
        return 'admin_register'
    
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

