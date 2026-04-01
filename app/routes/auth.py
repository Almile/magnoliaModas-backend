from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
async def autenticacao():
    return {"msg": "autenticação"}