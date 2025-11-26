from sqlalchemy.orm import Session
from typing import Dict, Any
import re
from datetime import datetime

from models.auth import Usuario
from core.security import verify_password, get_password_hash, validate_password_strength

class PerfilService:
    """
    Service para operações de perfil do usuário conforme documentação
    - Tela de Editar Perfil (/perfil)
    - Atualização de nome e senha
    """

    def __init__(self, db: Session):
        self.db = db

    def obter_dados_perfil(self, user_id: int) -> Dict[str, Any]:
        """
        Obtém dados do perfil para exibição
        Conforme Tela de Editar Perfil na documentação
        """
        try:
            usuario = self.db.query(Usuario).filter(
                Usuario.id_usuario == user_id,
                Usuario.status_conta == 'ativo'
            ).first()

            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            return {
                "success": True,
                "data": {
                    "nome": usuario.nome,
                    "email": usuario.email
                }
            }

        except Exception as e:
            return {"success": False, "mensagem": f"Erro ao obter perfil: {str(e)}"}

    def atualizar_nome(self, user_id: int, novo_nome: str) -> Dict[str, Any]:
        """
        Atualiza apenas o nome do usuário
        Conforme documentação: "Back-End tem que enviar a requisição de edição de perfil, com nome e senha como dados alterados"
        """
        try:
            usuario = self.db.query(Usuario).filter(
                Usuario.id_usuario == user_id,
                Usuario.status_conta == 'ativo'
            ).first()

            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            # Validação do nome conforme documentação
            if not self._validar_nome(novo_nome):
                return {"success": False, "mensagem": "Nome deve conter apenas letras e espaços (2-100 caracteres)"}

            usuario.nome = novo_nome.strip()
            usuario.data_atualizacao = datetime.utcnow()
            self.db.commit()

            return {
                "success": True,
                "mensagem": "Nome atualizado com sucesso",
                "data": {
                    "novo_nome": usuario.nome
                }
            }

        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao atualizar nome: {str(e)}"}

    def alterar_senha(self, user_id: int, nova_senha: str, confirmar_senha: str) -> Dict[str, Any]:
        """
        Altera a senha do usuário
        Conforme documentação: senha deve seguir padrão (8 dígitos com letra maiúscula, minúscula, número, caractere especial)
        """
        try:
            usuario = self.db.query(Usuario).filter(
                Usuario.id_usuario == user_id,
                Usuario.status_conta == 'ativo'
            ).first()

            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            # Verificar se as senhas coincidem
            if nova_senha != confirmar_senha:
                return {"success": False, "mensagem": "As senhas não coincidem"}

            # Validar força da senha conforme documentação
            if not validate_password_strength(nova_senha):
                return {
                    "success": False, 
                    "mensagem": "Senha deve ter: mínimo 8 caracteres, letra maiúscula, letra minúscula, número e caractere especial"
                }

            # Atualizar senha
            usuario.senha_hash = get_password_hash(nova_senha)
            usuario.data_atualizacao = datetime.utcnow()
            self.db.commit()

            return {
                "success": True,
                "mensagem": "Senha alterada com sucesso"
            }

        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao alterar senha: {str(e)}"}

    def atualizar_perfil_completo(self, user_id: int, novo_nome: str, nova_senha: str, confirmar_senha: str) -> Dict[str, Any]:
        """
        Atualiza nome e senha simultaneamente
        Conforme documentação: "Back-End tem que enviar a requisição de edição de perfil, com nome e senha como dados alterados"
        """
        try:
            usuario = self.db.query(Usuario).filter(
                Usuario.id_usuario == user_id,
                Usuario.status_conta == 'ativo'
            ).first()

            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            resultados = {}
            
            # Atualizar nome se fornecido
            if novo_nome and novo_nome.strip():
                if not self._validar_nome(novo_nome):
                    return {"success": False, "mensagem": "Nome deve conter apenas letras e espaços (2-100 caracteres)"}
                
                usuario.nome = novo_nome.strip()
                resultados["nome_atualizado"] = True

            # Atualizar senha se fornecida
            if nova_senha and confirmar_senha:
                if nova_senha != confirmar_senha:
                    return {"success": False, "mensagem": "As senhas não coincidem"}

                if not validate_password_strength(nova_senha):
                    return {
                        "success": False, 
                        "mensagem": "Senha deve ter: mínimo 8 caracteres, letra maiúscula, letra minúscula, número e caractere especial"
                    }

                usuario.senha_hash = get_password_hash(nova_senha)
                resultados["senha_atualizada"] = True

            if not resultados:
                return {"success": False, "mensagem": "Nenhum dado fornecido para atualização"}

            usuario.data_atualizacao = datetime.utcnow()
            self.db.commit()

            mensagem = "Perfil atualizado com sucesso"
            if resultados.get("nome_atualizado") and resultados.get("senha_atualizada"):
                mensagem = "Nome e senha atualizados com sucesso"
            elif resultados.get("nome_atualizado"):
                mensagem = "Nome atualizado com sucesso"
            elif resultados.get("senha_atualizada"):
                mensagem = "Senha atualizada com sucesso"

            return {
                "success": True,
                "mensagem": mensagem,
                "data": resultados
            }

        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao atualizar perfil: {str(e)}"}

    def _validar_nome(self, nome: str) -> bool:
        """
        Valida o formato do nome
        """
        nome_limpo = nome.strip()
        if len(nome_limpo) < 2 or len(nome_limpo) > 100:
            return False
        return bool(re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome_limpo))