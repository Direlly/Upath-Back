from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from datetime import datetime

class TokenBase(BaseModel):
    """Base para schemas de token"""
    token: str

class PasswordResetTokenRequest(BaseModel):
    """Schema para solicitação de token de reset de senha"""
    email: str

class PasswordResetTokenCreate(BaseModel):
    """Schema para criação de token de reset"""
    user_id: int

class PasswordResetTokenResponse(BaseModel):
    """Resposta com token de reset"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class PasswordResetTokenValidate(BaseModel):
    """Schema para validação de token de reset"""
    token: str

class PasswordResetTokenValidateResponse(BaseModel):
    """Resposta da validação de token"""
    valido: bool
    id_usuario: Optional[int] = None
    data_expiracao: Optional[datetime] = None
    mensagem: Optional[str] = None

class AdminPINCreate(BaseModel):
    """Schema para criação de PIN de administrador"""
    admin_id: int

class AdminPINResponse(BaseModel):
    """Resposta com PIN de administrador"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class AdminPINValidate(BaseModel):
    """Schema para validação de PIN de administrador"""
    admin_id: int
    pin: str
    
    @validator('pin')
    def validate_pin_length(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError('PIN deve conter exatamente 4 dígitos numéricos')
        return v

class AdminPINValidateResponse(BaseModel):
    """Resposta da validação de PIN"""
    valido: bool
    mensagem: str
    data_criacao: Optional[datetime] = None

class AdminPINAtivoResponse(BaseModel):
    """Resposta com PIN ativo"""
    pin: str
    data_expiracao: datetime
    data_criacao: datetime

class TokenCleanupResponse(BaseModel):
    """Resposta da limpeza de tokens expirados"""
    success: bool
    tokens_expirados_removidos: int
    pins_expirados_removidos: int
    mensagem: Optional[str] = None

class RefreshTokenCreate(BaseModel):
    """Schema para criação de refresh token"""
    user_id: int
    user_role: str = "student"

class RefreshTokenResponse(BaseModel):
    """Resposta com refresh token"""
    token: str
    expires_at: datetime
    user_id: int
    user_role: str

class RefreshTokenValidate(BaseModel):
    """Schema para validação de refresh token"""
    token: str

class RefreshTokenValidateResponse(BaseModel):
    """Resposta da validação de refresh token"""
    valido: bool
    user_id: Optional[int] = None
    user_role: Optional[str] = None
    expires_at: Optional[datetime] = None

class TokenBlacklistAdd(BaseModel):
    """Schema para adicionar token à lista negra"""
    token: str
    expires_at: datetime

class TokenBlacklistCheck(BaseModel):
    """Schema para verificar token na lista negra"""
    token: str

class TokenBlacklistResponse(BaseModel):
    """Resposta da verificação de lista negra"""
    blacklisted: bool