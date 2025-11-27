from sqlalchemy.orm import Session
from typing import Optional
from models.auth import Usuario
from schemas.perfil_schemas import UserProfileUpdate, PasswordUpdate
from core.security import verify_password, get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_profile(self, user_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    
    def update_user_profile(self, user_id: int, profile_data: UserProfileUpdate) -> Optional[Usuario]:
        user = self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
        if not user:
            return None
        
        if profile_data.nome:
            user.nome = profile_data.nome # type: ignore
        if profile_data.foto_url:
            user.foto_url = profile_data.foto_url # type: ignore
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_password(self, user_id: int, password_data: PasswordUpdate) -> bool:
        user = self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
        if not user:
            return False
        
        # Usar setattr para evitar problemas de tipo com SQLAlchemy
        if not verify_password(password_data.current_password, str(user.senha_hash)):
            return False
        
        user.senha_hash = get_password_hash(password_data.new_password)  # type: ignore
        self.db.commit()
        return True
    
    def get_user_home_data(self, user_id: int) -> dict:
        user = self.get_user_profile(user_id)
        
        if not user:
            return {}
        
        # Cards de notícias (mock data - pode virar banco de dados depois)
        news_cards = [
            {
                "titulo": "Inscrições Abertas para o PROUNI",
                "descricao": "Prazo até 30/11 para inscrições no PROUNI 2024",
                "imagem": "https://example.com/prouni.jpg"
            },
            {
                "titulo": "Novas Bolsas em Tecnologia",
                "descricao": "Empresas oferecem 500 bolsas em cursos de TI",
                "imagem": "https://example.com/tech.jpg"
            }
        ]
        
        return {
            "nome": user.nome,
            "imagem": getattr(user, 'foto_url', None),
            "noticias": news_cards
        }