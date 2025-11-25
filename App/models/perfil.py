from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Administrador(Base):
    __tablename__ = "administradores"
    
    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    nivel_permissao = Column(String(50), default='superadmin')
    ativo = Column(Boolean, default=True)
    data_ultimo_login = Column(DateTime, nullable=True) 

    usuario = relationship("Usuario", back_populates="administrador")


