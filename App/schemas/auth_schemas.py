from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    confirmar_senha: str  # Nome corrigido para match com auth_service

    @validator('confirmar_senha')
    def passwords_match(cls, v, values, **kwargs):
        if 'senha' in values and v != values['senha']:
            raise ValueError('Senhas não coincidem')
        return v

class AdminLogin(BaseModel):
    email: EmailStr
    senha: str

class AdminAuth(BaseModel):
    session_id: str
    pin: str
    
    @validator('pin')
    def validate_pin_length(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError('PIN deve conter exatamente 4 dígitos numéricos')
        return v

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    nova_senha: str
    confirmar_senha: str  # Nome corrigido

    @validator('confirmar_senha')
    def passwords_match(cls, v, values, **kwargs):
        if 'nova_senha' in values and v != values['nova_senha']:
            raise ValueError('Senhas não coincidem')
        return v

class ProfileUpdate(BaseModel):
    novo_nome: str

class PasswordUpdate(BaseModel):
    senha_atual: str
    nova_senha: str
    confirmar_senha: str

    @validator('confirmar_senha')
    def passwords_match(cls, v, values, **kwargs):
        if 'nova_senha' in values and v != values['nova_senha']:
            raise ValueError('Senhas não coincidem')
        return v