# 🔮 Analytics Dashboard

> Dashboard semanal de performance — Receita · Canais · Audiência · Cadastros · Checkout

Painel de BI construído em **Streamlit + Plotly**, cobrindo frameworks de KPIs e análises definidos em uma proposta. Desenvolvido para acompanhamento semanal de performance.

---

## 📸 Visão geral

| Aba | O que monitora |
|---|---|
| 💰 **Receita** | Receita total, ticket médio, ARR, mix pontual/assinatura, produtos, recompra |
| 📡 **Canais** | Receita e audiência por canal, taxa de conversão, GSC, e-mail, alertas |
| 👥 **Audiência** | Sessões, perfil do visitante em 3 dimensões, conexão audiência → receita |
| 📝 **Cadastros** | Funil de cadastro, score de qualidade, origem dos cadastros |
| 🛒 **Checkout** | Funil carrinho tradicional e compra rápida, recuperação de abandonados, segmentações |

---

## 🚀 Rodando localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/analytics-dashboard.git
cd analytics-dashboard
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure credenciais (opcional)

Caso queira conectar a fontes de dados reais:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edite .streamlit/secrets.toml com suas credenciais
```

### 5. Rode o app

```bash
streamlit run app.py
```

Acesse em: [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deploy no Streamlit Cloud

1. Faça fork / push do repositório no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io) e clique em **"New app"**
3. Selecione o repositório, branch `main` e arquivo `app.py`
4. Em **"Advanced settings"**, adicione os segredos do `.streamlit/secrets.toml` se necessário
5. Clique em **Deploy** — o app fica disponível em um link público `*.streamlit.app`

---

## 🗂 Estrutura do projeto

```
analytics-dashboard/
│
├── app.py                        # Aplicação principal
├── requirements.txt              # Dependências Python
├── README.md
├── .gitignore
│
├── .streamlit/
│   ├── config.toml               # Tema dark + configurações do servidor
│   └── secrets.toml.example      # Template de credenciais (não commitado)
│
└── assets/                       # Fontes, imagens e estáticos locais
```

---

## 🎨 Design System

| Elemento | Fonte |
|---|---|
| Títulos / headers | `Aconchego` (local) → fallback `Georgia, serif` |
| Body / UI | `Figtree` via Google Fonts |
| Números / KPIs | `JetBrains Mono` |

**Paleta de cores:**

```
#151731  →  Navy (primary / background)
#760681  →  Roxo
#CE008D  →  Rosa (CTA / destaque)
#EF4D03  →  Laranja (alertas / atenção)
```

---

## 📦 Dependências principais

| Pacote | Versão mínima | Uso |
|---|---|---|
| `streamlit` | 1.32.0 | Framework do app |
| `plotly` | 5.18.0 | Gráficos interativos |
| `pandas` | 2.0.0 | Manipulação de dados |
| `numpy` | 1.24.0 | Cálculos numéricos |

---

## 🔌 Conectando dados reais

O `app.py` usa dados simulados (seed fixo para reprodutibilidade). Para usar dados reais, desative o toggle **"Usar dados mock (sem conexão)"** na barra lateral e implemente a função `get_data(use_mock=False)` no `app.py`.

Você pode carregar dados de qualquer fonte, por exemplo:

- **Google Analytics 4** → via `google-analytics-data`
- **Google Search Console** → via `google-search-console`
- **BigQuery / banco interno** → via `google-cloud-bigquery` ou `sqlalchemy`
- **Planilhas Google** → via `gspread`

Adicione credenciais no `.streamlit/secrets.toml` e acesse com `st.secrets["chave"]`.

---

## 📄 Licença

Uso interno. Não distribuir externamente.
