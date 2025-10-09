# 🚀 Guia de Deploy - Render.com

Este guia explica como fazer o deploy da aplicação Dashboard Clínica Estética no Render.com usando Docker.

## 📋 Pré-requisitos

1. **Conta no Render.com** (gratuita)
2. **Repositório Git** (GitHub, GitLab, ou Bitbucket)
3. **Credenciais do Google Sheets** configuradas

## 🔧 Configuração do Projeto

### 1. Estrutura de Arquivos

```
prestige_clinic_dash/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── render.yaml
├── app.py
├── dashboard.py
├── database.py
├── models.py
├── auth.py
└── ... (outros arquivos)
```

### 2. Variáveis de Ambiente Necessárias

No Render.com, configure as seguintes variáveis de ambiente:

#### **Obrigatórias:**

- `GOOGLE_CREDENTIALS_JSON`: JSON das credenciais do Google Service Account
- `SECRET_KEY`: Chave secreta para sessões (gerar uma nova)

#### **Opcionais:**

- `DATABASE_URL`: URL do banco PostgreSQL (se usar banco externo)
- `STREAMLIT_SERVER_PORT`: 10000 (padrão)
- `STREAMLIT_SERVER_ADDRESS`: 0.0.0.0 (padrão)

## 🐳 Deploy no Render.com

### Passo 1: Preparar o Repositório

1. **Commit todos os arquivos:**

```bash
git add .
git commit -m "Add Docker configuration for Render.com deploy"
git push origin main
```

### Passo 2: Criar Serviço no Render.com

1. **Acesse [render.com](https://render.com)**
2. **Clique em "New +"**
3. **Selecione "Web Service"**
4. **Conecte seu repositório Git**

### Passo 3: Configurar o Serviço

#### **Configurações Básicas:**

- **Name**: `prestige-clinic-dashboard`
- **Environment**: `Docker`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Dockerfile Path**: `./Dockerfile`
- **Docker Context**: `.`

#### **Configurações Avançadas:**

- **Plan**: `Starter` (gratuito)
- **Auto-Deploy**: `Yes`
- **Health Check Path**: `/_stcore/health`

### Passo 4: Configurar Variáveis de Ambiente

No painel do Render.com, vá em **Environment** e adicione:

```bash
# Google Sheets Credentials (JSON completo)
GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"..."}

# Secret Key (gerar uma nova)
SECRET_KEY=your-secret-key-here

# Streamlit Configuration
STREAMLIT_SERVER_PORT=10000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Passo 5: Deploy

1. **Clique em "Create Web Service"**
2. **Aguarde o build** (5-10 minutos)
3. **Acesse a URL** fornecida pelo Render

## 🔐 Configuração das Credenciais do Google

### 1. Obter Credenciais JSON

1. **Acesse [Google Cloud Console](https://console.cloud.google.com)**
2. **Crie um projeto** ou selecione existente
3. **Ative a Google Sheets API**
4. **Crie uma Service Account**
5. **Baixe o JSON** das credenciais

### 2. Configurar no Render.com

1. **Copie todo o conteúdo do JSON**
2. **Cole na variável `GOOGLE_CREDENTIALS_JSON`**
3. **Remova quebras de linha** (deve ser uma linha só)

### 3. Compartilhar Planilhas

Para cada planilha do Google Sheets:

1. **Abra a planilha**
2. **Clique em "Compartilhar"**
3. **Adicione o email da Service Account** como Editor
4. **Email da Service Account**: `dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com`

## 📊 Monitoramento e Logs

### 1. Logs da Aplicação

- **Render Dashboard** → **Logs**
- **Filtre por nível**: Error, Warning, Info

### 2. Health Check

- **URL**: `https://your-app.onrender.com/_stcore/health`
- **Status**: Deve retornar 200 OK

### 3. Métricas

- **CPU Usage**: Monitor no dashboard
- **Memory Usage**: Verificar se não excede limite
- **Response Time**: Deve ser < 2 segundos

## 🔧 Troubleshooting

### Problemas Comuns:

#### **1. Build Falha**

```bash
# Verificar logs de build
# Problema comum: requirements.txt com versões incompatíveis
```

#### **2. Aplicação Não Inicia**

```bash
# Verificar variáveis de ambiente
# Verificar se GOOGLE_CREDENTIALS_JSON está correto
```

#### **3. Erro de Google Sheets**

```bash
# Verificar se planilhas estão compartilhadas
# Verificar se JSON das credenciais está correto
```

#### **4. Timeout de Deploy**

```bash
# Aumentar timeout no render.yaml
# Otimizar Dockerfile
```

## 🚀 Otimizações de Produção

### 1. Performance

- **Cache**: Usar `@st.cache_data` para funções pesadas
- **Database**: Considerar PostgreSQL para produção
- **CDN**: Usar CloudFlare para assets estáticos

### 2. Segurança

- **HTTPS**: Automático no Render.com
- **Secrets**: Nunca commitar credenciais
- **Rate Limiting**: Implementar se necessário

### 3. Escalabilidade

- **Plan Upgrade**: Para mais recursos
- **Database**: PostgreSQL para múltiplos usuários
- **Load Balancing**: Para alta disponibilidade

## 📱 Acessando a Aplicação

### URL de Produção:

```
https://prestige-clinic-dashboard.onrender.com
```

### Usuários de Teste:

- **Admin**: `admin@prestige.com` / `admin123`
- **Clínica**: `joao@clinica.com` / `joao123`

## 🔄 Atualizações

### Deploy Automático:

1. **Push para main** → Deploy automático
2. **Monitor logs** durante deploy
3. **Testar funcionalidades** após deploy

### Deploy Manual:

1. **Render Dashboard** → **Manual Deploy**
2. **Selecionar branch** → **Deploy**

## 📞 Suporte

### Logs Importantes:

- **Build Logs**: Erros de dependências
- **Runtime Logs**: Erros de aplicação
- **Health Check**: Status da aplicação

### Contato:

- **Render Support**: [help.render.com](https://help.render.com)
- **Documentação**: [render.com/docs](https://render.com/docs)

---

## ✅ Checklist de Deploy

- [ ] Repositório Git configurado
- [ ] Dockerfile criado
- [ ] requirements.txt atualizado
- [ ] render.yaml configurado
- [ ] Variáveis de ambiente definidas
- [ ] Credenciais Google configuradas
- [ ] Planilhas compartilhadas
- [ ] Deploy realizado
- [ ] Health check funcionando
- [ ] Aplicação acessível
- [ ] Funcionalidades testadas

**🎉 Deploy Concluído com Sucesso!**
