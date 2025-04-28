# API de Sistema de Crédito

Uma API RESTful para gerenciamento de scores de crédito e registros de dívidas.

## Visão Geral

Este projeto implementa um sistema de crédito simples com as seguintes funcionalidades:

-   Autenticação e autorização de usuários
-   Gerenciamento de registros de dívidas
-   Cálculo de score de crédito baseado no valor das dívidas

## Tecnologias Utilizadas

-   **Python**: Linguagem de programação principal
-   **FastAPI**: Framework para API
-   **PostgreSQL**: Banco de dados relacional
-   **SQLAlchemy**: ORM para interações com o banco de dados
-   **JWT**: Mecanismo de autenticação de usuários

## Estrutura do Projeto

```
credit-system/
├── app/
│   ├── __init__.py
│   ├── main.py            # Ponto de entrada da aplicação
│   ├── config.py          # Configurações do sistema
│   ├── database.py        # Conexão com o banco de dados
│   ├── models.py          # Modelos do banco de dados
│   ├── schemas.py         # Esquemas Pydantic
│   ├── auth.py            # Utilitários de autenticação
│   └── routers/           # Endpoints da API
│       ├── __init__.py
│       ├── users.py       # Gerenciamento de usuários
│       ├── debts.py       # Gerenciamento de registros de dívidas
│       └── score.py       # Cálculo de score de crédito
├── requirements.txt
└── README.md
```

## Requisitos

-   Python 3.8+
-   PostgreSQL
-   email-validator

## Configuração e Instalação

### Preparação do Banco de Dados

1. Instale o PostgreSQL:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

2. Inicie o serviço PostgreSQL:

```bash
sudo systemctl start postgresql
```

3. Crie um banco de dados e um usuário:

```bash
sudo -u postgres psql -c "CREATE DATABASE credit_db;"
sudo -u postgres psql -c "CREATE USER seu_usuario WITH PASSWORD 'sua_senha';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE credit_db TO seu_usuario;"
sudo -u postgres psql -c "GRANT ALL ON SCHEMA public TO seu_usuario;" credit_db
```

### Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/credit-system.git
cd credit-system
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente necessárias:

```bash
export DATABASE_URL="postgresql://seu_usuario:sua_senha@localhost/credit_db"
export SECRET_KEY="sua_chave_secreta"
```

5. Execute a aplicação:

```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Endpoints da API

### Autenticação

-   `POST /register`: Registra um novo usuário
-   `POST /login`: Autentica e obtém token de acesso
-   `POST /logout`: Invalida sessão (client-side)

### Gerenciamento de Dívidas

-   `GET /debts`: Lista dívidas do usuário autenticado
-   `POST /debts`: Cria uma nova dívida (somente admin)

### Score de Crédito

-   `GET /score`: Obtém score de crédito do usuário autenticado

## Testando a API

1. Acesse a documentação interativa em `http://localhost:8000/docs`
2. Registre um usuário através do endpoint `/register`
3. Faça login com as credenciais no endpoint `/login` para obter um token
4. Clique no botão "Authorize" no topo da página e insira o token no formato `Bearer seu_token_aqui`
5. Agora você pode testar os endpoints protegidos como `/debts` e `/score`

## Detalhes de Implementação

-   Usuários com endereços de email de domínio específico (configurado no sistema) recebem automaticamente privilégios de administrador
-   O score de crédito é calculado usando a fórmula: 1000 / √(x + 100), onde x é o valor médio das dívidas
-   A autenticação é realizada via tokens JWT com expiração de 30 minutos
