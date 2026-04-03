from fastapi import APIRouter, HTTPException
from app.core.firebase import db

router = APIRouter()

@router.get("/")
async def listar_todo_estoque():
    try:
        estoque_ref = db.collection("estoques").stream()
        return [doc.to_dict() for doc in estoque_ref]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/produto/{produto_id}")
async def buscar_estoque_por_produto(produto_id: str):
    try:
        query = db.collection("estoques").where("id_produto", "==", produto_id).stream()
        lista_estoque = []
        
        for doc in query:
            item = doc.to_dict()
            item["id_variacao"] = doc.id
            lista_estoque.append(item)
            
        if not lista_estoque:
            return {"msg": "Nenhum estoque encontrado para este produto", "estoque": []}
            
        return lista_estoque
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))