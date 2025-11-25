from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    status_conta = Column(String(20), default='ativo')

class Perfil(Base):
    __tablename__ = "perfis"
    
    id_perfil = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    nivel_acesso = Column(String(50), default='estudante')

class TokenRecuperacao(Base):
    __tablename__ = "tokens_recuperacao"
    
    id_token = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    token = Column(String(100), unique=True, nullable=False)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_expiracao = Column(DateTime, nullable=False)
    utilizado = Column(Boolean, default=False)