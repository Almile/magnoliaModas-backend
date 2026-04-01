# 🚀 Backend - Magnolia Modas (FastAPI + Firebase)

Este é o servidor do nosso projeto. Ele gerencia o banco de dados, autenticação e no futuro terá a lógica de Machine Learning.

## 🛠️ Pré-requisitos
1. Ter o **Python 3.10+** instalado.
2. Ter o **VS Code** instalado.

## 🏃 Como rodar o projeto

Abra o terminal na pasta do projeto e siga estes passos:

### 1. Criar o ambiente virtual
```bash
python -m venv venv
```

### 2. Ativar o ambiente
```bash
# Windows: 
venv\Scripts\activate
# Linux/Mac: 
source venv/bin/activate
```

### 3. Instalar as bibliotecas
```bash
pip install -r requirements.txt
```
### 4. Configurar as Chaves do firebase

- Você precisa do arquivo serviceAccountKey.json dentro da pasta app/core/ para o banco de dados funcionar.

### 5. Rodar o Servidor
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

O servidor estará rodando em: http://localhost:8000

### 📂 Estrutura de Pastas
app/main.py: Onde o servidor "nasce" e as rotas são registradas.

app/routes/: Onde criamos os caminhos da API (ex: /produtos).

app/models/: Onde definimos quais campos cada dado deve ter (Schemas).

app/core/: Configurações de conexão (Firebase).

📖 Documentação Automática
Com o servidor rodando, acesse: http://localhost:8000/docs para ver e testar todas as rotas criadas.