from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict, Any
from datetime import datetime

class UserLogin(BaseModel):
    """Schema para login de usuário"""
    email: EmailStr
    senha: str

class UserCreate(BaseModel):
    """Schema para criação de usuário"""
    nome: str
    email: EmailStr
    confirm_email: EmailStr
    senha: str
    confirmar_senha: str
    
    @validator('nome')
    def validate_nome(cls, v):
        import re
        v = v.strip()
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Nome deve ter entre 2 e 100 caracteres')
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        return v
    
    @validator('senha')
    def validate_senha(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 número')
        caracteres_especiais = '!@#$%^&*()_+-=[]{}|;:,.<>?`~'
        if not any(c in caracteres_especiais for c in v):
            raise ValueError('Senha deve ter pelo menos 1 caractere especial')
        return v
    
    @validator('confirmar_senha')
    def passwords_match(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('As senhas não coincidem')
        return v

class UserRegisterResponse(BaseModel):
    """Resposta do registro de usuário"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class UserLoginResponse(BaseModel):
    """Resposta do login de usuário"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class PasswordResetRequest(BaseModel):
    """Schema para solicitação de reset de senha"""
    email: EmailStr

class PasswordReset(BaseModel):
    """Schema para redefinição de senha"""
    token: str
    nova_senha: str
    confirmar_senha: str
    
    @validator('nova_senha')
    def validate_nova_senha(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 número')
        caracteres_especiais = '!@#$%^&*()_+-=[]{}|;:,.<>?`~'
        if not any(c in caracteres_especiais for c in v):
            raise ValueError('Senha deve ter pelo menos 1 caractere especial')
        return v
    
    @validator('confirmar_senha')
    def passwords_match(cls, v, values):
        if 'nova_senha' in values and v != values['nova_senha']:
            raise ValueError('As senhas não coincidem')
        return v

class PasswordResetResponse(BaseModel):
    """Resposta do reset de senha"""
    success: bool
    message: str

class ForgotPasswordResponse(BaseModel):
    """Resposta da solicitação de recuperação de senha"""
    success: bool
    message: str

class UserMeResponse(BaseModel):
    """Resposta com dados do usuário atual"""
    success: bool
    data: Dict[str, Any]

class LogoutResponse(BaseModel):
    """Resposta do logout"""
    success: bool
    message: str