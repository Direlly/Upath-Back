from sqlalchemy.orm import Session
import re
import datetime
from typing import Optional, Dict, Any
import secrets
import string

from core.security import get_password_hash, verify_password
from models.auth import Usuario, Perfil, TokenRecuperacao
from services.token_service import TokenService
from services.email_service import EmailService

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.token_service = TokenService(db)
        self.email_service = EmailService()

    def registrar_usuario(self, nome: str, email: str, confirm_email: str, 
                         senha: str, confirm_senha: str) -> dict:
        """
        Registra um novo usuário no sistema 
        """
        try:
            print(f"🔧 Tentando registrar usuário: {email}")
            
            # Validações básicas
            if email != confirm_email:
                return {"success": False, "mensagem": "Emails não coincidem"}
            
            if senha != confirm_senha:
                return {"success": False, "mensagem": "Senhas não coincidem"}
            
            # Verifica se email já existe
            usuario_existente = self.db.query(Usuario).filter(
                Usuario.email == email
            ).first()
            
            if usuario_existente:
                return {"success": False, "mensagem": "Email já cadastrado"}
            
            # Valida nome
            if not re.match(r'^[A-Za-zÀ-ÿ\s]{2,100}$', nome.strip()):
                return {"success": False, "mensagem": "Nome deve conter apenas letras e espaços"}
            
            # Valida senha 
            validacao_senha = self.validar_senha(senha)
            if not validacao_senha["success"]:
                return validacao_senha
            
            # Cria hash da senha 
            print("🔧 Gerando hash da senha...")
            senha_hash = get_password_hash(senha)
            print("✅ Hash gerado com sucesso")
            
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
            print(f"✅ Usuário criado com ID: {novo_usuario.id_usuario}")
            
            # Tenta criar perfil
            try:
                perfil = Perfil(
                    id_usuario=novo_usuario.id_usuario,
                    nivel_acesso="estudante"
                )
                self.db.add(perfil)
                self.db.commit()
                print("✅ Perfil criado com sucesso")
            except Exception as e:
                print(f"⚠️  Perfil não criado: {e}")
                self.db.rollback()
            
            return {
                "success": True,
                "id_usuario": novo_usuario.id_usuario,
                "nome": novo_usuario.nome,
                "email": novo_usuario.email,
                "mensagem": "Usuário registrado com sucesso"
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Erro no registro: {str(e)}")
            return {"success": False, "mensagem": f"Erro ao registrar usuário: {str(e)}"}

    def validar_senha(self, senha: str) -> Dict[str, Any]:
        """
        Valida os requisitos da senha
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

    def autenticar_usuario(self, email: str, senha: str) -> Optional[Usuario]:
        try:
            print(f"🔐 Tentando autenticar: {email}")
            
            usuario = self.db.query(Usuario).filter(
                Usuario.email == email.lower().strip(),
                Usuario.status_conta == 'ativo'
            ).first()
            
            if not usuario:
                print("❌ Usuário não encontrado ou inativo")
                return None
            
            print(f"✅ Usuário encontrado: {usuario.nome}")
            print(f"🔑 Verificando senha...")
            
            senha_correta = verify_password(senha, usuario.senha_hash) # type: ignore
            print(f"Senha correta: {senha_correta}")
            
            if not senha_correta:
                print("❌ Senha incorreta")
                return None
            
            print(f"✅ Autenticação bem-sucedida para: {usuario.email}")
            return usuario
                
        except Exception as e:
            print(f"💥 Erro na autenticação: {str(e)}")
            return None

    def enviar_email_recuperacao(self, email: str) -> Dict[str, Any]:
        """
        Envia email de recuperação de senha
        """
        try:
            # Verifica se usuário existe
            usuario = self.db.query(Usuario).filter(
                Usuario.email == email.lower().strip(),
                Usuario.status_conta == 'ativo'
            ).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Email não encontrado"}
            
            # Gera token de recuperação usando TokenService
            reset_token = self.token_service.create_password_reset_token(usuario.id_usuario) # type: ignore
            
            # Envia email usando EmailService
            email_enviado = self.email_service.send_password_reset_email(email, reset_token.token) # type: ignore
            
            if not email_enviado:
                return {"success": False, "mensagem": "Erro ao enviar email de recuperação"}
            
            print(f"📧 Email de recuperação enviado para {email}")
            
            return {
                "success": True, 
                "mensagem": "Email de recuperação enviado com sucesso"
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao enviar email de recuperação: {str(e)}")
            return {"success": False, "mensagem": f"Erro ao enviar email de recuperação: {str(e)}"}

    def redefinir_senha(self, token: str, nova_senha: str) -> Dict[str, Any]:
        """
        Redefine a senha do usuário usando token de recuperação
        """
        try:
            # Verifica token usando TokenService
            reset_token = self.token_service.verify_password_reset_token(token)
            
            if not reset_token:
                return {"success": False, "mensagem": "Token inválido ou expirado"}
            
            # Busca usuário
            usuario = self.db.query(Usuario).filter(
                Usuario.id_usuario == reset_token.user_id
            ).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}
            
            # Valida nova senha
            validacao_senha = self.validar_senha(nova_senha)
            if not validacao_senha["success"]:
                return validacao_senha
            
            # Atualiza senha
            usuario.senha_hash = get_password_hash(nova_senha) # type: ignore
            
            # Marca token como usado
            self.token_service.use_password_reset_token(token)
            
            self.db.commit()
            
            print(f"✅ Senha redefinida para usuário: {usuario.email}")
            
            return {
                "success": True, 
                "mensagem": "Senha redefinida com sucesso"
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao redefinir senha: {str(e)}")
            return {"success": False, "mensagem": f"Erro ao redefinir senha: {str(e)}"}

    def _gerar_token_recuperacao(self, length: int = 32) -> str:
        """
        Gera token aleatório para recuperação de senha
        """
        caracteres = string.ascii_letters + string.digits
        return ''.join(secrets.choice(caracteres) for _ in range(length))

    def alterar_senha(self, id_usuario: int, senha_atual: str, nova_senha: str) -> Dict[str, Any]:
        """
        Altera senha do usuário logado
        """
        try:
            usuario = self.db.query(Usuario).filter(
                Usuario.id_usuario == id_usuario
            ).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}
            
            # Verifica senha atual
            if not verify_password(senha_atual, usuario.senha_hash): # type: ignore
                return {"success": False, "mensagem": "Senha atual incorreta"}
            
            # Valida nova senha
            validacao_senha = self.validar_senha(nova_senha)
            if not validacao_senha["success"]:
                return validacao_senha
            
            # Atualiza senha
            usuario.senha_hash = get_password_hash(nova_senha) # type: ignore
            self.db.commit()
            
            return {
                "success": True,
                "mensagem": "Senha alterada com sucesso"
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao alterar senha: {str(e)}")
            return {"success": False, "mensagem": f"Erro ao alterar senha: {str(e)}"}