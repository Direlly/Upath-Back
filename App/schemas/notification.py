from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schemas para notificações
class NotificationBase(BaseModel):
    titulo: str
    tipo: str  # bolsa, curso, prazo
    mensagem: str

# Schema para resposta de notificação
class NotificationResponse(NotificationBase):
    id: int
    lido: bool
    data_envio: datetime

    class Config:
        from_attributes = True

# Schema para configurações de notificação do usuário
class NotificationSettings(BaseModel):
    notification_type: str
    enabled: bool