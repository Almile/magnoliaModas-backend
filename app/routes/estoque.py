from fastapi import APIRouter, HTTPException, Body
from app.core.firebase import db
from datetime import datetime
from app.models.schemas import EstoqueBase

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

@router.post("/adicionar-variacao")
async def adicionar_variacao(payload: EstoqueBase, id_produto: str):
    try:
        produto_ref = db.collection("produtos").document(id_produto).get()
        if not produto_ref.exists:
            raise HTTPException(status_code=404, detail="Produto pai não encontrado.")

        nova_variacao_ref = db.collection("estoques").document()
        id_gerado = nova_variacao_ref.id
        
        dados_variacao = {
            "id_produto": id_produto,
            "tamanho": payload.tamanho,
            "cor": payload.cor,
            "quantidade": payload.quantidade,
            "codigo_barras": payload.codigo_barras or f"TEMP-{id_produto}-{payload.tamanho}-{payload.cor}",
        }
        
        nova_variacao_ref.set(dados_variacao)

        db.collection("historico_estoque").add({
            "id_produto_estoque": id_gerado,
            "tipo": "Entrada",
            "quantidade": payload.quantidade,
            "motivo": "Criação de nova variação/grade",
            "data": datetime.now()
        })

        return {
            "status": "sucesso", 
            "id_variacao": id_gerado, 
            "msg": f"Variação {payload.tamanho} - {payload.cor} adicionada ao produto."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))