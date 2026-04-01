from fastapi import APIRouter, HTTPException
from app.core.firebase import db
from app.models.schemas import ProdutoCreate
from typing import List

router = APIRouter()

@router.post("/adicionar-produto")
async def adicionar_produto(produto: ProdutoCreate):
    try:
        doc_ref = db.collection("produtos").document()
        dados_produto = produto.model_dump(mode="json")
        doc_ref.set(dados_produto)
        return {"id": doc_ref.id, "status": "sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@router.get("/{produto_id}")
async def buscar_produto(produto_id: str):
    doc = db.collection("produtos").document(produto_id).get()
    if doc.exists:
        return {**doc.to_dict(), "id": doc.id}
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@router.put("/{produto_id}")
async def atualizar_produto(produto_id: str, produto: ProdutoCreate):
    try:
        doc_ref = db.collection("produtos").document(produto_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Produto não existe")
        
        doc_ref.update(produto.model_dump(mode="json", exclude_unset=True))
        return {"status": "atualizado", "id": produto_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{produto_id}")
async def deletar_produto(produto_id: str):
    try:
        doc_ref = db.collection("produtos").document(produto_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        doc_ref.delete()
        return {"status": "removido", "id": produto_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))