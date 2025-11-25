from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_admin
from schemas.cursos_schemas import  CourseCreate
from services.cursos_service import CourseService
from services.email_service import EmailService
import secrets
from datetime import datetime, timedelta

router = APIRouter()

# Simulação de sessões admin temporárias para 2FA
admin_sessions = {}

# Rota para login admin e envio do PIN 2FA
@router.post("/login", response_model=LoginResponse)
async def admin_login(credentials: LoginRequest, db: Session = Depends(get_db)):

    # Buscar admin no banco
    admin = db.query(Admin).filter(Admin.username == credentials.username).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    # Verificar senha com passlib
    if not pwd_context.verify(credentials.password, admin.password):
        raise HTTPException(status_code=401, detail="Senha inválida")

    # Gerar sessão e PIN (para 2FA opcional)
    session_id = secrets.token_hex(16)
    pin_code = str(secrets.randbelow(10000)).zfill(4)

    admin_sessions[session_id] = {
        "username": admin.username,
        "pin_code": pin_code,
        "created_at": datetime.utcnow()
    }

    # Aqui você pode enviar o PIN por email ou SMS (opcional)
    # Ex.: email_service.send_admin_2fa_email(admin.email, pin_code)

    return {
        "success": True,
        "token": session_id,  # ou JWT se preferir
        "message": "Login realizado com sucesso"
    }


# Rota para verificar o PIN 2FA e obter token JWT
@router.post("/auth")
async def admin_verify_2fa(verification_data: dict):
    session_id = verification_data.get("session_id")
    token_4d = verification_data.get("token_4d")
    
    session = admin_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    # Verificar expiração (10 minutos)
    if datetime.utcnow() - session["created_at"] > timedelta(minutes=10):
        del admin_sessions[session_id]
        raise HTTPException(status_code=401, detail="PIN expirado")
    
    if session["pin_code"] != token_4d:
        raise HTTPException(status_code=401, detail="PIN incorreto")
    
    # Gerar JWT admin
    from core.security import create_access_token
    access_token = create_access_token(
        data={
            "sub": session["email"],
            "user_id": 0,  # ID especial para admin
            "role": "admin"
        },
        expires_delta=timedelta(hours=8)
    )
    
    # Limpar sessão temporária
    del admin_sessions[session_id]
    
    return {
        "success": True,
        "data": {
            "token": access_token,
            "user": {
                "email": session["email"],
                "role": "admin"
            }
        }
    }


@router.get("/homeAdmin")
async def admin_home(current_admin: dict = Depends(get_current_admin)):
    return {
        "success": True,
        "data": {
            "message": f"Bem-vindo, {current_admin['email']}! Esta é a área administrativa."
        }
    }

