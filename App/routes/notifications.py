from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from schemas.notification import NotificationSettings
from services.notification_service import NotificationService

router = APIRouter()

@router.get("/")
async def get_notifications(
    filter: str = Query(None, description="Filtro por tipo"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notification_service = NotificationService(db)
    
    filters = {}
    if filter:
        filters['filter'] = filter
    
    notifications = notification_service.get_user_notifications(current_user["user_id"], filters)
    
    return {
        "success": True,
        "data": notifications
    }

@router.patch("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notification_service = NotificationService(db)
    success = notification_service.mark_notification_as_read(notification_id, current_user["user_id"])
    
    return {
        "success": True,
        "data": {
            "mensagem": "Notificação marcada como lida"
        }
    }

@router.get("/settings")
async def get_notification_settings(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    notification_service = NotificationService(db)
    settings = notification_service.get_notification_settings(current_user["user_id"])
    
    return {
        "success": True,
        "data": settings
    }

@router.put("/settings")
async def update_notification_settings(
    settings: list[NotificationSettings],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notification_service = NotificationService(db)
    success = notification_service.update_notification_settings(current_user["user_id"], settings)
    
    return {
        "success": True,
        "data": {
            "mensagem": "Configurações de notificação atualizadas"
        }
    }