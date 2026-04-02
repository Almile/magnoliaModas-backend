from fastapi import APIRouter, HTTPException, Header, Depends
from app.core.firebase import db
from firebase_admin import auth
from app.models.schemas import ProdutoCreate, ProdutoUpdate
from typing import List

router = APIRouter()

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verificar_admin(credenciais: HTTPAuthorizationCredentials = Depends(security)):
    token = credenciais.credentials # O FastAPI já corta o "Bearer " pra você aqui!
    try:
        decoded_token = auth.verify_id_token(token)
        if decoded_token.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso restrito")
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/")
async def listar_produtos():
    try:
        produtos_ref = db.collection("produtos").stream()
        lista_produtos = []
        for doc in produtos_ref:
            item = doc.to_dict()
            item["id"] = doc.id
            lista_produtos.append(item)
        return lista_produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/adicionar-produto")
async def adicionar_produto(produto: ProdutoCreate):
    try:
        doc_ref = db.collection("produtos").document()
        dados_produto = produto.model_dump(mode="json")
        doc_ref.set(dados_produto)
        return {"id": doc_ref.id, "status": "sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{produto_id}")
async def buscar_produto(produto_id: str):
    doc = db.collection("produtos").document(produto_id).get()
    if doc.exists:
        return {**doc.to_dict(), "id": doc.id}
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@router.put("/{produto_id}")
async def atualizar_produto(produto_id: str, produto: ProdutoUpdate):
    try:
        doc_ref = db.collection("produtos").document(produto_id)
        snapshot = doc_ref.get()
        if not snapshot.exists:
            raise HTTPException(status_code=404, detail="Produto não existe")
        dados_para_atualizar = produto.model_dump(exclude_unset=True)
        if not dados_para_atualizar:
            return {"message": "Nada para atualizar"}

        doc_ref.update(dados_para_atualizar)
        return {"status": "atualizado", "id": produto_id, "campos_alterados": list(dados_para_atualizar.keys())}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{produto_id}")
async def deletar(produto_id: str, user=Depends(verificar_admin)):
    try:
        doc_ref = db.collection("produtos").document(produto_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        doc_ref.delete()
        return {"status": "removido", "id": produto_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))