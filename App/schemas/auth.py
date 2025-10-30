from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TokenBase(BaseModel):
    token: str
    token_type: str = "bearer"

class TokenResponse(TokenBase):
    user_id: int
    email: str
    role: str
    expires_in: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    confirm_password: str

class AdminLoginRequest(BaseModel):
    email: EmailStr
    senha: str

class Admin2FARequest(BaseModel):
    session_id: str
    token_4d: str

class AdminSessionResponse(BaseModel):
    session_id: str
    expires_at: datetime

class AuditLogResponse(BaseModel):
    id: int
    acao: str
    alvo: str
    admin_email: Optional[str]
    user_id: Optional[int]
    ip_address: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True