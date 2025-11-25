
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from passlib.context import CryptContext

from App.models.admin import Admin
from App.models.perfil import User
from App.models.cursos import AccessHistory

# Configuração do passlib para hashing seguro
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    """
    Service para operações administrativas:
    - Validação de login com senha criptografada.
    - Validação de PIN (também com hash).
    - Consultas de usuários e histórico.
    """

    def __init__(self, db: Session):
        self.db = db

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def _hash_password(self, plain: str) -> str:
        return pwd_context.hash(plain)

    def _verify_pin(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def _hash_pin(self, plain: str) -> str:
        return pwd_context.hash(plain)

    def validar_login(self, username: str, password: str) -> bool:
        """
        Valida username e senha do admin usando hash seguro.
        """
        try:
            admin: Optional[Admin] = self.db.execute(
                select(Admin).where(Admin.username == username)
            ).scalar_one_or_none()

            if not admin:
                return False

            return self._verify_password(password, admin.password)
        except SQLAlchemyError:
            return False

    def validar_pin(self, username: str, pin: str) -> bool:
        """
        Valida PIN do admin usando hash seguro.
        """
        try:
            admin: Optional[Admin] = self.db.execute(
                select(Admin).where(Admin.username == username)
            ).scalar_one_or_none()

            if not admin or not admin.pin:
                return False

            return self._verify_pin(pin, admin.pin)
        except SQLAlchemyError:
            return False

    def obter_nome_admin(self, username: str) -> Optional[str]:
        """
        Retorna o nome do administrador pelo username.
        """
        try:
            return self.db.execute(
                select(Admin.name).where(Admin.username == username)
            ).scalar_one_or_none()
        except SQLAlchemyError:
            return None


    def consultar_usuario_por_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            user: Optional[User] = self.db.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()

            if not user:
                return None

            return {"id": user.id, "name": user.name, "active": user.active}
        except SQLAlchemyError:
            return None

    def consultar_historico_acessos(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        try:
            page = max(1, page)
            page_size = min(page_size, 100)

            query = select(AccessHistory).order_by(AccessHistory.timestamp.desc())
            total = self.db.execute(select(func.count()).select_from(AccessHistory)).scalar_one()

            offset = (page - 1) * page_size
            historico = self.db.execute(query.offset(offset).limit(page_size)).scalars().all()

            items = [{"user_id": h.user_id, "timestamp": h.timestamp} for h in historico]

            return {
                "items": items,
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size,
            }
        except SQLAlchemyError:
            return {"items": [], "page": page, "page_size": page_size, "total": 0, "total_pages": 0}

    def consultar_usuarios_ativos(self) -> List[Dict[str, Any]]:
        try:
            ativos = self.db.execute(select(User).where(User.active.is_(True))).scalars().all()
            return [{"id": u.id, "name": u.name} for u in ativos]
        except SQLAlchemyError:
            return []


    def criar_admin(self, username: str, password: str, pin: str, name: str) -> bool:
        """
        Cria um novo admin com senha e PIN criptografados.
        """
        try:
            hashed_password = self._hash_password(password)
            hashed_pin = self._hash_pin(pin)

            novo_admin = Admin(username=username, password=hashed_password, pin=hashed_pin, name=name)
            self.db.add(novo_admin)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
