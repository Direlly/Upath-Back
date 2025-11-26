from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from models.auth import Base

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    nivel_permissao = Column(String(50), default='admin')  # admin, superadmin
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_ultimo_login = Column(DateTime, nullable=True)
    
    # Relacionamentos
    pins = relationship("AdminPIN", back_populates="admin")
    acoes = relationship("AdminAcao", back_populates="admin")

class AdminPIN(Base):
    __tablename__ = "admin_pins"
    
    id_pin = Column(Integer, primary_key=True, autoincrement=True)
    id_admin = Column(Integer, ForeignKey('admins.id'), nullable=False)
    pin = Column(String(4), nullable=False)  # PIN de 4 dígitos em texto puro (será hasheado no service)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_expiracao = Column(DateTime, nullable=False)
    utilizado = Column(Boolean, default=False)
    data_utilizacao = Column(DateTime, nullable=True)
    
    admin = relationship("Admin", back_populates="pins")

class AdminSession(Base):
    __tablename__ = "admin_sessions"
    
    id_session = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(32), unique=True, nullable=False, index=True)
    admin_email = Column(String(100), nullable=False)
    pin_code = Column(String(4), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)

class AdminAcao(Base):
    __tablename__ = "admin_acoes"
    
    id_acao = Column(Integer, primary_key=True, autoincrement=True)
    id_admin = Column(Integer, ForeignKey('admins.id'), nullable=False)
    tipo_acao = Column(String(50), nullable=False)  # bloquear_usuario, desbloquear_usuario, excluir_usuario, resetar_senha
    id_usuario_alvo = Column(Integer, nullable=True)
    descricao = Column(Text, nullable=True)
    data_acao = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    
    admin = relationship("Admin", back_populates="acoes")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)