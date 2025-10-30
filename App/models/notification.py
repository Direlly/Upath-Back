from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    titulo = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)  # bolsa, curso, prazo, status, alerta
    mensagem = Column(Text, nullable=False)
    lido = Column(Boolean, default=False)
    data_envio = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="pendente")  # pendente, enviado, lido
    
    def __repr__(self):
        return f"<Notification {self.id} - {self.titulo}>"