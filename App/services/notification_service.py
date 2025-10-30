from sqlalchemy.orm import Session
from models.notification import Notification
from models.user import UserNotificationSettings
from schemas.notification import NotificationSettings
from typing import List

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_notifications(self, user_id: int, filters: dict = None) -> List[Notification]:
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if filters and filters.get('filter'):
            filter_type = filters['filter']
            query = query.filter(Notification.tipo == filter_type)
        
        return query.order_by(Notification.data_envio.desc()).all()
    
    def mark_notification_as_read(self, notification_id: int, user_id: int) -> bool:
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.lido = True
            notification.status = "lido"
            self.db.commit()
            return True
        return False
    
    def create_notification(self, user_id: int, notification_data: dict) -> Notification:
        notification = Notification(
            user_id=user_id,
            titulo=notification_data.get('titulo'),
            tipo=notification_data.get('tipo'),
            mensagem=notification_data.get('mensagem')
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def get_notification_settings(self, user_id: int) -> List[UserNotificationSettings]:
        return self.db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).all()
    
    def update_notification_settings(self, user_id: int, settings: List[NotificationSettings]) -> bool:
        # Remove configurações existentes
        self.db.query(UserNotificationSettings).filter(
            UserNotificationSettings.user_id == user_id
        ).delete()
        
        # Adiciona novas configurações
        for setting in settings:
            new_setting = UserNotificationSettings(
                user_id=user_id,
                notification_type=setting.notification_type,
                enabled=setting.enabled
            )
            self.db.add(new_setting)
        
        self.db.commit()
        return True
    
    def get_unread_count(self, user_id: int) -> int:
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.lido == False
        ).count()