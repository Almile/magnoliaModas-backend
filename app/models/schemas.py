from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from typing import Optional
# --- USUÁRIO ---from pydantic import BaseModel, EmailStr, Field


# --- USUÁRIO ---
class UsuarioBase(BaseModel):
    nome_usuario: str
    email: EmailStr

class UsuarioCreate(BaseModel):
    nome_usuario: str
    email: EmailStr
    senha: str
    role: str = "funcionario"

# --- PRODUTO ---

# Dica: Defina o Base antes para que o Create e o Update herdem dele
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

# O Update agora herda do Base, mas torna tudo Opcional
class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco_base: Optional[float] = None # Ajustado para bater com o nome do campo no Base
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    estacao: Optional[str] = None
    tags: Optional[List[str]] = None
    processado_ml: Optional[bool] = None

# --- ESTOQUE ---
class EstoqueBase(BaseModel):
    id_produto: str
    codigo_barras: str
    tamanhos: List[str] = [] # Ex: ["P", "M", "G"]
    cores: List[str] = []
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
    itens: List[ItemVenda]