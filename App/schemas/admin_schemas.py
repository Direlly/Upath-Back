from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: str
    message: str

class PinValidationRequest(BaseModel):
    username: str
    pin: str

class PinValidationResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class AdminResponse(BaseModel):
    id: int
    username: str
    name: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        orm_mode = True

class AccessHistoryResponse(BaseModel):
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class PaginatedAccessHistory(BaseModel):
    items: List[AccessHistoryResponse]
    page: int
    page_size: int
    total: int
    total_pages: int
