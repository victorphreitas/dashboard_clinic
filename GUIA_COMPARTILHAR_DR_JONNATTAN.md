# 🏥 Guia: Compartilhar Planilha do Dr. Jonnattan

## 🚨 **PROBLEMA IDENTIFICADO:**

**Dr. Jonnattan Prada** foi cadastrado ontem, mas sua planilha não foi compartilhada com o service account.

**Status:**

- ✅ Clínica cadastrada no sistema
- ✅ Link da planilha configurado
- ❌ Planilha não compartilhada com service account
- ❌ 0 dados no dashboard

---

## 🔧 **SOLUÇÃO PASSO A PASSO:**

### **Passo 1: Acessar a Planilha** 📊

```
Link: https://docs.google.com/spreadsheets/d/1ZhqhpA1agIKo2w92X8h0NqLSJy1QJKt2/edit?gid=1445686101#gid=1445686101
```

### **Passo 2: Compartilhar com Service Account** 🔗

1. **Abra a planilha** no link acima
2. **Clique em "Compartilhar"** (canto superior direito)
3. **Adicione o email:**
   ```
   dashboard-prestige-clinic@mapa-bot-claro.iam.gserviceaccount.com
   ```
4. **Defina permissão:** Editor
5. **Clique em "Enviar"**

### **Passo 3: Verificar Compartilhamento** ✅

Após compartilhar, execute:

```bash
python check_empty_clinics.py
```

**Resultado esperado:**

```
✅ Dr. Jonnattan Prada: X meses importados
```

---

## 🎯 **RESULTADO ESPERADO:**

**Após compartilhar a planilha:**

- ✅ Sistema conseguirá acessar a planilha
- ✅ Dados serão importados automaticamente
- ✅ Dr. Jonnattan verá seus dados no dashboard
- ✅ Sistema funcionará normalmente

---

## 📊 **VERIFICAÇÃO:**

**Para verificar se funcionou:**

1. Execute: `python check_empty_clinics.py`
2. Execute: `python debug_dashboard.py`
3. Acesse o dashboard e verifique se os dados aparecem

---

## 🚀 **SISTEMA AUTOMATIZADO:**

**Agora o sistema tem:**

- ✅ **Detecção automática** de clínicas sem dados
- ✅ **Script de correção** automática
- ✅ **Verificação de acesso** às planilhas
- ✅ **Guia de solução** para problemas

**O sistema está preparado para detectar e corrigir automaticamente clínicas sem dados!** 🎉

