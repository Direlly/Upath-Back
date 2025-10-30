from sqlalchemy.orm import Session
from models.auth import AuditLog
from typing import Optional, Dict, Any
import json

class AuditService:
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(
        self, 
        acao: str, 
        alvo: str, 
        admin_email: Optional[str] = None,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        detalhes: Optional[Dict[str, Any]] = None,
        status: str = "sucesso"
    ) -> AuditLog:
        
        detalhes_json = json.dumps(detalhes) if detalhes else None
        
        audit_log = AuditLog(
            acao=acao,
            alvo=alvo,
            admin_email=admin_email,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            detalhes=detalhes_json,
            status=status
        )
        
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log
    
    def get_audit_logs(
        self, 
        admin_email: Optional[str] = None,
        user_id: Optional[int] = None,
        acao: Optional[str] = None,
        limit: int = 100
    ) -> list:
        query = self.db.query(AuditLog)
        
        if admin_email:
            query = query.filter(AuditLog.admin_email == admin_email)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if acao:
            query = query.filter(AuditLog.acao == acao)
        
        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()