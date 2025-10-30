import secrets
import string
from datetime import datetime, timedelta

def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)

def generate_pin_code() -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(4))

def calculate_media_enem(notas: list) -> float:
    return sum(notas) / len(notas) if notas else 0

def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def get_academic_year() -> int:
    current_year = datetime.now().year
    current_month = datetime.now().month
    return current_year if current_month >= 8 else current_year - 1