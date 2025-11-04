from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from auth import Base
import datetime

class Notificacao(Base):
    __tablename__ = 'notificacao'
    
    id_notificacao = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    mensagem = Column(Text, nullable=False)
    tipo = Column(Enum('prazo', 'status', 'alerta', name='tipo_notificacao_enum'), nullable=False)
    status = Column(Enum('pendente', 'enviado', 'lido', name='status_notificacao_enum'), default='pendente')
    data_envio = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="notificacoes")

class Relatorio(Base):
    __tablename__ = 'relatorio'
    
    id_relatorio = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    tipo = Column(String(100))
    filtros = Column(Text)
    data_geracao = Column(DateTime, default=datetime.datetime.utcnow)
    arquivo_exportado = Column(String(255))
    
    # Relationships
    usuario = relationship("Usuario", back_populates="relatorios")