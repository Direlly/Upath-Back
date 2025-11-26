from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    status_conta = Column(String(20), default='ativo')  # ativo, bloqueado, inativo
    role = Column(String(20), default='student')  # student, admin
    
    # Relacionamentos
    perfil = relationship("Perfil", back_populates="usuario", uselist=False)
    tokens_recuperacao = relationship("TokenRecuperacao", back_populates="usuario")
    historico_login = relationship("HistoricoLogin", back_populates="usuario")
    testes_vocacionais = relationship("TesteVocacional", back_populates="usuario")
    simulacoes_enem = relationship("SimulacaoENEM", back_populates="usuario")

class Perfil(Base):
    __tablename__ = "perfis"
    
    id_perfil = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    data_nascimento = Column(DateTime, nullable=True)
    genero = Column(String(20), nullable=True)
    escolaridade = Column(String(50), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    bio = Column(Text, nullable=True)
    foto_url = Column(String(255), nullable=True)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="perfil")

class TokenRecuperacao(Base):
    __tablename__ = "tokens_recuperacao"
    
    id_token = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    token = Column(String(100), unique=True, nullable=False, index=True)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_expiracao = Column(DateTime, nullable=False)
    utilizado = Column(Boolean, default=False)
    data_utilizacao = Column(DateTime, nullable=True)
    
    usuario = relationship("Usuario", back_populates="tokens_recuperacao")

class HistoricoLogin(Base):
    __tablename__ = "historico_login"
    
    id_historico = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    data_login = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    dispositivo = Column(String(100), nullable=True)
    
    usuario = relationship("Usuario", back_populates="historico_login")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id_refresh_token = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    user_role = Column(String(20), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime, nullable=True)

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    
    id_blacklist = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)