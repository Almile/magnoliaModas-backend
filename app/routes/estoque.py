from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def listar_estoque():
    return {"msg": "Lista de produtos no estoque"}
