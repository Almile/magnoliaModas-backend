from fastapi import APIRouter, HTTPException
from app.core.firebase import db
from datetime import datetime
from app.models.schemas import VendaCreate
router = APIRouter()

@router.post("/")
async def processar_venda(venda: VendaCreate):
    try:
        batch = db.batch()
        venda_ref = db.collection("venda").document()
        total_geral_venda = 0.0
        itens_para_registro = []

        for item in venda.itens:
            estoque_ref = db.collection("estoques").document(item.id_item_estoque)
            estoque_doc = estoque_ref.get()

            if not estoque_doc.exists:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Item de estoque {item.id_item_estoque} não encontrado."
                )

            dados_estoque = estoque_doc.to_dict()
            estoque_atual = dados_estoque.get("quantidade", 0)

            if estoque_atual < item.quantidade:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Estoque insuficiente para o item {item.id_item_estoque}. Disponível: {estoque_atual}"
                )

            subtotal_item = item.preco_unitario_venda * item.quantidade
            total_geral_venda += subtotal_item

            nova_quantidade = estoque_atual - item.quantidade
            batch.update(estoque_ref, {"quantidade": nova_quantidade})

            itens_para_registro.append({
                "id_item_estoque": item.id_item_estoque,
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario_venda,
                "subtotal": subtotal_item
            })

        dados_finais_venda = {
            "id_vendedor": venda.id_usuario,
            "meio_venda": venda.meio_venda,
            "status_venda": venda.status_venda,
            "nome_comprador": venda.nome_comprador,
            "telefone_comprador": venda.telefone_comprador,
            "dados_pagamento": venda.dados_pagamento,
            "itens": itens_para_registro,
            "total_venda": total_geral_venda,
            "data_criacao": datetime.now()
        }

        batch.set(venda_ref, dados_finais_venda)
        batch.commit()

        return {
            "status": "sucesso",
            "venda_id": venda_ref.id,
            "total": total_geral_venda
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")