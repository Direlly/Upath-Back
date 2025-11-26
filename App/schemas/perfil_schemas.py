from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict, Any
from datetime import datetime

class ProfileBase(BaseModel):
    """Base para schemas de perfil"""
    nome: Optional[str] = None

class ProfileUpdate(ProfileBase):
    """Schema para atualização de perfil (apenas nome)"""
    novo_nome: str
    
    @validator('novo_nome')
    def validate_nome(cls, v):
        import re
        v = v.strip()
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Nome deve ter entre 2 e 100 caracteres')
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        return v

class PasswordUpdate(BaseModel):
    """Schema para atualização de senha"""
    senha_atual: str
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

class ProfileCompleteUpdate(BaseModel):
    """Schema para atualização completa do perfil (nome e senha)"""
    novo_nome: Optional[str] = None
    nova_senha: Optional[str] = None
    confirmar_senha: Optional[str] = None
    
    @validator('novo_nome')
    def validate_nome(cls, v):
        if v is None:
            return v
        import re
        v = v.strip()
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Nome deve ter entre 2 e 100 caracteres')
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        return v
    
    @validator('nova_senha')
    def validate_nova_senha(cls, v, values):
        if v is None:
            return v
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
        if 'nova_senha' in values and values['nova_senha'] is not None:
            if v != values['nova_senha']:
                raise ValueError('As senhas não coincidem')
        return v

class ProfileResponse(BaseModel):
    """Resposta com dados do perfil"""
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None

class UserProfileData(BaseModel):
    """Dados do usuário para resposta"""
    id: int
    nome: str
    email: EmailStr
    data_cadastro: datetime
    ultimo_login: Optional[datetime]
    status: str
    estatisticas: Optional[Dict[str, Any]] = None

class ProfileUpdateResponse(BaseModel):
    """Resposta da atualização de perfil"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class PasswordUpdateResponse(BaseModel):
    """Resposta da atualização de senha"""
    success: bool
    message: str