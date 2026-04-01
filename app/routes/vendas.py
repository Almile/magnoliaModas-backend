from fastapi import APIRouter

router = APIRouter()

@router.get("/vendas")
async def listar_vendas():
    return {"msg": "vendas"}