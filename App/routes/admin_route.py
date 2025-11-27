from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, criar_token, get_current_admin
from schemas.admin_schemas import LoginRequest, LoginResponse, PinValidationRequest, PinValidationResponse
from services.admin_service import AdminService
from services.token_service import AdminAuthService
from services.email_service import EmailService
from datetime import timedelta

router = APIRouter(prefix="/api/admin", tags=["Administração"])

# Rota para login admin e envio do PIN 2FA
@router.post("/login", response_model=LoginResponse)
async def admin_login(credentials: LoginRequest, db: Session = Depends(get_db)):
    admin_service = AdminService(db)
    email_service = EmailService()
    admin_auth_service = AdminAuthService(db)

    # Buscar admin no banco
    admin = admin_service.obter_admin_por_username(credentials.username)
    if not admin:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    # Verificar senha
    if not admin_service.validar_login(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Senha inválida")

    # Criar sessão 2FA
    session = admin_auth_service.create_admin_session(admin.email) # type: ignore
    
    # Enviar PIN por email
    email_enviado = email_service.send_admin_pin_email(admin.email, session.pin_code) # type: ignore
    
    if not email_enviado:
        # Não falhar se o email não for enviado, apenas logar
        print(f"⚠️ Email não enviado, mas PIN gerado: {session.pin_code}")

    return {
        "success": True,
        "token": session.session_id,
        "message": "Código de verificação enviado para seu email"
    }

# Rota para verificar o PIN 2FA e obter token JWT
@router.post("/verify-2fa", response_model=PinValidationResponse)
async def admin_verify_2fa(verification_data: PinValidationRequest, db: Session = Depends(get_db)):
    admin_auth_service = AdminAuthService(db)
    admin_service = AdminService(db)
    
    # Verificar sessão e PIN
    session = admin_auth_service.verify_admin_session(
        verification_data.session_id, 
        verification_data.pin
    )
    
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou PIN incorreto")
    
    # Buscar admin pelo email da sessão
    admin = admin_service.obter_admin_por_email(session.admin_email) # type: ignore
    if not admin:
        raise HTTPException(status_code=401, detail="Administrador não encontrado")
    
    # Marcar sessão como usada
    admin_auth_service.mark_admin_session_used(session.session_id) # type: ignore
    
    # Gerar JWT admin
    access_token = criar_token(
        data={
            "sub": admin.email,
            "user_id": admin.id,
            "role": "admin",
            "username": admin.username,
            "name": admin.name
        },
        expires_delta=timedelta(hours=8)
    )
    
    return {
        "success": True,
        "message": "Autenticação realizada com sucesso",
        "token": access_token
    }

@router.get("/home")
async def admin_home(current_admin: dict = Depends(get_current_admin)):
    return {
        "success": True,
        "data": {
            "message": f"Bem-vindo, {current_admin.get('name', 'Administrador')}!",
            "user": {
                "email": current_admin.get('email'),
                "username": current_admin.get('username'),
                "name": current_admin.get('name'),
                "role": current_admin.get('role')
            }
        }
    }

# Rota para obter estatísticas do sistema
@router.get("/stats")
async def admin_stats(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    
    estatisticas = admin_service.obter_estatisticas_sistema()
    usuarios_ativos = admin_service.consultar_usuarios_ativos()
    historico_recente = admin_service.consultar_historico_acessos(page=1, page_size=5)
    
    return {
        "success": True,
        "data": {
            "estatisticas": estatisticas,
            "usuarios_ativos": usuarios_ativos,
            "acessos_recentes": historico_recente["items"]
        }
    }

# Rota para listar usuários
@router.get("/users")
async def listar_usuarios(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    
    # Usar a mesma função de histórico mas adaptar para usuários se necessário
    historico = admin_service.consultar_historico_acessos(page=page, page_size=page_size)
    
    return {
        "success": True,
        "data": historico
    }

# Rota para obter detalhes de um usuário específico
@router.get("/users/{user_id}")
async def obter_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_service = AdminService(db)
    
    usuario = admin_service.consultar_usuario_por_id(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "success": True,
        "data": usuario
    }