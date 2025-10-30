# 📊 Análise de Procedimentos - Nova Funcionalidade

## 🎯 Objetivo

Esta nova funcionalidade adiciona uma seção completa de análise de procedimentos ao dashboard, permitindo visualizar dados detalhados sobre:

- **Data do primeiro contato**
- **Data que compareceu na consulta**
- **Data que fechou a cirurgia**
- **Procedimento realizado**
- **Tipo de procedimento**
- **Quantidade na mesma venda**
- **Forma de pagamento**
- **Valor da venda**
- **Valor do parcelado**

## 🏗️ Estrutura Implementada

### 1. **Modelo de Dados** (`models.py`)

- Nova tabela `procedimentos` com todos os campos necessários
- Relacionamento com a tabela `clientes`
- Campos de data, valores monetários e metadados

### 2. **CRUD de Procedimentos** (`database.py`)

- Classe `ProcedimentoCRUD` com operações completas
- Funções para criar, buscar, atualizar e deletar procedimentos
- Conversão para DataFrame do pandas

### 3. **Importação do Google Sheets** (`import_procedimentos.py`)

- Script para importar dados da aba "Procedimentos"
- Processamento automático de datas e valores monetários
- Suporte a diferentes formatos de data e moeda

### 4. **Visualizações** (`dashboard.py`)

- Função `create_procedimentos_analysis()` com análises completas
- KPIs principais: total de procedimentos, faturamento, ticket médio, taxa de fechamento
- Gráficos por tipo, mês, forma de pagamento
- Tabela detalhada com todos os procedimentos

### 5. **Integração no Dashboard** (`app.py`)

- Nova seção "🏥 Análise de Procedimentos" no dashboard principal
- Filtros por mês aplicados aos procedimentos
- Carregamento automático dos dados

## 📋 Como Usar

### **1. Migração do Banco de Dados**

```bash
python migrate_procedimentos.py
```

### **2. Importação de Dados**

```bash
# Para importar de todas as clínicas
python import_procedimentos.py

# Para importar de uma clínica específica
python -c "from import_procedimentos import load_procedimentos_for_cliente; from database import cliente_crud; cliente = cliente_crud.get_all_clientes()[0]; load_procedimentos_for_cliente(cliente)"
```

### **3. Dados de Exemplo**

```bash
python create_sample_procedimentos.py
```

## 📊 Estrutura da Aba "Procedimentos" no Google Sheets

A aba deve ter os seguintes cabeçalhos:

| Coluna                    | Descrição                | Exemplo                          |
| ------------------------- | ------------------------ | -------------------------------- |
| Data 1° Contato           | Data do primeiro contato | 16/10/2024                       |
| Data Compareu na Consulta | Data da consulta         | 16/10/2024                       |
| Data Fechou Cirurgia      | Data do fechamento       | 16/10/2024                       |
| Procedimento              | Nome do procedimento     | Mommy Makeover, Lipo HD          |
| Tipo                      | Tipo do procedimento     | Cosmiatria, Cirúrgico            |
| Quantidade na Mesma Venda | Quantidade               | 2                                |
| Forma de Pagamento        | Forma de pagamento       | Parcelado no Pix (Financiamento) |
| Valor da Venda            | Valor total              | R$ 20.000,00                     |
| Valor do Parcelado        | Valor parcelado          | R$ 1.000,00                      |

## 🎨 Visualizações Disponíveis

### **KPIs Principais**

- Total de Procedimentos
- Faturamento Total
- Ticket Médio
- Procedimentos Fechados (com taxa de conversão)

### **Análise por Tipo**

- Gráfico de pizza: Distribuição por tipo
- Gráfico de barras: Faturamento por tipo

### **Análise Temporal**

- Procedimentos por mês
- Faturamento por mês

### **Análise de Pagamento**

- Distribuição por forma de pagamento
- Faturamento por forma de pagamento

### **Tabela Detalhada**

- Todos os procedimentos com formatação adequada
- Filtros aplicados pelos meses selecionados

## 🔧 Configuração

### **Variáveis de Ambiente**

Certifique-se de que `GOOGLE_SHEETS_CREDENTIALS` está configurado no arquivo `.env`:

```env
GOOGLE_SHEETS_CREDENTIALS={"type": "service_account", "project_id": "...", ...}
```

### **Estrutura da Planilha**

- A planilha deve ter uma aba chamada "Procedimentos"
- Os cabeçalhos devem estar na primeira linha
- Os dados devem começar na segunda linha

## 🚀 Próximos Passos

1. **Teste a funcionalidade** com os dados de exemplo
2. **Configure a aba "Procedimentos"** nas planilhas das clínicas
3. **Execute a importação** dos dados reais
4. **Verifique as visualizações** no dashboard

## 📝 Notas Importantes

- Os dados de procedimentos são filtrados pelos meses selecionados na sidebar
- A importação substitui todos os dados existentes de procedimentos
- As datas são processadas automaticamente em diferentes formatos
- Os valores monetários são convertidos automaticamente
- A funcionalidade está totalmente integrada ao sistema de autenticação existente

## 🎉 Resultado Final

A nova seção "🏥 Análise de Procedimentos" aparece no dashboard principal, após a seção de "Tendências e Sazonalidade", fornecendo uma visão completa e detalhada de todos os procedimentos realizados pelas clínicas.
