from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from core.database import Base
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha_hash = Column(String(64), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    status_conta = Column(Enum('ativo', 'inativo', 'suspenso', name='status_conta_enum'), default='ativo')
    
    # Relationships
    perfil = relationship("Perfil", back_populates="usuario", uselist=False)
    notificacoes = relationship("Notificacao", back_populates="usuario")
    simulacoes = relationship("Simulacao", back_populates="usuario")
    testes_vocacionais = relationship("TesteVocacional", back_populates="usuario")
    relatorios = relationship("Relatorio", back_populates="usuario")

class Perfil(Base):
    __tablename__ = 'perfil'
    
    id_perfil = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True)
    pin_seguranca = Column(String(6))
    nivel_acesso = Column(Enum('estudante', 'admin', name='nivel_acesso_enum'), default='estudante')
    
    # Relationships
    usuario = relationship("Usuario", back_populates="perfil")