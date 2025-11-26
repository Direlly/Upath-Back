from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.auth_schemas import UserLogin, UserCreate, PasswordUpdate, PasswordResetRequest, PasswordReset
from services.auth_service import AuthService
from core.security import criar_token, get_current_user, get_password_hash
from models.auth import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

# Rota para registrar novo usuário
@router.post("/register")
def registrar_usuario(dados: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    resultado = service.registrar_usuario(
        nome=dados.nome,
        email=dados.email,
        senha=dados.senha,
        confirmar_senha=dados.confirmar_senha
    )
    
    if not resultado["success"]:
        if "já cadastrado" in resultado["mensagem"]:
            raise HTTPException(status_code=409, detail=resultado["mensagem"])
        else:
            raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    # Criar token JWT após registro bem-sucedido
    token = criar_token({"sub": dados.email, "id": resultado["id_usuario"], "role": "student"})
    
    return {
        "success": True,
        "data": {
            "id_usuario": resultado["id_usuario"],
            "nome": resultado["nome"],
            "email": resultado["email"],
            "token": token,
            "mensagem": "Conta criada com sucesso."
        }
    }

@router.post("/login")
def login_usuario(dados: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    usuario = service.autenticar_usuario(dados.email, dados.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais incorretas.")
    
    # CRIAR TOKEN JWT
    token_data = {
        "sub": usuario.email,
        "id": usuario.id_usuario,
        "role": "student"
    }
    token = criar_token(token_data)
    
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email
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
    resultado = service.redefinir_senha(dados.token, dados.nova_senha, dados.confirmar_senha)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True, 
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }

@router.get("/me")
def obter_usuario_atual(usuario_atual: dict = Depends(get_current_user), db: Session = Depends(get_db)):
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
            "role": usuario.role
        }
    }

@router.post("/logout")
def logout_usuario():
    # Em JWT, o logout é feito no front-end removendo o token
    return {
        "success": True,
        "data": {
            "mensagem": "Logout realizado com sucesso."
        }
    }