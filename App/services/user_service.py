from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime
from models.auth import Usuario

class UserService:
    """
    Service para operações específicas de usuários estudantes
    """

    def __init__(self, db: Session):
        self.db = db

    def obter_dados_home(self, user_id: int) -> Dict[str, Any]:
        """
        Obtém dados para a tela home do estudante
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            return {
                "success": True,
                "data": {
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "opcoes": [
                        {
                            "titulo": "Teste Vocacional",
                            "descricao": "Descubra cursos que combinam com seu perfil",
                            "rota": "/teste",
                            "icone": "🎓"
                        },
                        {
                            "titulo": "Simulação ENEM",
                            "descricao": "Calcule suas chances no curso desejado",
                            "rota": "/simulacao",
                            "icone": "📊"
                        }
                    ]
                }
            }
        except Exception as e:
            return {"success": False, "mensagem": f"Erro ao obter dados: {str(e)}"}

    def obter_perfil_completo(self, user_id: int) -> Dict[str, Any]:
        """
        Obtém dados completos do perfil do usuário
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
            
            if not usuario:
                return {"success": False, "mensagem": "Usuário não encontrado"}

            # Obter último login
            from models.auth import HistoricoLogin
            ultimo_login = self.db.query(HistoricoLogin).filter(
                HistoricoLogin.id_usuario == user_id
            ).order_by(HistoricoLogin.data_login.desc()).first()

            return {
                "success": True,
                "data": {
                    "id": usuario.id_usuario,
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "data_cadastro": usuario.data_cadastro,
                    "ultimo_login": ultimo_login.data_login if ultimo_login else None,
                    "status": usuario.status_conta
                }
            }
        except Exception as e:
            return {"success": False, "mensagem": f"Erro ao obter perfil: {str(e)}"}