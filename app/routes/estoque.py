from fastapi import APIRouter, HTTPException, Body
from app.core.firebase import db
from datetime import datetime

router = APIRouter()

@router.get("/")
async def listar_todo_estoque():
    try:
        estoque_ref = db.collection("estoques").stream()
        lista_estoque = []
        for doc in estoque_ref:
            item = doc.to_dict()
            item["id_variacao"] = doc.id
            lista_estoque.append(item)
        return lista_estoque
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

@router.patch("/baixar/{variacao_id}")
async def baixar_estoque(variacao_id: str, quantidade_vendida: int = Body(..., embed=True)):
    try:
        doc_ref = db.collection("estoques").document(variacao_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="ID de variação não encontrado no banco.")
        dados_atuais = doc.to_dict()
        estoque_atual = dados_atuais.get("quantidade", 0)

        if estoque_atual < quantidade_vendida:
            raise HTTPException(
                status_code=400, 
                detail=f"Estoque insuficiente. Disponível: {estoque_atual}"
            )
        novo_estoque = estoque_atual - quantidade_vendida
        doc_ref.update({"quantidade": novo_estoque})

        historico_ref = db.collection("historico_estoque").document()
        historico_ref.set({
            "id_produto_estoque": variacao_id,
            "tipo": "Saída",
            "quantidade": quantidade_vendida,
            "motivo": "Venda",
            "data": datetime.now()
        })
        return {
            "status": "sucesso", 
            "novo_estoque": novo_estoque,
            "msg": f"Baixa de {quantidade_vendida} unidades realizada."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/repor/{variacao_id}")
async def repor_estoque(variacao_id: str, quantidade_adicionada: int = Body(..., embed=True)):
    try:
        doc_ref = db.collection("estoques").document(variacao_id)
        doc = doc_ref.get()

        nova_qtd = doc.to_dict().get("quantidade", 0) + quantidade_adicionada
        doc_ref.update({"quantidade": nova_qtd})

        db.collection("historico_estoque").add({
            "id_produto_estoque": variacao_id,
            "tipo": "Entrada",
            "quantidade": quantidade_adicionada,
            "motivo": "Reposição de Estoque",
            "data": datetime.now()
        })
        return {"status": "sucesso", "novo_estoque": nova_qtd}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))