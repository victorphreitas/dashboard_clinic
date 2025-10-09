# 🔧 Configuração do Google Sheets - Dra Taynah Bastos

## 📋 Status Atual

- ✅ **Credenciais configuradas**: `google_credentials.json`
- ✅ **Autenticação funcionando**: Conta de serviço ativa
- ❌ **Acesso à planilha**: Precisa ser compartilhada

## 🎯 Próximos Passos

### 1. Compartilhar a Planilha

Acesse: https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk

### 2. Adicionar Permissão

1. Clique em **"Compartilhar"** (canto superior direito)
2. Adicione o email: `dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com`
3. Defina permissão como **"Editor"** ou **"Visualizador"**
4. Clique em **"Enviar"**

### 3. Testar Acesso

```bash
cd /home/victor/Desktop/Projects/dashboards/prestige_clinic_dash
source venv/bin/activate
python test_google_auth.py
```

### 4. Importar Dados

```bash
python import_google_sheets.py
```

## 📊 Estrutura Esperada da Planilha

A planilha deve ter as seguintes colunas:

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

### ID da Planilha:

`1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs`

### URL da Planilha:

https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk

## ✅ Após Configuração

Quando a planilha for compartilhada corretamente:

1. Execute `python test_google_auth.py` - deve mostrar "✅ Dados acessíveis!"
2. Execute `python import_google_sheets.py` - deve importar dados reais
3. A Dra Taynah terá seus dados reais no dashboard

## 🚨 Importante

- **Não compartilhe** o arquivo `google_credentials.json`
- **Mantenha** as credenciais seguras
- **Use** apenas para este projeto
