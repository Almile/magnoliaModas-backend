from fastapi import APIRouter

router = APIRouter()

@router.get("/estoque")
async def listar_estoque():
    return {"msg": "Lista de produtos no estoque"}