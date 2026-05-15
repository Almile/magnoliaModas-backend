from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from app.core.firebase import db
from firebase_admin import auth
from app.models.schemas import ProdutoCreate, ProdutoUpdate, ProdutoComEstoqueCreate
from app.services.cloudinary_service import upload_imagem_cloudinary
from typing import List
import json
from datetime import datetime
from fastapi import Query
from typing import Optional

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

@router.get("/filtrar")
async def filtrar_produtos(
    categoria: Optional[str] = Query(None),
    estacao: Optional[str] = Query(None),
    processado_ml: Optional[bool] = Query(None),
    preco_min: Optional[float] = Query(None),
    preco_max: Optional[float] = Query(None),
    nome: Optional[str] = Query(None)
):
    try:
        query = db.collection("produtos")
        filtros_exatos = {
            "categoria": categoria,
            "processado_ml": processado_ml
        }
        for campo, valor in filtros_exatos.items():
            if valor is not None:
                query = query.where(campo, "==", valor)

        if preco_min is not None:
            query = query.where("preco_base", ">=", preco_min)
        if preco_max is not None:
            query = query.where("preco_base", "<=", preco_max)

        docs = query.stream()
        lista_produtos = []

        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            match_estacao = not estacao or estacao.lower() in item.get("estacao", "").lower()
            match_nome = not nome or nome.lower() in item.get("nome", "").lower()
            if not (match_estacao and match_nome):
                continue

            estoque_ref = db.collection("estoques").where("id_produto", "==", doc.id).stream()
            item["estoque"] = [v.to_dict() for v in estoque_ref]
            lista_produtos.append(item)
        return lista_produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro dinâmico: {str(e)}")

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

def salvar_estoque_inicial(id_produto: str, lista_estoque: list):
    for item in lista_estoque:
        estoque_ref = db.collection("estoques").document()
        
        codigo = item.get("codigo_barras") 
        
        dados_estoque = {
            "id_produto": id_produto,
            "tamanho": item.get("tamanho", "U"),
            "cor": item.get("cor", "N/A"),
            "quantidade": item.get("quantidade", 0),
            "codigo_barras": codigo if codigo else None, 
        }
        estoque_ref.set(dados_estoque)

@router.post("/adicionar-produto")
async def adicionar_produto(
    nome: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    estacao: str = Form(...),
    preco_base: float = Form(...),
    tags: str = Form('[]'),
    estoque_inicial: str = Form('[]'),
    imagem: UploadFile = File(None),
    imagem_url: Optional[str] = Form(None)
):
    try:
        try:
            lista_tags = json.loads(tags.replace("'", '"')) 
        except:
            lista_tags = []
        
        try:
            lista_estoque = json.loads(estoque_inicial)
        except:
            lista_estoque = []
        url_final = None

        if imagem:
            url_final = await upload_imagem_cloudinary(imagem)
        elif imagem_url:
            url_final = imagem_url
        
        novo_produto = {
            "nome": nome,
            "descricao": descricao,
            "categoria": categoria,
            "estacao": estacao,
            "preco_base": preco_base,
            "imagem": url_final,
            "tags": lista_tags,
            "data_cadastro": datetime.now(),
            "processado_ml": True if imagem_url else False
        }

        doc_ref_produto = db.collection("produtos").document()
        id_produto_gerado = doc_ref_produto.id
        doc_ref_produto.set(novo_produto)

        salvar_estoque_inicial(id_produto_gerado, lista_estoque)

        return {"id": id_produto_gerado, "status": "sucesso", "url_imagem": url_final}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

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
