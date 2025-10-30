from sqlalchemy.orm import Session
from models.user import User
from core.security import get_password_hash, verify_password
from schemas.user import UserCreate
from datetime import datetime

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.senha)
        
        user = User(
            nome=user_data.nome,
            email=user_data.email,
            senha_hash=hashed_password
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.senha_hash):
            return None
        return user
    
    def update_last_login(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_login = datetime.utcnow()
            self.db.commit()