from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import produtos

# 1. Instancia o app apenas UMA vez
app = FastAPI(title="Gestão de Loja API")

# 2. Configura o CORS nesta instância
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inclui as rotas nesta mesma instância
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(produtos.router, prefix="/auth", tags=["auth"])
app.include_router(produtos.router, prefix="/estoque", tags=["Estoque"])
app.include_router(produtos.router, prefix="/ml", tags=["Machine learning"])
app.include_router(produtos.router, prefix="/vendas", tags=["Vendas"])


# 4. Define a rota home
@app.get("/")
def home():
    return {"message": "API de Gestão de Loja Online"}