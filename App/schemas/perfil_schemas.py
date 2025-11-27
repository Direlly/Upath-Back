from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    nome: str
    email: EmailStr

class UserCreate(UserBase):
    confirmEmail: EmailStr
    senha: str
    confirmSenha: str
    
    @validator('nome')
    def validate_nome(cls, v):
        import re
        if not re.match(r'^[A-Za-zÀ-ÿ\s]{2,100}$', v):
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
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in v):
            raise ValueError('Senha deve ter pelo menos 1 caractere especial')
        return v
    
    @validator('confirmSenha')
    def passwords_match(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('Senhas não coincidem')
        return v
    
    @validator('confirmEmail')
    def emails_match(cls, v, values):
        if 'email' in values and v != values['email']:
            raise ValueError('Emails não coincidem')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserResponse(UserBase):
    id: int
    foto_url: Optional[str] = None
    role: str = "student"
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    nome: Optional[str] = None
    foto_url: Optional[str] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve ter pelo menos 1 número')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in v):
            raise ValueError('Senha deve ter pelo menos 1 caractere especial')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Senhas não coincidem')
        return v