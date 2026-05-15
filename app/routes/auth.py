import os
from dotenv import load_dotenv
import httpx
from fastapi import APIRouter, HTTPException
from firebase_admin import auth, firestore
from app.core.firebase import db
from app.models.schemas import UsuarioCreate

load_dotenv() 

router = APIRouter()

FIREBASE_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")

@router.post("/cadastro")
async def cadastrar_usuario(usuario: UsuarioCreate):
    try:
        user_record = auth.create_user(
            email=usuario.email,
            password=usuario.senha,
            display_name=usuario.nome_usuario
        )

        auth.set_custom_user_claims(user_record.uid, {'role': usuario.role})
        
        db.collection("usuarios").document(user_record.uid).set({
            "nome": usuario.nome_usuario,
            "email": usuario.email,
            "role": usuario.role,
            "criado_em": firestore.SERVER_TIMESTAMP
        })

        return {
            "uid": user_record.uid, 
            "role": usuario.role, 
            "status": "Usuário criado com sucesso"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login_usuario(email: str, senha: str):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": senha,
        "returnSecureToken": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        data = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

        return {
            "token": data["idToken"],
            "email": data["email"],
            "localId": data["localId"]
        }

@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    uid = user["uid"]
    auth.revoke_refresh_tokens(uid)
    return {
        "status": "sucesso",
        "message": "Sessões revogadas com sucesso."
    }