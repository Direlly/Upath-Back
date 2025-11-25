import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:Abi369nt45@localhost/upath_db")
    
    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "a9f8b7c6d5e378nk863jnu7n6o5p4q3r2s1t0")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "upath.contato@gmail.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "zzwv mecg ozpm gzqu")
    
    # AI Service
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://localhost:5001")
    
    class Config:
        env_file = ".env"

settings = Settings()