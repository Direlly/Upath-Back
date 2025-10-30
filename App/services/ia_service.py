import requests
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from core.config import settings

class IAService:
    def __init__(self):
        self.vocational_model = None
        self.scholarship_model = None
        self.load_models()
    
    def load_models(self):
        try:
            # Carregar modelos treinados
            self.vocational_model = joblib.load('models/decision_tree.pkl')
            self.scholarship_model = joblib.load('models/random_forest.pkl')
        except:
            # Criar modelos dummy se não existirem
            self.vocational_model = DecisionTreeClassifier()
            self.scholarship_model = RandomForestClassifier()
    
    def predict_vocational_area(self, answers: list) -> dict:
        # Simular predição de área vocacional
        areas = ["Ciências Humanas", "Ciências Exatas", "Ciências Biológicas", "Linguagens e Artes"]
        
        # Lógica simples baseada nas respostas
        score_humanas = sum(1 for ans in answers if ans in ['1', '2'])  # Exemplo
        score_exatas = sum(1 for ans in answers if ans in ['3', '4'])   # Exemplo
        
        if score_exatas > score_humanas:
            area = "Ciências Exatas"
            cursos = ["Engenharia Civil", "Ciência da Computação", "Matemática", "Física"]
        else:
            area = "Ciências Humanas"
            cursos = ["Psicologia", "História", "Sociologia", "Jornalismo"]
        
        return {
            "area_predita": area,
            "confianca": 0.85,
            "cursos_sugeridos": cursos
        }
    
    def predict_scholarship_chance(self, user_data: dict) -> dict:
        # Simular predição de chances de bolsa
        notas = [
            user_data['nota_redacao'],
            user_data['nota_natureza'],
            user_data['nota_humanas'],
            user_data['nota_linguagens'],
            user_data['nota_matematica']
        ]
        media = sum(notas) / len(notas)
        
        if media >= 800:
            chance = 95.0
        elif media >= 700:
            chance = 75.0
        elif media >= 600:
            chance = 50.0
        else:
            chance = 25.0
        
        return {
            "chance_bolsa": chance,
            "media_usuario": media,
            "programas_recomendados": ["PROUNI", "FIES", "Bolsas Institucionais"]
        }
    
    def chat_response(self, message: str, context: dict = None) -> dict:
        # Simular chat com IA
        message_lower = message.lower()
        
        if "teste vocacional" in message_lower or "perfil" in message_lower:
            response = "Entendido! Vamos começar seu teste vocacional. Responda 8 perguntas para descobrir sua área ideal."
        elif "bolsa" in message_lower or "financiamento" in message_lower:
            response = "Posso ajudar com informações sobre bolsas! Para uma análise personalizada, faça uma simulação com suas notas do ENEM."
        else:
            response = "Olá! Sou seu assistente UPath. Posso ajudar com testes vocacionais, simulações de ingresso e informações sobre bolsas. Como posso ajudar?"
        
        return {
            "resposta": response,
            "contexto": context or {"sessao_id": "123"}
        }