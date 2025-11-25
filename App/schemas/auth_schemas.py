from pydantic import BaseModel, EmailStr, validator
import re

class UserBase(BaseModel):
    nome: str
    email: EmailStr

class UserCreate(UserBase):
    confirmEmail: EmailStr
    senha: str
    confirmSenha: str

    @validator('nome')
    def validar_nome(cls, v):
        if not re.match(r'^[A-Za-zÀ-ÿ\s]{2,100}$', v.strip()):
            raise ValueError('Nome deve conter apenas letras e espaços')
        return v.strip()

    @validator('confirmEmail')
    def emails_coincidem(cls, v, values):
        if 'email' in values and v != values['email']:
            raise ValueError('Emails não coincidem')
        return v

    @validator('confirmSenha')
    def senhas_coincidem(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('Senhas não coincidem')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    id_usuario: int
    nome: str
    email: str
    role: str

    class Config:
        from_attributes = True

class PasswordUpdate(BaseModel):
    senha_atual: str
    nova_senha: str
    confirmar_senha: str

    @validator('confirmar_senha')
    def senhas_coincidem(cls, v, values):
        if 'nova_senha' in values and v != values['nova_senha']:
            raise ValueError('Senhas não coincidem')
        return v

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    nova_senha: str
    confirmar_senha: str

    @validator('confirmar_senha')
    def senhas_coincidem(cls, v, values):
        if 'nova_senha' in values and v != values['nova_senha']:
            raise ValueError('Senhas não coincidem')
        return v