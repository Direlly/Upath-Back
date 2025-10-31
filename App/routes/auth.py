from fastapi import APIRouter, Depends, HTTPException ,Form, status 
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import create_access_token, verify_password, get_password_hash
from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth_service import AuthService

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


@router.post("/google-login", response_model=dict)
async def google_login(token: str = Form(...), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    
    try:
        # Verificar o token do Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), audience="1096686352229-odd85chvi5i3o9hdae3ujg9vkcfg0l4d.apps.googleusercontent.com")
        
        email = idinfo['email']
        nome = idinfo.get('name', 'Usuário Google')
        
        # Atualizar último login
        auth_service.update_last_login(user.id)
        
        # Gerar token de acesso
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
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token do Google inválido"
        )
