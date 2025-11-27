from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from schemas.perfil_schemas import PasswordUpdate, UserProfileUpdate
from services.perfil_service import UserService
from services.auth_service import AuthService

router = APIRouter(prefix="/api/perfil", tags=["Perfil"])

@router.post("/change-password")
def alterar_senha(
    dados: PasswordUpdate, 
    db: Session = Depends(get_db), 
    usuario_atual: dict = Depends(get_current_user)
):
    service = AuthService(db)
    resultado = service.alterar_senha(
        id_usuario=usuario_atual["user_id"],
        senha_atual=dados.current_password,
        nova_senha=dados.new_password
    )
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }

@router.get("/me")
def obter_perfil(
    db: Session = Depends(get_db),
    usuario_atual: dict = Depends(get_current_user)
):
    service = UserService(db)
    perfil = service.get_user_profile(usuario_atual["user_id"])
    
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    
    return {
        "success": True,
        "data": {
            "id": perfil.id,
            "nome": perfil.nome,
            "email": perfil.email,
            "foto_url": perfil.foto_url,
            "role": getattr(perfil, 'role', 'student')
        }
    }

@router.put("/update")
def atualizar_perfil(
    dados: UserProfileUpdate,
    db: Session = Depends(get_db),
    usuario_atual: dict = Depends(get_current_user)
):
    service = UserService(db)
    perfil_atualizado = service.update_user_profile(usuario_atual["user_id"], dados)
    
    if not perfil_atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "success": True,
        "data": {
            "id": perfil_atualizado.id,
            "nome": perfil_atualizado.nome,
            "foto_url": perfil_atualizado.foto_url,
            "mensagem": "Perfil atualizado com sucesso"
        }
    }

@router.get("/home")
def home_usuario(
    db: Session = Depends(get_db),
    usuario_atual: dict = Depends(get_current_user)
):
    service = UserService(db)
    dados_home = service.get_user_home_data(usuario_atual["user_id"])
    
    return {
        "success": True,
        "data": dados_home
    }