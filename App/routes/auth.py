from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    
    # Verificar se email já existe
    if auth_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado"
        )
    
    # Criar usuário
    user = auth_service.create_user(user_data)
    
    return {
        "success": True,
        "data": {
            "id_usuario": user.id,
            "nome": user.nome,
            "email": user.email
        }
    }

@router.post("/login", response_model=dict)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    
    user = auth_service.authenticate_user(login_data.email, login_data.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas"
        )
    
    # Atualizar último login
    auth_service.update_last_login(user.id)
    
    # Gerar token
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id, "role": user.role})
    
    return {
        "success": True,
        "data": {
            "token": access_token,
            "user": {
                "id": user.id,
                "nome": user.nome,
                "role": user.role
            }
        }
    }

@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    # Implementar lógica de recuperação de senha
    return {"success": True, "message": "Email de recuperação enviado"}

@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    # Implementar lógica de redefinição de senha
    return {"success": True, "message": "Senha redefinida com sucesso"}