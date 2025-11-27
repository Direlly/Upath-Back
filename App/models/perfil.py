from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    foto_url = Column(String(255), nullable=True)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    status_conta = Column(String(20), default='ativo')
    ultimo_login = Column(DateTime, nullable=True)
    
    # Relacionamentos
    perfil = relationship("Perfil", back_populates="usuario", uselist=False)
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)
    tokens_recuperacao = relationship("TokenRecuperacao", back_populates="usuario")

class Perfil(Base):
    __tablename__ = "perfis"
    
    id_perfil = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    nivel_acesso = Column(String(50), default='estudante')
    bio = Column(Text, nullable=True)
    telefone = Column(String(20), nullable=True)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="perfil")

class Administrador(Base):
    __tablename__ = "administradores"
    
    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    nivel_permissao = Column(String(50), default='superadmin')
    ativo = Column(Boolean, default=True)
    data_ultimo_login = Column(DateTime, nullable=True) 

    usuario = relationship("Usuario", back_populates="administrador")