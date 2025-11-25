from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.auth_schemas import UserLogin, UserCreate, PasswordUpdate, PasswordResetRequest, PasswordReset
from services.auth_service import AuthService
from core.security import criar_token, get_current_user
from models.auth import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

@router.post("/register")
def registrar_usuario(dados: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    resultado = service.registrar_usuario(
        nome=dados.nome,
        email=dados.email,
        confirm_email=dados.confirmEmail,
        senha=dados.senha,
        confirm_senha=dados.confirmSenha
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
    
    token = criar_token({"sub": usuario.email, "id": usuario.id_usuario, "role": "student"})
    return {
        "success": True,
        "data": {
            "token": token,
            "usuario": {
                "id": usuario.id_usuario, 
                "nome": usuario.nome, 
                "email": usuario.email,
                "role": "student"
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

@router.get("/me")
def obter_usuario_atual(usuario_atual: dict = Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "usuario": usuario_atual
        }
    }

@router.post("/debug-auth")
def debug_autenticacao(email: str, senha: str, db: Session = Depends(get_db)):
    """
    Endpoint para debug da autenticação
    """
    from core.security import get_password_hash, verify_password
    
    service = AuthService(db)
    
    # Verifica se usuário existe
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    debug_info = {
        "usuario_existe": usuario is not None,
        "email": email,
        "senha_fornecida": senha,
        "hash_calculado": get_password_hash(senha) if usuario else "N/A"
    }
    
    if usuario:
        debug_info.update({
            "hash_armazenado": usuario.senha_hash,
            "senha_confere": verify_password(senha, usuario.senha_hash), # type: ignore
            "status_conta": usuario.status_conta
        })
    
    # Tenta autenticar
    usuario_autenticado = service.autenticar_usuario(email, senha)
    debug_info["autenticacao_sucesso"] = usuario_autenticado is not None
    
    return {"success": True, "debug": debug_info}