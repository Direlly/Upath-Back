from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_admin, validate_admin_pin, get_admin_pin_hash, criar_token
from schemas.auth_schemas import AdminLogin, AdminAuth
from services.auth_service import AuthService
from services.admin_service import AdminService
from services.email_service import EmailService
import secrets
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/admin", tags=["Administração"])

# Simulação de sessões admin temporárias para 2FA
admin_sessions = {}

# Rota para login admin - primeira etapa (credenciais)
@router.post("/login")
async def admin_login(credentials: AdminLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    
    # Autenticar admin
    resultado = service.autenticar_admin(credentials.email, credentials.senha)
    
    if not resultado["success"]:
        raise HTTPException(status_code=401, detail=resultado["mensagem"])
    
    # Gerar sessão temporária e PIN
    session_id = secrets.token_hex(16)
    pin_code = str(secrets.randbelow(10000)).zfill(4)
    
    admin_sessions[session_id] = {
        "admin_id": resultado["admin_id"],
        "email": credentials.email,
        "pin_code": pin_code,
        "created_at": datetime.utcnow()
    }
    
    # Aqui você pode enviar o PIN por email
    # email_service.send_admin_pin_email(credentials.email, pin_code)
    
    return {
        "success": True,
        "data": {
            "session_id": session_id,
            "message": "PIN enviado para autenticação"
        }
    }

# Rota para verificar o PIN e obter token JWT de admin
@router.post("/auth")
async def admin_verify_pin(auth_data: AdminAuth, db: Session = Depends(get_db)):
    session_id = auth_data.session_id
    pin = auth_data.pin
    
    session = admin_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")
    
    # Verificar expiração (10 minutos)
    if datetime.utcnow() - session["created_at"] > timedelta(minutes=10):
        del admin_sessions[session_id]
        raise HTTPException(status_code=401, detail="PIN expirado")
    
    # Validar PIN
    if session["pin_code"] != pin:
        raise HTTPException(status_code=401, detail="PIN incorreto")
    
    # Gerar JWT admin definitivo
    access_token = criar_token(
        {
            "sub": session["email"],
            "id": session["admin_id"],
            "role": "admin"
        },
        timedelta(hours=8)
    )
    
    # Limpar sessão temporária
    del admin_sessions[session_id]
    
    return {
        "success": True,
        "data": {
            "token": access_token,
            "user": {
                "id": session["admin_id"],
                "email": session["email"],
                "role": "admin"
            }
        }
    }

@router.get("/home")
async def admin_home(current_admin: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    admin_service = AdminService(db)
    
    # Obter estatísticas básicas
    stats = admin_service.obter_estatisticas()
    
    return {
        "success": True,
        "data": {
            "admin": {
                "email": current_admin["email"],
                "id": current_admin["user_id"]
            },
            "estatisticas": stats,
            "message": f"Bem-vindo, {current_admin['email']}! Esta é a área administrativa."
        }
    }

@router.get("/users")
async def pesquisar_usuarios(
    user_id: str = Query(None, description="ID do usuário para pesquisa"),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    
    if user_id:
        # Pesquisar usuário específico por ID
        usuario = admin_service.pesquisar_usuario_por_id(user_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return {
            "success": True,
            "data": {
                "usuario": usuario
            }
        }
    else:
        # Listar todos os usuários (com paginação em produção)
        usuarios = admin_service.listar_usuarios()
        return {
            "success": True,
            "data": {
                "usuarios": usuarios,
                "total": len(usuarios)
            }
        }

@router.post("/users/{user_id}/block")
async def bloquear_usuario(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    resultado = admin_service.bloquear_usuario(user_id)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }

@router.post("/users/{user_id}/unblock")
async def desbloquear_usuario(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    resultado = admin_service.desbloquear_usuario(user_id)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }

@router.delete("/users/{user_id}")
async def excluir_usuario(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    resultado = admin_service.excluir_usuario(user_id)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }

@router.post("/users/{user_id}/reset-password")
async def resetar_senha_usuario(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    resultado = admin_service.resetar_senha_usuario(user_id)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    return {
        "success": True,
        "data": {
            "mensagem": resultado["mensagem"]
        }
    }

@router.get("/metrics")
async def obter_metricas(
    periodo: str = Query("diario", description="Período: diario, semanal, mensal"),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    metricas = admin_service.obter_metricas_usuarios(periodo)
    
    return {
        "success": True,
        "data": {
            "periodo": periodo,
            "metricas": metricas
        }
    }