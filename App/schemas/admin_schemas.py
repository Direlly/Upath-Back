from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List, Dict, Any

class AdminLogin(BaseModel):
    """Schema para login de administrador"""
    email: EmailStr
    senha: str

class AdminAuth(BaseModel):
    """Schema para autenticação com PIN do administrador"""
    session_id: str
    pin: str
    
    @validator('pin')
    def validate_pin_length(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError('PIN deve conter exatamente 4 dígitos numéricos')
        return v

class AdminLoginResponse(BaseModel):
    """Resposta do login de administrador"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class AdminAuthResponse(BaseModel):
    """Resposta da autenticação com PIN"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class AdminProfileResponse(BaseModel):
    """Resposta com dados do administrador"""
    id: int
    email: str
    nome: str
    role: str = "admin"

    class Config:
        from_attributes = True

class UserSearchRequest(BaseModel):
    """Schema para pesquisa de usuário por ID"""
    user_id: Optional[str] = None

class UserCardResponse(BaseModel):
    """Schema para card do usuário no admin"""
    id: int
    nome: str
    email: str
    status: str
    ultimo_login: Optional[datetime]
    reset_pendente: bool
    data_cadastro: datetime

class UserListResponse(BaseModel):
    """Resposta com lista de usuários"""
    usuarios: List[UserCardResponse]
    pagina: int
    por_pagina: int
    total: int
    total_paginas: int

class UserActionResponse(BaseModel):
    """Resposta para ações em usuários"""
    success: bool
    message: str

class MetricsRequest(BaseModel):
    """Schema para filtro de métricas"""
    periodo: str = "diario"  # diario, semanal, mensal
    
    @validator('periodo')
    def validate_periodo(cls, v):
        if v not in ['diario', 'semanal', 'mensal']:
            raise ValueError('Período deve ser: diario, semanal ou mensal')
        return v

class MetricsResponse(BaseModel):
    """Resposta com métricas de usuários"""
    usuarios_ativos: int
    novos_usuarios: int
    logins_por_dia: List[Dict[str, Any]]
    periodo: str

class AdminStatsResponse(BaseModel):
    """Estatísticas do dashboard administrativo"""
    total_usuarios: int
    usuarios_ativos: int
    usuarios_bloqueados: int
    logins_24h: int

class AdminHomeResponse(BaseModel):
    """Resposta da home do administrador"""
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None