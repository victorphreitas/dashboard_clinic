# 📋 Guia: Como Compartilhar as Planilhas do Google Sheets

## 🎯 **Objetivo**

Compartilhar as planilhas com a conta de serviço para que o sistema possa acessar os dados reais.

## 📧 **Email da Conta de Serviço**

```
dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com
```

## 🔗 **Links das Planilhas**

### 1. **Planilha Dr. João Silva**

- **URL**: https://docs.google.com/spreadsheets/d/1hZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk
- **ID**: 1hZuf0UYkMX8txqfXOZPf-BoVs

### 2. **Planilha Dra Taynah Bastos**

- **URL**: https://docs.google.com/spreadsheets/d/1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs/edit?usp=drivesdk
- **ID**: 1acueFut0Baft66fH7jTZuf0UYkMX8txqfXOZPf-BoVs

## 📝 **Passo a Passo**

### **Para cada planilha, faça:**

1. **Acesse o link da planilha**
2. **Clique em "Compartilhar"** (canto superior direito)
3. **Adicione o email**: `dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com`
4. **Defina permissão**: "Editor" ou "Visualizador"
5. **Clique em "Enviar"**

## 🔍 **Verificação**

Após compartilhar, execute:

```bash
cd /home/victor/Desktop/Projects/dashboards/prestige_clinic_dash
source venv/bin/activate
python test_sheets_access.py
```

## ✅ **Resultado Esperado**

Quando compartilhado corretamente, você verá:

```
✅ Planilha acessada: [Nome da Planilha]
📋 Abas encontradas: [Lista de abas]
📊 X registros encontrados
```

## 🚀 **Importar Dados Reais**

Após compartilhar, execute:

```bash
python import_multiple_sheets.py
```

## 🚨 **Importante**

- **Compartilhe AMBAS as planilhas**
- **Use o email exato**: `dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com`
- **Permissão**: Editor ou Visualizador
- **Não compartilhe** o arquivo `google_credentials.json`

## 📞 **Se tiver problemas**

1. Verifique se o email está correto
2. Confirme que a permissão foi dada
3. Teste novamente com `python test_sheets_access.py`
4. Se ainda não funcionar, verifique se a planilha existe e está acessível
