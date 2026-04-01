from fastapi import APIRouter

router = APIRouter()

@router.get("/ml")
async def ml():
    return {"msg": "uso de ml"}