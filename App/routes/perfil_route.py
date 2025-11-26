from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from schemas.auth_schemas import ProfileUpdate, PasswordUpdate
from services.auth_service import AuthService

router = APIRouter(prefix="/api/perfil", tags=["Perfil"])

@router.get("/")
def obter_perfil(
    db: Session = Depends(get_db), 
    usuario_atual: dict = Depends(get_current_user)
):
    service = AuthService(db)
    usuario = service.obter_usuario_por_id(usuario_atual["user_id"])
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "success": True,
        "data": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role,
            "ultimo_login": usuario.ultimo_login
        }
    }

@router.put("/")
def atualizar_perfil(
    dados: ProfileUpdate,
    db: Session = Depends(get_db), 
    usuario_atual: dict = Depends(get_current_user)
):
    service = AuthService(db)
    resultado = service.atualizar_perfil(
        id_usuario=usuario_atual["user_id"],
        novo_nome=dados.novo_nome
    )
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"],
            "nome_atualizado": dados.novo_nome
        }
    }

@router.post("/change-password")
def alterar_senha(
    dados: PasswordUpdate, 
    db: Session = Depends(get_db), 
    usuario_atual: dict = Depends(get_current_user)
):
    service = AuthService(db)
    resultado = service.alterar_senha(
        id_usuario=usuario_atual["user_id"],
        senha_atual=dados.senha_atual,
        nova_senha=dados.nova_senha,
        confirmar_senha=dados.confirmar_senha
    )
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }