from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# --- USUÁRIO ---
class UsuarioBase(BaseModel):
    nome_usuario: str = Field(..., examples=["Luan Santana"])
    email: EmailStr = Field(..., examples=["luan@gmail.com"])

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., examples=["senha123"])
    role: str = Field("funcionario", examples=["admin"])

# --- PRODUTO ---
class ProdutoBase(BaseModel):
    nome: str = Field(..., examples=["Vestido Midi Floral"])
    descricao: str = Field(..., examples=["Vestido de viscose com estampa floral e fenda lateral."])
    imagem: Optional[str] = Field(None, examples=["https://link-da-imagem.com/foto.jpg"])
    categoria: str = Field(..., examples=["Vestidos"])
    estacao: str = Field(..., examples=["Primavera/Verão 2026"])
    preco_base: float = Field(..., examples=[189.90])
    tags: List[str] = Field([], examples=[["floral", "viscose", "festa"]])
    processado_ml: bool = Field(False, examples=[False])

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, examples=["Vestido Midi Floral Alterado"])
    preco_base: Optional[float] = Field(None, examples=[199.90])
    descricao: Optional[str] = Field(None, examples=["Nova descrição aqui"])
    categoria: Optional[str] = None
    estacao: Optional[str] = None
    tags: Optional[List[str]] = None
    processado_ml: Optional[bool] = None

# --- ESTOQUE ---
class EstoqueBase(BaseModel):
    tamanho: str = Field(..., examples=["M"])
    cor: str = Field(..., examples=["Azul Marinho"])
    quantidade: int = Field(..., examples=[15])
    codigo_barras: Optional[str] = Field(None, examples=["7891234567890"])

class ProdutoComEstoqueCreate(ProdutoCreate):
    estoque_inicial: List[EstoqueBase] = Field(
        ..., 
        examples=[[
            {"tamanho": "P", "cor": "Rosa", "quantidade": 5},
            {"tamanho": "M", "cor": "Rosa", "quantidade": 10}
        ]]
    )

class EstoqueCreate(EstoqueBase):
    id_produto: str = Field(..., examples=["ID_DO_PRODUTO_FIREBASE"])

# --- VENDA ---
class ItemVenda(BaseModel):
    id_item_estoque: str = Field(..., examples=["ID_DO_ITEM_NO_ESTOQUE"])
    quantidade: int = Field(..., examples=[2])
    preco_unitario_venda: float = Field(..., examples=[189.90])

class VendaCreate(BaseModel):
    id_usuario: str = Field(..., examples=["ID_VENDEDOR_LOGADO"])
    meio_venda: str = Field(..., examples=["WhatsApp"])
    status_venda: str = Field("Pendente", examples=["Finalizada"])
    nome_comprador: str = Field(..., examples=["Ana Silva"])
    telefone_comprador: str = Field(..., examples=["13999999999"])
    dados_pagamento: str = Field(..., examples=["Pix"])
    itens: List[ItemVenda]