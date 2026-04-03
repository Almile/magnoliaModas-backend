from fastapi import APIRouter, HTTPException, Header, Depends
from app.core.firebase import db
from firebase_admin import auth
from app.models.schemas import ProdutoCreate, ProdutoUpdate, ProdutoComEstoqueCreate
from typing import List

router = APIRouter()

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verificar_admin(credenciais: HTTPAuthorizationCredentials = Depends(security)):
    token = credenciais.credentials 
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
            
            estoque_ref = db.collection("estoques").where("id_produto", "==", doc.id).stream()
            item["estoque"] = [variacao.to_dict() for variacao in estoque_ref]
            lista_produtos.append(item)
        return lista_produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{produto_id}")
async def buscar_produto(produto_id: str):
    doc = db.collection("produtos").document(produto_id).get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    produto_data = doc.to_dict()
    produto_data["id"] = doc.id
    
    estoque_ref = db.collection("estoques").where("id_produto", "==", produto_id).stream()
    produto_data["estoque"] = [variacao.to_dict() for variacao in estoque_ref]
    
    return produto_data

@router.post("/adicionar-produto")
async def adicionar_produto(payload: ProdutoComEstoqueCreate):
    try:
        dados_produto = payload.model_dump(exclude={'estoque_inicial'}, mode="json")
        
        doc_ref_produto = db.collection("produtos").document()
        id_produto_gerado = doc_ref_produto.id
        doc_ref_produto.set(dados_produto)

        for item in payload.estoque_inicial:
            estoque_ref = db.collection("estoques").document()
            dados_estoque = {
                "id_produto": id_produto_gerado,
                "tamanho": item.tamanho,
                "cor": item.cor,
                "quantidade": item.quantidade,
                "codigo_barras": item.codigo_barras or f"TEMP-{id_produto_gerado}-{item.tamanho}",
            }
            estoque_ref.set(dados_estoque)
        return {
            "id": id_produto_gerado, 
            "status": "sucesso", 
            "msg": f"Produto e {len(payload.estoque_inicial)} variações criadas."
        }
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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