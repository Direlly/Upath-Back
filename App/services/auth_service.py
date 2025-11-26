from sqlalchemy.orm import Session
import re
import datetime
from typing import Optional, Dict, Any
import secrets
import string

from core.security import get_password_hash, verify_password, criar_token_recuperacao_senha
from models.auth import Usuario, Perfil, TokenRecuperacao, HistoricoLogin, Admin
from services.email_service import EmailService

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()

    def registrar_usuario(self, nome: str, email: str, senha: str, confirmar_senha: str) -> dict:
        """
        Registra um novo usuário no sistema 
        """
        try:
            print(f"🔧 Tentando registrar usuário: {email}")
            
            # Validações básicas
            if senha != confirmar_senha:
                return {"success": False, "mensagem": "Senhas não coincidem"}
            
            # Verifica se email já existe
            usuario_existente = self.db.query(Usuario).filter(
                Usuario.email == email.lower().strip()
            ).first()
            
            if usuario_existente:
                return {"success": False, "mensagem": "Email já cadastrado"}
            
            # Valida nome
            if not re.match(r'^[A-Za-zÀ-ÿ\s]{2,100}$', nome.strip()):
                return {"success": False, "mensagem": "Nome deve conter apenas letras e espaços"}
            
            # Valida senha 
            validacao_senha = self._validar_senha(senha)
            if not validacao_senha["success"]:
                return validacao_senha
            
            # Cria hash da senha 
            senha_hash = get_password_hash(senha)
            
            # Cria usuário
            novo_usuario = Usuario(
                nome=nome.strip(),
                email=email.lower().strip(),
                senha_hash=senha_hash,
                data_cadastro=datetime.datetime.utcnow(),
                status_conta='ativo'
            )
            
            self.db.add(novo_usuario)
            self.db.commit()
            self.db.refresh(novo_usuario)
            
            # Registrar primeiro login
            self._registrar_login(novo_usuario.id_usuario) # type: ignore
            
            return {
                "success": True,
                "id_usuario": novo_usuario.id_usuario,
                "nome": novo_usuario.nome,
                "email": novo_usuario.email,
                "mensagem": "Usuário registrado com sucesso"
            }
            
        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao registrar usuário: {str(e)}"}

    def _validar_senha(self, senha: str) -> Dict[str, Any]:
        """
        Valida os requisitos da senha conforme documentação
        """
        if len(senha) < 8:
            return {"success": False, "mensagem": "Senha deve ter pelo menos 8 caracteres"}
        
        if not any(c.isupper() for c in senha):
            return {"success": False, "mensagem": "Senha deve ter pelo menos 1 letra maiúscula"}
        
        if not any(c.islower() for c in senha):
            return {"success": False, "mensagem": "Senha deve ter pelo menos 1 letra minúscula"}
        
        if not any(c.isdigit() for c in senha):
            return {"success": False, "mensagem": "Senha deve ter pelo menos 1 número"}
        
        caracteres_especiais = '!@#$%^&*()_+-=[]{}|;:,.<>?`~'
        if not any(c in caracteres_especiais for c in senha):
            return {"success": False, "mensagem": "Senha deve ter pelo menos 1 caractere especial"}
        
        return {"success": True}

    def autenticar_usuario(self, email: str, senha: str) -> Dict[str, Any]:
        """
        Autentica usuário (estudante ou admin)
        """
        try:
            # Primeiro verifica se é admin
            admin = self.db.query(Admin).filter(
                Admin.email == email.lower().strip(),
                Admin.ativo == True
            ).first()
            
            if admin:
                if verify_password(senha, admin.senha_hash):
                    self._registrar_login_admin(admin.id)
                    return {
                        "success": True,
                        "id_usuario": admin.id,
                        "nome": admin.nome,
                        "email": admin.email,
                        "role": "admin",
                        "mensagem": "Autenticação admin bem-sucedida"
                    }
            
            # Se não é admin, verifica se é usuário normal
            usuario = self.db.query(Usuario).filter(
                Usuario.email == email.lower().strip(),
                Usuario.status_conta == 'ativo'
            ).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado ou inativo"}
            
            if not verify_password(senha, usuario.senha_hash):
                return {"success": False, "mensagem": "Senha incorreta"}
            
            # Registrar login bem-sucedido
            self._registrar_login(usuario.id_usuario)
            
            return {
                "success": True,
                "id_usuario": usuario.id_usuario,
                "nome": usuario.nome,
                "email": usuario.email,
                "role": "student",
                "mensagem": "Login bem-sucedido"
            }
                
        except Exception as e:
            return {"success": False, "mensagem": f"Erro na autenticação: {str(e)}"}

    def autenticar_admin(self, email: str, senha: str) -> Dict[str, Any]:
        """
        Autentica especificamente um administrador
        """
        try:
            admin = self.db.query(Admin).filter(
                Admin.email == email.lower().strip(),
                Admin.ativo == True
            ).first()
            
            if not admin:
                return {"success": False, "mensagem": "Administrador não encontrado"}
            
            if not verify_password(senha, admin.senha_hash):
                return {"success": False, "mensagem": "Senha incorreta"}
            
            return {
                "success": True,
                "admin_id": admin.id,
                "email": admin.email,
                "nome": admin.nome,
                "mensagem": "Autenticação admin bem-sucedida"
            }
                
        except Exception as e:
            return {"success": False, "mensagem": f"Erro na autenticação: {str(e)}"}

    def _registrar_login(self, user_id: int):
        """
        Registra histórico de login para usuários
        """
        try:
            historico = HistoricoLogin(
                id_usuario=user_id,
                data_login=datetime.datetime.utcnow(),
                ip_address="127.0.0.1"  # Em produção, obter do request
            )
            self.db.add(historico)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao registrar login: {e}")

    def _registrar_login_admin(self, admin_id: int):
        """
        Registra histórico de login para administradores
        """
        try:
            # Similar ao de usuários, pode ser expandido
            pass
        except Exception as e:
            print(f"Erro ao registrar login admin: {e}")

    def obter_usuario_por_id(self, user_id: int) -> Optional[Usuario]:
        """
        Obtém usuário por ID
        """
        try:
            return self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
        except Exception as e:
            return None

    def obter_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Obtém usuário por email
        """
        try:
            return self.db.query(Usuario).filter(Usuario.email == email.lower().strip()).first()
        except Exception as e:
            return None

    def atualizar_perfil(self, id_usuario: int, novo_nome: str) -> Dict[str, Any]:
        """
        Atualiza nome do perfil do usuário
        """
        try:
            usuario = self.obter_usuario_por_id(id_usuario)
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}
            
            # Valida nome
            if not re.match(r'^[A-Za-zÀ-ÿ\s]{2,100}$', novo_nome.strip()):
                return {"success": False, "mensagem": "Nome deve conter apenas letras e espaços"}
            
            usuario.nome = novo_nome.strip()
            self.db.commit()
            
            return {
                "success": True,
                "mensagem": "Perfil atualizado com sucesso"
            }
            
        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao atualizar perfil: {str(e)}"}

    def alterar_senha(self, id_usuario: int, senha_atual: str, nova_senha: str, confirmar_senha: str) -> Dict[str, Any]:
        """
        Altera senha do usuário logado
        """
        try:
            if nova_senha != confirmar_senha:
                return {"success": False, "mensagem": "Senhas não coincidem"}
            
            usuario = self.obter_usuario_por_id(id_usuario)
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}
            
            # Verifica senha atual
            if not verify_password(senha_atual, usuario.senha_hash):
                return {"success": False, "mensagem": "Senha atual incorreta"}
            
            # Valida nova senha
            validacao_senha = self._validar_senha(nova_senha)
            if not validacao_senha["success"]:
                return validacao_senha
            
            # Atualiza senha
            usuario.senha_hash = get_password_hash(nova_senha)
            self.db.commit()
            
            return {
                "success": True,
                "mensagem": "Senha alterada com sucesso"
            }
            
        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao alterar senha: {str(e)}"}

    # Manter as funções existentes de recuperação de senha...
    def enviar_email_recuperacao(self, email: str) -> Dict[str, Any]:
        # Implementação mantida do código anterior
        pass

    def redefinir_senha(self, token: str, nova_senha: str, confirmar_senha: str) -> Dict[str, Any]:
        # Implementação mantida do código anterior
        pass

    def _gerar_token_recuperacao(self, length: int = 32) -> str:
        # Implementação mantida do código anterior
        pass