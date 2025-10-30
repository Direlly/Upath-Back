from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NotificationBase(BaseModel):
    titulo: str
    tipo: str  # bolsa, curso, prazo
    mensagem: str

class NotificationResponse(NotificationBase):
    id: int
    lido: bool
    data_envio: datetime

    class Config:
        from_attributes = True

class NotificationSettings(BaseModel):
    notification_type: str
    enabled: bool