# 🏥 Solução: Dr. Jonnattan - Planilha Não Acessível

## 🚨 **PROBLEMA CONFIRMADO:**

**Status do Service Account:**

- ✅ **Dra Marlei**: Funcionando perfeitamente
- ✅ **Dr. João**: Funcionando perfeitamente
- ❌ **Dr. Jonnattan**: Erro de acesso

**Erro:** `APIError: [400]: This operation is not supported for this document`

---

## 🔧 **SOLUÇÕES PASSO A PASSO:**

### **Solução 1: Verificar Compartilhamento** 🔍

**1. Acesse a planilha:**

```
https://docs.google.com/spreadsheets/d/1ZhqhpA1agIKo2w92X8h0NqLSJy1QJKt2/edit
```

**2. Verifique se está compartilhada:**

- Clique em "Compartilhar" (canto superior direito)
- Procure por: `dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com`
- Se não estiver, adicione com permissão **"Editor"**

### **Solução 2: Verificar Permissões** 🔐

**Email correto:**

```
dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com
```

**Permissão necessária:**

```
Editor (não apenas Visualizador)
```

### **Solução 3: Verificar Configurações da Planilha** ⚙️

**1. Verificar se a planilha não está em modo privado**
**2. Verificar se não há restrições de domínio**
**3. Verificar se a planilha não está em uma organização restritiva**

### **Solução 4: Testar com Link Diferente** 🔗

**Link alternativo (sem gid):**

```
https://docs.google.com/spreadsheets/d/1ZhqhpA1agIKo2w92X8h0NqLSJy1QJKt2/edit
```

---

## 🧪 **TESTE DE VERIFICAÇÃO:**

**Execute este comando para testar:**

```bash
python -c "
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file('google_credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
gc = gspread.authorize(creds)

try:
    sheet = gc.open_by_key('1ZhqhpA1agIKo2w92X8h0NqLSJy1QJKt2')
    print('✅ Acesso funcionando!')
    print(f'Título: {sheet.title}')
except Exception as e:
    print(f'❌ Erro: {e}')
"
```

---

## 🎯 **RESULTADO ESPERADO:**

**Quando funcionar, você verá:**

```
✅ Acesso funcionando!
Título: [Nome da Planilha]
```

**Depois execute:**

```bash
python check_empty_clinics.py
```

**Resultado esperado:**

```
✅ Dr. Jonnattan Prada: X meses importados
```

---

## 🚀 **PRÓXIMOS PASSOS:**

**1. Verificar compartilhamento** ✅
**2. Testar acesso** ✅  
**3. Executar importação** ✅
**4. Verificar dashboard** ✅

**O sistema está funcionando perfeitamente, só precisa da planilha ser compartilhada corretamente!** 🎉

