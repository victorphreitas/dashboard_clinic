# 🏥 Prestige Clinic Dashboard

Sistema de dashboard multiusuário para análise de performance de clínicas estéticas, com autenticação e banco de dados.

## 📁 Estrutura do Projeto

```
/prestige_clinic_dash
├── app.py                    # Ponto de entrada do Streamlit
├── dashboard.py              # Funções e gráficos de análise
├── auth.py                   # Sistema de autenticação
├── database.py               # Conexão e CRUD no banco
├── models.py                 # Definição das tabelas
├── seed_database.py          # Script para popular dados iniciais
├── requirements.txt          # Dependências do projeto
├── env_example.txt           # Exemplo de variáveis de ambiente
├── data/
│   └── seed_data.csv         # Dados iniciais de exemplo
└── README.md                 # Este arquivo
```

## 🚀 Como Executar

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Configuração do Banco de Dados

Execute o script para popular o banco com dados iniciais:

```bash
python seed_database.py
```

Este script criará:

- Um usuário administrador
- Uma clínica de exemplo com dados
- Tabelas do banco de dados

### 3. Executar a Aplicação

```bash
streamlit run app.py
```

## 👥 Usuários Padrão

Após executar o `seed_database.py`, você terá acesso com:

### 👑 Administrador

- **Email:** admin@prestigeclinic.com
- **Senha:** admin123
- **Permissões:** Pode visualizar dashboards de todas as clínicas
- **Função:** Administra o sistema, não possui clínica própria

### 🏥 Clínica de Exemplo

- **Email:** joao@clinicaestetica.com
- **Senha:** clinica123
- **Permissões:** Acesso apenas aos próprios dados

### 🏥 Dra Taynah Bastos (Cirurgia Plástica)

- **Email:** taynah@cirurgiaplastica.com
- **Senha:** taynah2024
- **Permissões:** Acesso apenas aos próprios dados
- **Google Sheets:** https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk

## 🔧 Funcionalidades

### ✅ Sistema de Autenticação

- Login e registro de novos clientes
- Controle de sessão
- Diferenciação entre usuários comuns e administradores

### 📊 Dashboard Multiusuário

- Cada cliente vê apenas seus próprios dados
- Administradores podem selecionar qualquer clínica
- Filtros por período (mês)
- Todas as visualizações originais mantidas

### 🗄️ Banco de Dados

- SQLite para desenvolvimento local
- Estrutura preparada para PostgreSQL em produção
- Dados isolados por cliente
- Sistema de CRUD completo

### 📈 Análises Disponíveis

- KPIs principais (leads, faturamento, fechamentos, ROAS)
- Análise do funil de conversão
- Performance por canal de aquisição
- Análise financeira (faturamento vs investimento)
- Análise de custos e eficiência
- Tendências mensais e sazonais
- Insights e recomendações

## 🛠️ Desenvolvimento

### Adicionando Novos Clientes

1. Registre-se através da interface web
2. Ou use o sistema de CRUD programaticamente:

```python
from database import cliente_crud

cliente = cliente_crud.create_cliente(
    nome="Nome do Cliente",
    email="email@cliente.com",
    senha="senha123",
    nome_da_clinica="Nome da Clínica"
)
```

### Adicionando Dados do Dashboard

```python
from database import dados_crud

dados = dados_crud.create_dados_dashboard(
    cliente_id=1,
    mes="Janeiro",
    leads_totais=100,
    faturamento=50000.0,
    # ... outros campos
)
```

## 🚀 Deploy

### Para Produção

1. **Banco de Dados:** Configure PostgreSQL
2. **Variáveis de Ambiente:** Configure `DATABASE_URL`
3. **Deploy:** Use Streamlit Cloud, Render, ou AWS

### Exemplo de Deploy no Streamlit Cloud

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático

## 📝 Notas Técnicas

- **Autenticação:** Senhas são hasheadas com bcrypt
- **Sessão:** Gerenciada pelo Streamlit session_state
- **Banco:** SQLAlchemy ORM com suporte a múltiplos SGBDs
- **Segurança:** Validação de entrada e sanitização de dados

## 🔒 Segurança

- Senhas hasheadas com bcrypt
- Validação de email e senha
- Controle de acesso por usuário
- Dados isolados por cliente

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs de erro
2. Confirme se o banco foi populado corretamente
3. Verifique as credenciais de acesso
