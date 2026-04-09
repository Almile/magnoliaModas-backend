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
from app.services.ml_service import analisar_roupa_com_ia
from .produtos import salvar_estoque_inicial
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class SalesPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

@router.post("/sugerir-dados-produto")
async def sugerir_produto_ml(imagem: UploadFile = File(...)):
    try:
        conteudo_imagem = await imagem.read()
        
        sugestao_ia = await analisar_roupa_com_ia(conteudo_imagem)
        
        imagem.file.seek(0)
        url_foto = await upload_imagem_cloudinary(imagem)

        return {
            "status": "sucesso",
            "sugestao": {
                "nome": sugestao_ia.get("nome"),
                "preco_base": sugestao_ia.get("preco_sugerido"),
                "descricao": sugestao_ia.get("descricao"),
                "categoria": sugestao_ia.get("categoria"),
                "estacao": sugestao_ia.get("estacao"),
                "imagem": url_foto,
                "processado_ml": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na sugestão: {str(e)}")

def preparar_dados(self, dados_vendas):
    df = pd.DataFrame(dados_vendas)
    df['data'] = pd.to_datetime(df['data'])
    df['mes'] = df['data'].dt.month
    df['dia_semana'] = df['data'].dt.dayofweek
    return df

def treinar(self, dados_vendas):
    df = self.preparar_dados(dados_vendas)
    X = df[['produto_id', 'mes', 'dia_semana']]
    y = df['quantidade']
    self.model.fit(X, y)

def prever_proximo_periodo(self, produto_id):
    hoje = datetime.datetime.now()
    X_novo = pd.DataFrame([[produto_id, hoje.month, hoje.weekday()]], 
                            columns=['produto_id', 'mes', 'dia_semana'])
    previsao = self.model.predict(X_novo)
    return round(previsao[0])
