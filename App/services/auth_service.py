from sqlalchemy.orm import Session
from models.user import User
from core.security import get_password_hash, verify_password
from schemas.user import UserCreate
from datetime import datetime
from services.audit_service import AuditService
from fastapi import Request

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditService(db)
    
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate, request: Request = None) -> User:
        hashed_password = get_password_hash(user_data.senha)
        
        user = User(
            nome=user_data.nome,
            email=user_data.email,
            senha_hash=hashed_password
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Log de auditoria
        self.audit_service.log_action(
            acao="cadastro_usuario",
            alvo=f"Usuário {user.email}",
            user_id=user.id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            detalhes={"nome": user.nome, "email": user.email}
        )
        
        return user
    
    def authenticate_user(self, email: str, password: str, request: Request = None) -> User:
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.senha_hash):
            # Log de tentativa falha
            self.audit_service.log_action(
                acao="tentativa_login",
                alvo=f"Usuário {email}",
                ip_address=request.client.host if request else None,
                user_agent=request.headers.get("user-agent") if request else None,
                status="erro",
                detalhes={"motivo": "senha_incorreta"}
            )
            return None
        
        if not user.is_active:
            return None
        
        # Log de login bem-sucedido
        self.audit_service.log_action(
            acao="login",
            alvo=f"Usuário {user.email}",
            user_id=user.id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            status="sucesso"
        )
        
        return user
    
    def update_last_login(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_login = datetime.utcnow()
            self.db.commit()
    
    def verify_admin_credentials(self, email: str, password: str, request: Request = None) -> User:
        user = self.get_user_by_email(email)
        if not user or user.role != "admin":
            return None
        
        if not verify_password(password, user.senha_hash):
            # Log de tentativa admin falha
            self.audit_service.log_action(
                acao="tentativa_login_admin",
                alvo=f"Admin {email}",
                ip_address=request.client.host if request else None,
                user_agent=request.headers.get("user-agent") if request else None,
                status="erro",
                detalhes={"motivo": "credenciais_invalidas"}
            )
            return None
        
        return user