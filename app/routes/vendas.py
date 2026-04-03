from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def listar_vendas():
    return {"msg": "vendas"}