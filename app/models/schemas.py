from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# --- USUÁRIO ---
class UsuarioBase(BaseModel):
    nome_usuario: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str  #fazer o hash

# --- PRODUTO ---
class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    imagem: Optional[str] = None
    categoria: str
    estacao: str
    preco_base: float
    tags: List[str] = []
    processado_ml: bool = False

class ProdutoCreate(ProdutoBase):
    pass

# --- ESTOQUE ---
class EstoqueBase(BaseModel):
    id_produto: str  # FK para o Produto
    codigo_barras: str
    tamanho: str
    cor: str
    quantidade: int

class EstoqueCreate(EstoqueBase):
    pass

# --- VENDA ---
class ItemVenda(BaseModel):
    id_item_estoque: str
    quantidade: int
    preco_unitario_venda: float

class VendaCreate(BaseModel):
    id_usuario: str
    meio_venda: str # WhatsApp, Feira, etc
    status_venda: str = "Pendente"
    nome_comprador: str
    telefone_comprador: str
    dados_pagamento: str
    itens: List[ItemVenda] # Lista de itens que compõem a venda