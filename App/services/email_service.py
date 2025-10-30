import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
    
    # Rota para enviar email de redefinição de senha
    def send_password_reset_email(self, to_email: str, reset_token: str) -> bool:
        try:
            subject = "Redefinição de Senha - UPath"
            body = f"""
            Olá,
            
            Você solicitou a redefinição de sua senha no UPath.
            Clique no link abaixo para criar uma nova senha:
            
            http://localhost:3000/reset-password?token={reset_token}
            
            Este link expira em 1 hora.
            
            Se você não solicitou esta redefinição, ignore este email.
            
            Atenciosamente,
            Equipe UPath
            """
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    # Rota para enviar email com PIN 2FA para admin
    def send_admin_2fa_email(self, to_email: str, pin_code: str) -> bool:
        try:
            subject = "Código de Verificação - UPath Admin"
            body = f"""
            Seu código de verificação para acesso administrativo é:
            
            {pin_code}
            
            Este código expira em 10 minutos.
            
            Não compartilhe este código com ninguém.
            """
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    # Função genérica para envio de email
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.smtp_username, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Erro SMTP: {e}")
            return False