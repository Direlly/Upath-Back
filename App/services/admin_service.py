from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func, and_, or_
from passlib.context import CryptContext

from models.auth import Usuario, Admin, TokenRecuperacao, HistoricoLogin
from core.security import get_password_hash, verify_password
from services.email_service import EmailService

# Configuração do passlib para hashing seguro
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    """
    Service para operações administrativas completas
    """

    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()

    def autenticar_admin(self, email: str, senha: str) -> Dict[str, Any]:
        """
        Autentica administrador com email e senha
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
                "mensagem": "Autenticação bem-sucedida"
            }

        except Exception as e:
            return {"success": False, "mensagem": f"Erro na autenticação: {str(e)}"}

    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Obtém estatísticas para dashboard administrativo
        """
        try:
            total_usuarios = self.db.query(Usuario).count()
            usuarios_ativos = self.db.query(Usuario).filter(Usuario.status_conta == 'ativo').count()
            usuarios_bloqueados = self.db.query(Usuario).filter(Usuario.status_conta == 'bloqueado').count()
            
            # Logins nas últimas 24 horas
            logins_24h = self.db.query(HistoricoLogin).filter(
                HistoricoLogin.data_login >= datetime.utcnow() - timedelta(hours=24)
            ).count()

            return {
                "total_usuarios": total_usuarios,
                "usuarios_ativos": usuarios_ativos,
                "usuarios_bloqueados": usuarios_bloqueados,
                "logins_24h": logins_24h
            }
        except Exception as e:
            return {
                "total_usuarios": 0,
                "usuarios_ativos": 0,
                "usuarios_bloqueados": 0,
                "logins_24h": 0
            }

    def pesquisar_usuario_por_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Pesquisa usuário por ID
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
            
            if not usuario:
                return None

            # Obter último login
            ultimo_login = self.db.query(HistoricoLogin).filter(
                HistoricoLogin.id_usuario == usuario.id_usuario
            ).order_by(HistoricoLogin.data_login.desc()).first()

            # Verificar se há solicitação de reset pendente
            reset_pendente = self.db.query(TokenRecuperacao).filter(
                TokenRecuperacao.id_usuario == usuario.id_usuario,
                TokenRecuperacao.utilizado == False,
                TokenRecuperacao.data_expiracao > datetime.utcnow()
            ).first() is not None

            return {
                "id": usuario.id_usuario,
                "nome": usuario.nome,
                "email": usuario.email,
                "status": usuario.status_conta,
                "ultimo_login": ultimo_login.data_login if ultimo_login else None,
                "reset_pendente": reset_pendente,
                "data_cadastro": usuario.data_cadastro
            }
        except Exception as e:
            return None

    def listar_usuarios(self, pagina: int = 1, por_pagina: int = 20) -> Dict[str, Any]:
        """
        Lista todos os usuários com paginação
        """
        try:
            offset = (pagina - 1) * por_pagina
            
            usuarios = self.db.query(Usuario).offset(offset).limit(por_pagina).all()
            total = self.db.query(Usuario).count()

            usuarios_lista = []
            for usuario in usuarios:
                ultimo_login = self.db.query(HistoricoLogin).filter(
                    HistoricoLogin.id_usuario == usuario.id_usuario
                ).order_by(HistoricoLogin.data_login.desc()).first()

                usuarios_lista.append({
                    "id": usuario.id_usuario,
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "status": usuario.status_conta,
                    "ultimo_login": ultimo_login.data_login if ultimo_login else None,
                    "data_cadastro": usuario.data_cadastro
                })

            return {
                "usuarios": usuarios_lista,
                "pagina": pagina,
                "por_pagina": por_pagina,
                "total": total,
                "total_paginas": (total + por_pagina - 1) // por_pagina
            }
        except Exception as e:
            return {"usuarios": [], "pagina": pagina, "por_pagina": por_pagina, "total": 0, "total_paginas": 0}

    def bloquear_usuario(self, user_id: str) -> Dict[str, Any]:
        """
        Bloqueia um usuário
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            usuario.status_conta = 'bloqueado'
            self.db.commit()

            return {"success": True, "mensagem": "Usuário bloqueado com sucesso"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao bloquear usuário: {str(e)}"}

    def desbloquear_usuario(self, user_id: str) -> Dict[str, Any]:
        """
        Desbloqueia um usuário
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            usuario.status_conta = 'ativo'
            self.db.commit()

            return {"success": True, "mensagem": "Usuário desbloqueado com sucesso"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao desbloquear usuário: {str(e)}"}

    def excluir_usuario(self, user_id: str) -> Dict[str, Any]:
        """
        Exclui um usuário permanentemente
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            self.db.delete(usuario)
            self.db.commit()

            return {"success": True, "mensagem": "Usuário excluído com sucesso"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "mensagem": f"Erro ao excluir usuário: {str(e)}"}

    def resetar_senha_usuario(self, user_id: str) -> Dict[str, Any]:
        """
        Força reset de senha para um usuário
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            # Gerar token de recuperação
            from services.auth_service import AuthService
            auth_service = AuthService(self.db)
            resultado = auth_service.enviar_email_recuperacao(usuario.email)

            if resultado["success"]:
                return {"success": True, "mensagem": "Email de recuperação enviado com sucesso"}
            else:
                return {"success": False, "mensagem": resultado["mensagem"]}

        except Exception as e:
            return {"success": False, "mensagem": f"Erro ao resetar senha: {str(e)}"}

    def obter_metricas_usuarios(self, periodo: str = "diario") -> Dict[str, Any]:
        """
        Obtém métricas de usuários ativos por período
        """
        try:
            agora = datetime.utcnow()
            
            if periodo == "diario":
                data_inicio = agora - timedelta(days=1)
            elif periodo == "semanal":
                data_inicio = agora - timedelta(weeks=1)
            elif periodo == "mensal":
                data_inicio = agora - timedelta(days=30)
            else:
                data_inicio = agora - timedelta(days=1)

            # Usuários ativos no período
            usuarios_ativos = self.db.query(HistoricoLogin).filter(
                HistoricoLogin.data_login >= data_inicio
            ).distinct(HistoricoLogin.id_usuario).count()

            # Novos cadastros no período
            novos_usuarios = self.db.query(Usuario).filter(
                Usuario.data_cadastro >= data_inicio
            ).count()

            # Logins por dia (para gráfico)
            logins_por_dia = self._obter_logins_por_dia(data_inicio, agora)

            return {
                "usuarios_ativos": usuarios_ativos,
                "novos_usuarios": novos_usuarios,
                "logins_por_dia": logins_por_dia,
                "periodo": periodo
            }
        except Exception as e:
            return {
                "usuarios_ativos": 0,
                "novos_usuarios": 0,
                "logins_por_dia": [],
                "periodo": periodo
            }

    def _obter_logins_por_dia(self, data_inicio: datetime, data_fim: datetime) -> List[Dict[str, Any]]:
        """
        Obtém logins agrupados por dia para gráficos
        """
        try:
            # Esta é uma implementação simplificada
            # Em produção, usar funções de agregação do banco de dados
            logins = self.db.query(HistoricoLogin).filter(
                HistoricoLogin.data_login >= data_inicio,
                HistoricoLogin.data_login <= data_fim
            ).all()

            # Agrupar por dia (implementação básica)
            logins_por_dia = {}
            for login in logins:
                data = login.data_login.date()
                if data not in logins_por_dia:
                    logins_por_dia[data] = 0
                logins_por_dia[data] += 1

            return [{"data": str(data), "logins": count} for data, count in logins_por_dia.items()]
        except Exception as e:
            return []