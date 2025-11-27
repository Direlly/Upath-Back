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
    
    def send_password_reset_email(self, to_email: str, reset_token: str) -> bool:
        try:
            subject = "Redefinição de Senha - UPath"
            reset_url = f"http://localhost:5173/reset-password?token={reset_token}"
            
            body = f"""
            Olá,
            
            Você solicitou a redefinição de sua senha no UPath.
            Clique no link abaixo para criar uma nova senha:
            
            {reset_url}
            
            Este link expira em 1 hora.
            
            Se você não solicitou esta redefinição, ignore este email.
            
            Atenciosamente,
            Equipe UPath
            """
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Erro ao enviar email de recuperação: {e}")
            return False
    
    def send_admin_pin_email(self, to_email: str, pin_code: str) -> bool:
        try:
            subject = "Código de Verificação - UPath Admin"
            body = f"""
            Prezado Administrador,
            
            Seu código de verificação para acesso administrativo é:
            
            {pin_code}
            
            Este código expira em 10 minutos.
            
            Não compartilhe este código com ninguém.
            
            Atenciosamente,
            Sistema UPath
            """
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Erro ao enviar email de PIN: {e}")
            return False
    
    def send_account_locked_email(self, to_email: str, admin_name: str) -> bool:
        """
        Envia email quando conta é bloqueada por administrador
        """
        try:
            subject = "Conta Bloqueada - UPath"
            body = f"""
            Prezado usuário,
            
            Sua conta no UPath foi bloqueada por um administrador.
            
            Se você acredita que isso foi um erro, entre em contato com o suporte.
            
            Atenciosamente,
            Equipe UPath
            """
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Erro ao enviar email de conta bloqueada: {e}")
            return False
    
    def send_account_deleted_email(self, to_email: str) -> bool:
        """
        Envia email quando conta é excluída por administrador
        """
        try:
            subject = "Conta Excluída - UPath"
            body = f"""
            Prezado usuário,
            
            Sua conta no UPath foi excluída por um administrador.
            
            Se você acredita que isso foi um erro, entre em contato com o suporte.
            
            Atenciosamente,
            Equipe UPath
            """
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Erro ao enviar email de conta excluída: {e}")
            return False

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
            
            print(f"✅ Email enviado para: {to_email}")
            return True
        except Exception as e:
            print(f"Erro SMTP: {e}")
            return False