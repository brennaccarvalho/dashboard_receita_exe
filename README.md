# Analytics Dashboard

> Dashboard semanal de performance: Receita, Canais, Audiência, Cadastros e Checkout.

Painel de BI construído em **Streamlit + Plotly**, cobrindo os frameworks de KPIs e análises definidos na proposta. Desenvolvido para acompanhamento semanal de performance.

---

## Visão geral

| Aba | O que monitora |
|---|---|
| 💰 **Receita** | Receita total, ticket médio, ARR, mix pontual/assinatura, produtos, recompra |
| 📡 **Canais** | Receita e audiência por canal, taxa de conversão, GSC, e-mail, alertas |
| 👥 **Audiência** | Sessões, perfil do visitante em 3 dimensões, conexão audiência → receita |
| 📝 **Cadastros** | Funil de cadastro, score de qualidade, origem dos cadastros |
| 🛒 **Checkout** | Funil carrinho tradicional e compra rápida, recuperação de abandonados, segmentações |

---

## Rodando localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/analytics-dashboard.git
cd analytics-dashboard
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure segredos (opcional)

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 5. Rode o app

```bash
streamlit run app.py
```

Acesse em: [http://localhost:8501](http://localhost:8501)

---

## Deploy no Streamlit Cloud

1. Faça fork ou push do repositório no GitHub.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e clique em **New app**.
3. Selecione o repositório, branch `main` e arquivo `app.py`.
4. Em **Advanced settings**, adicione os segredos do `.streamlit/secrets.toml` se necessário.
5. Clique em **Deploy**.

---

## Estrutura do projeto

```text
analytics-dashboard/
├── app.py
├── db.py
├── queries.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
└── assets/
```

---

## Dependências principais

| Pacote | Versão mínima | Uso |
|---|---|---|
| `streamlit` | 1.32.0 | Framework do app |
| `plotly` | 5.18.0 | Gráficos interativos |
| `pandas` | 2.0.0 | Manipulação de dados |
| `numpy` | 1.24.0 | Cálculos numéricos |
| `psycopg2-binary` | 2.9.9 | Conexão direta com AWS Redshift |

---

## 🔌 Conectando dados reais

1. Copie o arquivo de exemplo:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. Preencha o arquivo com as credenciais do cluster Redshift:

```toml
[redshift]
host     = "meu-cluster.xxxx.us-east-1.redshift.amazonaws.com"
port     = 5439
database = "analytics"
user     = "username"
password = "password"
```

3. Inicie o app com `streamlit run app.py`.

4. Na sidebar, desative o toggle **Modo mock (sem Redshift)** para usar as queries reais.

5. Se o app não conseguir conectar, ele continua funcionando em modo seguro:
   - as consultas retornam `DataFrame` vazio;
   - o dashboard mostra `Sem dados para este período` nas seções afetadas;
   - o modo mock continua disponível mesmo sem credenciais.

### Observações importantes

- O app usa `psycopg2` direto, sem SQLAlchemy e sem `st.experimental_connection`.
- As credenciais são lidas de `st.secrets["redshift"]`.
- Se o cluster Redshift estiver em VPC privada ou com restrição de rede, a máquina que roda o Streamlit precisa ter acesso ao cluster.
- Se o cluster não for público, pode ser necessário configurar VPN, bastion, peering, Security Group ou whitelist de IP antes da conexão funcionar.

---

## Licença

Uso interno. Não distribuir externamente.
