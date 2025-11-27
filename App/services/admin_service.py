from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

from models.admin import Admin, User, AccessHistory

# Configuração do passlib para hashing seguro
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    """
    Service para operações administrativas
    """

    def __init__(self, db: Session):
        self.db = db

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def obter_admin_por_username(self, username: str) -> Optional[Admin]:
        """
        Obtém admin pelo username
        """
        try:
            return self.db.query(Admin).filter(Admin.username == username).first()
        except SQLAlchemyError:
            return None

    def obter_admin_por_email(self, email: str) -> Optional[Admin]:
        """
        Obtém admin pelo email
        """
        try:
            return self.db.query(Admin).filter(Admin.email == email).first()
        except SQLAlchemyError:
            return None

    def validar_login(self, username: str, password: str) -> bool:
        """
        Valida username e senha do admin usando hash seguro.
        """
        try:
            admin = self.obter_admin_por_username(username)
            if not admin:
                return False

            return self._verify_password(password, admin.password) # type: ignore
        except SQLAlchemyError:
            return False

    def validar_pin(self, username: str, pin: str) -> bool:
        """
        Valida PIN do admin usando hash seguro.
        """
        try:
            admin = self.obter_admin_por_username(username)
            if not admin or not admin.pin: # type: ignore
                return False

            return self._verify_password(pin, admin.pin) # type: ignore
        except SQLAlchemyError:
            return False

    def obter_nome_admin(self, username: str) -> Optional[str]:
        """
        Retorna o nome do administrador pelo username.
        """
        try:
            admin = self.obter_admin_por_username(username)
            return admin.name if admin else None # type: ignore
        except SQLAlchemyError:
            return None

    def consultar_usuario_por_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None

            return {
                "id": user.id, 
                "name": user.name, 
                "email": user.email,
                "active": user.active
            }
        except SQLAlchemyError:
            return None

    def consultar_historico_acessos(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        try:
            page = max(1, page)
            page_size = min(page_size, 100)

            query = self.db.query(AccessHistory).order_by(AccessHistory.timestamp.desc())
            total = query.count()

            offset = (page - 1) * page_size
            historico = query.offset(offset).limit(page_size).all()

            items = [
                {
                    "id": h.id,
                    "user_id": h.user_id, 
                    "timestamp": h.timestamp,
                    "user_name": h.user.name if h.user else "N/A"
                } for h in historico
            ]

            return {
                "items": items,
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size,
            }
        except SQLAlchemyError as e:
            print(f"Erro ao consultar histórico: {e}")
            return {"items": [], "page": page, "page_size": page_size, "total": 0, "total_pages": 0}

    def consultar_usuarios_ativos(self) -> List[Dict[str, Any]]:
        try:
            ativos = self.db.query(User).filter(User.active == True).all()
            return [
                {
                    "id": u.id, 
                    "name": u.name, 
                    "email": u.email
                } for u in ativos
            ]
        except SQLAlchemyError as e:
            print(f"Erro ao consultar usuários ativos: {e}")
            return []

    def obter_estatisticas_sistema(self) -> Dict[str, Any]:
        """
        Obtém estatísticas do sistema
        """
        try:
            total_usuarios = self.db.query(User).count()
            usuarios_ativos = self.db.query(User).filter(User.active == True).count()
            total_acessos = self.db.query(AccessHistory).count()
            
            # Acessos hoje
            hoje = datetime.now().date()
            acessos_hoje = self.db.query(AccessHistory).filter(
                AccessHistory.timestamp >= hoje
            ).count()

            return {
                "total_usuarios": total_usuarios,
                "usuarios_ativos": usuarios_ativos,
                "total_acessos": total_acessos,
                "acessos_hoje": acessos_hoje
            }
        except SQLAlchemyError as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}