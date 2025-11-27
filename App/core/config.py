import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database - CORRIGIDO
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:Abi369nt45@localhost:3306/upath_db")
    
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
    
    # Password Requirements
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_NUMBER: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    
    # Admin PIN
    ADMIN_PIN_LENGTH: int = 4
    
    class Config:
        env_file = ".env"

settings = Settings()