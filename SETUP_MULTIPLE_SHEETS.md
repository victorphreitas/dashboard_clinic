# 🔧 Configuração do Google Sheets - Múltiplas Clínicas

## 📋 Status Atual

- ✅ **Credenciais configuradas**: `google_credentials.json`
- ✅ **Autenticação funcionando**: Conta de serviço ativa
- ❌ **Acesso às planilhas**: Precisam ser compartilhadas

## 🎯 Próximos Passos

### 1. Compartilhar as Planilhas

#### Planilha Dr. João Silva:

- **URL**: https://docs.google.com/spreadsheets/d/1hZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk
- **ID**: 1hZuf0UYkMX8txqfXOZPf-BoVs

#### Planilha Dra Taynah Bastos:

- **URL**: https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk
- **ID**: 1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs

### 2. Adicionar Permissão em AMBAS as planilhas

1. Clique em **"Compartilhar"** (canto superior direito)
2. Adicione o email: `dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com`
3. Defina permissão como **"Editor"** ou **"Visualizador"**
4. Clique em **"Enviar"**

### 3. Importar Dados de Ambas as Clínicas

```bash
cd /home/victor/Desktop/Projects/dashboards/prestige_clinic_dash
source venv/bin/activate
python import_multiple_sheets.py
```

## 📊 Estrutura Esperada das Planilhas

### 🔄 **Importante: Todas as Abas são Processadas**

O script agora acessa **TODAS as abas** de cada planilha, não apenas a primeira. Cada aba deve ter as seguintes colunas:

- `mes` - Nome do mês (Janeiro, Fevereiro, etc.)
- `leads_totais` - Total de leads
- `leads_google_ads` - Leads do Google Ads
- `leads_meta_ads` - Leads do Meta Ads
- `leads_instagram_organico` - Leads do Instagram Orgânico
- `leads_indicacao` - Leads por indicação
- `leads_origem_desconhecida` - Leads de origem desconhecida
- `consultas_marcadas_totais` - Total de consultas marcadas
- `consultas_marcadas_google_ads` - Consultas do Google Ads
- `consultas_marcadas_meta_ads` - Consultas do Meta Ads
- `consultas_marcadas_ig_organico` - Consultas do Instagram Orgânico
- `consultas_marcadas_indicacao` - Consultas por indicação
- `consultas_marcadas_outros` - Outras consultas
- `consultas_comparecidas` - Consultas comparecidas
- `fechamentos_totais` - Total de fechamentos
- `fechamentos_google_ads` - Fechamentos do Google Ads
- `fechamentos_meta_ads` - Fechamentos do Meta Ads
- `fechamentos_ig_organico` - Fechamentos do Instagram Orgânico
- `fechamentos_indicacao` - Fechamentos por indicação
- `fechamentos_outros` - Outros fechamentos
- `faturamento` - Faturamento total
- `investimento_total` - Investimento total
- `investimento_facebook` - Investimento no Facebook
- `investimento_google` - Investimento no Google

## 🔍 Verificação

### Email da Conta de Serviço:

`dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com`

### IDs das Planilhas:

- **Dr. João**: `1hZuf0UYkMX8txqfXOZPf-BoVs`
- **Dra Taynah**: `1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs`

### URLs das Planilhas:

- **Dr. João**: https://docs.google.com/spreadsheets/d/1hZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk
- **Dra Taynah**: https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk

## ✅ Após Configuração

Quando ambas as planilhas forem compartilhadas corretamente:

1. Execute `python import_multiple_sheets.py` - importará dados de **TODAS as abas** de ambas as clínicas
2. Ambas as clínicas terão seus dados reais no dashboard
3. Sistema funcionará com dados reais do Google Sheets

## 🔄 Como Funciona o Processamento de Múltiplas Abas

### 📋 **Processo de Importação:**

1. **Acessa a planilha** usando o ID fornecido
2. **Lista todas as abas** disponíveis na planilha
3. **Processa cada aba** individualmente
4. **Combina todos os dados** de todas as abas
5. **Importa para o banco** de dados

### 📊 **Exemplo de Estrutura:**

```
Planilha Dr. João:
├── Aba 1: Janeiro
├── Aba 2: Fevereiro
├── Aba 3: Março
└── Aba 4: Abril

Planilha Dra Taynah:
├── Aba 1: Janeiro
├── Aba 2: Fevereiro
└── Aba 3: Março
```

### ✅ **Resultado:**

- **Dr. João**: Dados de Janeiro, Fevereiro, Março e Abril
- **Dra Taynah**: Dados de Janeiro, Fevereiro e Março
- **Dashboard**: Mostra todos os meses com dados

## 🚨 Importante

- **Compartilhe AMBAS as planilhas** com a conta de serviço
- **Não compartilhe** o arquivo `google_credentials.json`
- **Mantenha** as credenciais seguras
- **Use** apenas para este projeto

## 📋 Credenciais de Acesso

- **👑 Admin**: admin@prestigeclinic.com / admin123
- **🏥 Dr. João**: joao@clinicaestetica.com / clinica123
- **🏥 Dra Taynah**: taynah@cirurgiaplastica.com / taynah2024
