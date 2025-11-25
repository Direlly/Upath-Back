from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.auth_schemas import PasswordUpdate
from services.auth_service import AuthService

router = APIRouter(prefix="/api/perfil", tags=["Perfil"])

@router.post("/change-password")
def alterar_senha(dados: PasswordUpdate, db: Session = Depends(get_db), usuario_atual: dict = Depends(get_current_user)):
    service = AuthService(db)
    resultado = service.alterar_senha(
        id_usuario=usuario_atual["user_id"],
        senha_atual=dados.senha_atual,
        nova_senha=dados.nova_senha
    )
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }