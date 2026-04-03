from fastapi import APIRouter, HTTPException, Depends
from app.core.firebase import db
from firebase_admin import auth
from .produtos import verificar_admin
from app.models.schemas import UsuarioBase, UsuarioCreate
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
        
@router.get("/")
async def listar_funcionarios(user=Depends(verificar_admin)):
    try:
        usuarios_ref = db.collection("usuarios").stream()
        lista = []
        for doc in usuarios_ref:
            u = doc.to_dict()
            u["id"] = doc.id
            u.pop("senha", None)
            lista.append(u)
        return lista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{usuario_id}")
async def editar_funcionario(usuario_id: str, dados: UsuarioBase, user=Depends(verificar_admin)):
    try:
        doc_ref = db.collection("usuarios").document(usuario_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        doc_ref.update(dados.model_dump(exclude_unset=True))
        return {"status": "atualizado", "id": usuario_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{usuario_id}")
async def excluir_funcionario(usuario_id: str, user=Depends(verificar_admin)):
    try:
        db.collection("usuarios").document(usuario_id).delete()
        return {"status": "removido", "id": usuario_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))