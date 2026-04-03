from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import produtos, auth, estoque, ml, vendas ,usuarios
from fastapi.security import HTTPBearer

security = HTTPBearer()

app = FastAPI(title="API - Magnólia Modas", swagger_ui_parameters={"persistAuthorization": True})

# Configura o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"],dependencies=[Depends(security)])
app.include_router(estoque.router, prefix="/estoque", tags=["Estoque"])
app.include_router(vendas.router, prefix="/vendas", tags=["Vendas"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(ml.router, prefix="/ml", tags=["Machine Learning"])

@app.get("/")
def home():
    return {"message": "API - Magnólia Modas - acesse /docs para ver e testar os endpoints."}