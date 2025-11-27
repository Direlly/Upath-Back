from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.auth_schemas import UserLogin, UserCreate, PasswordResetRequest, PasswordReset
from services.auth_service import AuthService
from services.token_service import TokenService
from services.email_service import EmailService
from core.security import criar_token, get_current_user
from models.auth import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

# Rota para registrar novo usuário
@router.post("/register")
def registrar_usuario(dados: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    resultado = service.registrar_usuario(
        nome=dados.nome,
        email=dados.email,
        confirm_email=dados.email,  # Corrigido - usando o mesmo email
        senha=dados.senha,
        confirm_senha=dados.confirmar_senha  # Corrigido nome do campo
    )
    
    if not resultado["success"]:
        if "já cadastrado" in resultado["mensagem"]:
            raise HTTPException(status_code=409, detail=resultado["mensagem"])
        else:
            raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "id_usuario": resultado["id_usuario"],
            "nome": resultado["nome"],
            "email": resultado["email"],
            "mensagem": "Conta criada com sucesso."
        }
    }

@router.post("/login")
def login_usuario(dados: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    usuario = service.autenticar_usuario(dados.email, dados.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais incorretas.")
    
    # Gerar token JWT
    token = criar_token({"sub": usuario.email, "id": usuario.id_usuario})
    
    # Gerar refresh token
    token_service = TokenService(db)
    refresh_token = token_service.create_refresh_token(usuario.id_usuario)
    
    return {
        "success": True,
        "data": {
            "access_token": token,
            "refresh_token": refresh_token.token,
            "token_type": "bearer",
            "user": {
                "id_usuario": usuario.id_usuario,
                "nome": usuario.nome,
                "email": usuario.email
            }
        }
    }

@router.post("/forgot-password")
def recuperar_senha(dados: PasswordResetRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    resultado = service.enviar_email_recuperacao(dados.email)
    
    if not resultado["success"]:
        if "não encontrado" in resultado["mensagem"].lower():
            raise HTTPException(status_code=404, detail=resultado["mensagem"])
        else:
            raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True, 
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }

@router.post("/reset-password")
def redefinir_senha(dados: PasswordReset, db: Session = Depends(get_db)):
    service = AuthService(db)
    resultado = service.redefinir_senha(dados.token, dados.nova_senha)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True, 
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }