from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import secrets
from models.auth import RefreshToken, PasswordResetToken, AdminSession
from core.config import settings

class TokenService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_refresh_token(self, user_id: int) -> RefreshToken:
        # Revogar tokens antigos do usuário
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).update({"is_revoked": True})
        
        # Criar novo token
        token = secrets.token_urlsafe(64)
        expires_at = datetime.utcnow() + timedelta(days=30)  # 30 dias
        
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token
    
    def verify_refresh_token(self, token: str) -> Optional[RefreshToken]:
        """Verifica se o refresh token é válido"""
        return self.db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
    
    def revoke_refresh_token(self, token: str) -> bool:
        """Revoga um refresh token"""
        refresh_token = self.db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first()
        
        if refresh_token:
            refresh_token.is_revoked = True # type: ignore
            self.db.commit()
            return True
        return False
    
    def create_password_reset_token(self, user_id: int) -> PasswordResetToken:
        # Invalidar tokens antigos
        self.db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.is_used == False
        ).update({"is_used": True})
        
        # Criar novo token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hora
        
        reset_token = PasswordResetToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        
        self.db.add(reset_token)
        self.db.commit()
        self.db.refresh(reset_token)
        return reset_token
    
    def verify_password_reset_token(self, token: str) -> Optional[PasswordResetToken]:
        """Verifica se o token de reset de senha é válido"""
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).first()
    
    def use_password_reset_token(self, token: str) -> bool:
        """Marca um token de reset de senha como usado"""
        reset_token = self.verify_password_reset_token(token)
        if reset_token:
            reset_token.is_used = True # type: ignore
            self.db.commit()
            return True
        return False

class AdminAuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_admin_session(self, admin_email: str) -> AdminSession:
        """Cria uma nova sessão administrativa com PIN 2FA"""
        session_id = secrets.token_hex(16)
        pin_code = str(secrets.randbelow(10000)).zfill(4)
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # 10 minutos
        
        # Limpar sessões expiradas
        self.db.query(AdminSession).filter(
            AdminSession.expires_at < datetime.utcnow()
        ).delete()
        
        session = AdminSession(
            session_id=session_id,
            admin_email=admin_email,
            pin_code=pin_code,
            expires_at=expires_at
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def verify_admin_session(self, session_id: str, pin_code: str) -> Optional[AdminSession]:
        """Verifica se a sessão administrativa e PIN são válidos"""
        return self.db.query(AdminSession).filter(
            AdminSession.session_id == session_id,
            AdminSession.pin_code == pin_code,
            AdminSession.is_used == False,
            AdminSession.expires_at > datetime.utcnow()
        ).first()
    
    def mark_admin_session_used(self, session_id: str) -> bool:
        """Marca uma sessão administrativa como usada"""
        session = self.db.query(AdminSession).filter(
            AdminSession.session_id == session_id
        ).first()
        
        if session:
            session.is_used = True # type: ignore
            self.db.commit()
            return True
        return False