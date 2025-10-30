from sqlalchemy.orm import Session
from models.simulation import Simulation, SimulationResult
from models.course import CutoffScore
from schemas.simulation import SimulationCreate
from typing import List

class SimulationService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_simulation(self, user_id: int, simulation_data: SimulationCreate, media: float) -> Simulation:
        simulation = Simulation(
            user_id=user_id,
            ano_enem=simulation_data.ano_enem,
            nota_redacao=simulation_data.nota_redacao,
            nota_natureza=simulation_data.nota_natureza,
            nota_humanas=simulation_data.nota_humanas,
            nota_linguagens=simulation_data.nota_linguagens,
            nota_matematica=simulation_data.nota_matematica,
            estado=simulation_data.estado,
            modalidade=simulation_data.modalidade,
            media_usuario=media
        )
        
        self.db.add(simulation)
        self.db.commit()
        self.db.refresh(simulation)
        
        return simulation
    
    def find_compatible_courses(self, simulation_data: SimulationCreate, media: float) -> List[dict]:
        # Buscar cursos com notas de corte compatíveis
        cutoff_scores = self.db.query(CutoffScore).filter(
            CutoffScore.estado == simulation_data.estado,
            CutoffScore.modalidade == simulation_data.modalidade,
            CutoffScore.nota_corte <= media + 50  # Margem de 50 pontos
        ).all()
        
        results = []
        for cutoff in cutoff_scores:
            chance = self.calculate_admission_chance(media, cutoff.nota_corte)
            status = self.get_admission_status(media, cutoff.nota_corte)
            
            results.append({
                "nome_curso": cutoff.nome_curso,
                "instituicao": cutoff.instituicao,
                "nota_usuario": round(media, 1),
                "nota_corte": cutoff.nota_corte,
                "chance_ingresso": chance,
                "resultado": status
            })
        
        return results
    
    def calculate_admission_chance(self, user_score: float, cutoff_score: float) -> float:
        difference = user_score - cutoff_score
        if difference >= 50:
            return 95.0
        elif difference >= 20:
            return 80.0
        elif difference >= 0:
            return 60.0
        elif difference >= -20:
            return 30.0
        else:
            return 10.0
    
    def get_admission_status(self, user_score: float, cutoff_score: float) -> str:
        if user_score >= cutoff_score:
            return "Dentro da nota de corte"
        else:
            return "Abaixo da nota de corte"