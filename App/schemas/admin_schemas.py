from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: str
    message: str

class PinValidationRequest(BaseModel):
    session_id: str
    pin: str

class PinValidationResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    token: Optional[str] = None

class AdminResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    active: bool

    class Config:
        from_attributes = True

class AccessHistoryResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    timestamp: datetime

    class Config:
        from_attributes = True

class PaginatedAccessHistory(BaseModel):
    items: List[AccessHistoryResponse]
    page: int
    page_size: int
    total: int
    total_pages: int

class SystemStatsResponse(BaseModel):
    total_usuarios: int
    usuarios_ativos: int
    total_acessos: int
    acessos_hoje: int

class AdminStatsResponse(BaseModel):
    estatisticas: SystemStatsResponse
    usuarios_ativos: List[UserResponse]
    acessos_recentes: List[AccessHistoryResponse]