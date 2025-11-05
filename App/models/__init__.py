"""
Módulo de modelos de dados (SQLAlchemy).
"""

from models.auth import Usuario, Perfil
from App.models.teste import TesteVocacional, Pergunta, Resposta
from App.models.simulacao import Simulacao, SimulacaoCurso
from App.models.curso import Curso, AreaConhecimento, NotaCorte
from App.models.notificacao import Notificacao, Relatorio

__all__ = [
    
    # Auth models
    "Usuario",
    "Perfil", 
    
    # Teste models
    "TesteVocacional",
    "Pergunta",
    "Resposta", 
    
    # Simulacao models
    "Simulacao",
    "SimulacaoCurso",
    
    # Curso models
    "Curso",
    "AreaConhecimento", 
    "NotaCorte",
    
    # Notificacao models
    "Notificacao",
    "Relatorio"
]