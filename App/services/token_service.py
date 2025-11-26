from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import string
from typing import Optional, Dict, Any

from models.auth import PasswordResetToken, AdminPIN

class TokenService:
    """
    Service para gerenciamento de tokens conforme documentação
    - Tokens de recuperação de senha
    - PIN de administrador (4 dígitos numéricos)
    """

    def __init__(self, db: Session):
        self.db = db

    # === TOKENS DE RECUPERAÇÃO DE SENHA ===
    def criar_token_recuperacao_senha(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Cria token para recuperação de senha
        Conforme Tela de Esquecimento/Recuperação na documentação
        """
        try:
            # Invalidar tokens antigos do usuário
            self.db.query(PasswordResetToken).filter(
                PasswordResetToken.id_usuario == user_id,
                PasswordResetToken.utilizado == False
            ).update({"utilizado": True})

            # Gerar token seguro
            token = self._gerar_token_seguro(32)
            data_expiracao = datetime.utcnow() + timedelta(hours=24)  # 24 horas conforme doc

            # Criar novo token
            token_recuperacao = PasswordResetToken(
                id_usuario=user_id,
                token=token,
                data_expiracao=data_expiracao,
                utilizado=False,
                data_criacao=datetime.utcnow()
            )

            self.db.add(token_recuperacao)
            self.db.commit()
            self.db.refresh(token_recuperacao)

            return {
                "token": token,
                "data_expiracao": data_expiracao,
                "id_usuario": user_id
            }

        except Exception as e:
            self.db.rollback()
            print(f"Erro ao criar token de recuperação: {e}")
            return None

    def validar_token_recuperacao(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida token de recuperação de senha
        Conforme fluxo de redefinição na documentação
        """
        try:
            token_recuperacao = self.db.query(PasswordResetToken).filter(
                PasswordResetToken.token == token,
                PasswordResetToken.utilizado == False,
                PasswordResetToken.data_expiracao > datetime.utcnow()
            ).first()

            if not token_recuperacao:
                return None

            return {
                "valido": True,
                "id_usuario": token_recuperacao.id_usuario,
                "data_expiracao": token_recuperacao.data_expiracao
            }

        except Exception as e:
            print(f"Erro ao validar token de recuperação: {e}")
            return None

    def invalidar_token_recuperacao(self, token: str) -> bool:
        """
        Marca token de recuperação como utilizado
        """
        try:
            token_recuperacao = self.db.query(PasswordResetToken).filter(
                PasswordResetToken.token == token
            ).first()

            if token_recuperacao:
                token_recuperacao.utilizado = True
                token_recuperacao.data_utilizacao = datetime.utcnow()
                self.db.commit()
                return True
            return False

        except Exception as e:
            self.db.rollback()
            print(f"Erro ao invalidar token: {e}")
            return False

    # === PIN DE ADMINISTRADOR ===
    def criar_pin_administrador(self, admin_id: int) -> Optional[Dict[str, Any]]:
        """
        Cria PIN de 4 dígitos para autenticação de administrador
        Conforme Tela de Autenticação (/auth) na documentação: "PIN (4 dígitos numéricos)"
        """
        try:
            # Limpar PINs antigos do administrador
            self.db.query(AdminPIN).filter(
                AdminPIN.id_admin == admin_id,
                AdminPIN.utilizado == False
            ).update({"utilizado": True})

            # Gerar PIN de 4 dígitos numéricos
            pin = str(secrets.randbelow(10000)).zfill(4)
            data_expiracao = datetime.utcnow() + timedelta(minutes=10)  # 10 minutos

            # Criar novo PIN
            admin_pin = AdminPIN(
                id_admin=admin_id,
                pin=pin,
                data_expiracao=data_expiracao,
                utilizado=False,
                data_criacao=datetime.utcnow()
            )

            self.db.add(admin_pin)
            self.db.commit()
            self.db.refresh(admin_pin)

            return {
                "pin": pin,
                "data_expiracao": data_expiracao,
                "id_admin": admin_id
            }

        except Exception as e:
            self.db.rollback()
            print(f"Erro ao criar PIN admin: {e}")
            return None

    def validar_pin_administrador(self, admin_id: int, pin: str) -> Dict[str, Any]:
        """
        Valida PIN do administrador
        Conforme documentação: "Ao validar a identidade com o PIN (4 dígitos numéricos)"
        """
        try:
            # Primeiro validar formato do PIN
            if not self._validar_formato_pin(pin):
                return {
                    "valido": False,
                    "mensagem": "PIN deve conter exatamente 4 dígitos numéricos"
                }

            # Buscar PIN válido
            admin_pin = self.db.query(AdminPIN).filter(
                AdminPIN.id_admin == admin_id,
                AdminPIN.pin == pin,
                AdminPIN.utilizado == False,
                AdminPIN.data_expiracao > datetime.utcnow()
            ).first()

            if not admin_pin:
                return {
                    "valido": False,
                    "mensagem": "PIN inválido, expirado ou já utilizado"
                }

            # Marcar PIN como utilizado
            admin_pin.utilizado = True
            admin_pin.data_utilizacao = datetime.utcnow()
            self.db.commit()

            return {
                "valido": True,
                "mensagem": "PIN validado com sucesso",
                "data_criacao": admin_pin.data_criacao
            }

        except Exception as e:
            self.db.rollback()
            print(f"Erro ao validar PIN admin: {e}")
            return {
                "valido": False,
                "mensagem": f"Erro ao validar PIN: {str(e)}"
            }

    def obter_pin_ativo_administrador(self, admin_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém PIN ativo do administrador (se existir)
        """
        try:
            admin_pin = self.db.query(AdminPIN).filter(
                AdminPIN.id_admin == admin_id,
                AdminPIN.utilizado == False,
                AdminPIN.data_expiracao > datetime.utcnow()
            ).first()

            if admin_pin:
                return {
                    "pin": admin_pin.pin,
                    "data_expiracao": admin_pin.data_expiracao,
                    "data_criacao": admin_pin.data_criacao
                }
            return None

        except Exception as e:
            print(f"Erro ao obter PIN ativo: {e}")
            return None

    # === FUNÇÕES AUXILIARES ===
    def _gerar_token_seguro(self, length: int = 32) -> str:
        """
        Gera token seguro com caracteres alfanuméricos
        """
        caracteres = string.ascii_letters + string.digits
        return ''.join(secrets.choice(caracteres) for _ in range(length))

    def _validar_formato_pin(self, pin: str) -> bool:
        """
        Valida formato do PIN: exatamente 4 dígitos numéricos
        Conforme documentação: "PIN (4 dígitos numéricos)"
        """
        return len(pin) == 4 and pin.isdigit()

    def limpar_tokens_expirados(self) -> Dict[str, Any]:
        """
        Limpa tokens e PINs expirados do banco
        """
        try:
            agora = datetime.utcnow()
            
            # Limpar tokens de recuperação expirados
            tokens_expirados = self.db.query(PasswordResetToken).filter(
                PasswordResetToken.data_expiracao < agora
            ).delete()

            # Limpar PINs expirados
            pins_expirados = self.db.query(AdminPIN).filter(
                AdminPIN.data_expiracao < agora
            ).delete()

            self.db.commit()

            return {
                "success": True,
                "tokens_expirados_removidos": tokens_expirados,
                "pins_expirados_removidos": pins_expirados
            }

        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "mensagem": f"Erro ao limpar tokens expirados: {str(e)}"
            }