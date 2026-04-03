from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def ml():
    return {"msg": "uso de ml"}