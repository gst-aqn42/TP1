import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.email_user = os.environ.get('EMAIL_USER', '')
        self.email_password = os.environ.get('EMAIL_PASSWORD', '')
    
    def enviar_notificacao(self, destinatario, nome_autor, artigo):
        """Envia notificação por email sobre novo artigo"""
        try:
            # Configurar mensagem
            subject = f"Novo artigo publicado de {nome_autor}"
            body = f"""
            Olá!

            Um novo artigo foi publicado com o nome do autor {nome_autor}:

            Título: {artigo['titulo']}
            Autores: {', '.join([autor['nome'] for autor in artigo['autores']])}
            Resumo: {artigo.get('resumo', 'Sem resumo')}

            Acesse nossa plataforma para ver o artigo completo.

            Atenciosamente,
            Equipe SimpleLib
            """
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = destinatario
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Enviar email (em produção, configurar credenciais reais)
            print(f"Simulando envio de email para: {destinatario}")
            print(f"Assunto: {subject}")
            print(f"Conteúdo: {body}")
            
            # Em ambiente real, descomente:
            # with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            #     server.starttls()
            #     server.login(self.email_user, self.email_password)
            #     server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            return False

# Instância global
email_service = EmailService()

def enviar_email_confirmacao_inscricao(email):
    """Envia email de confirmação de inscrição"""
    try:
        subject = "Confirmação de Inscrição - SimpleLib"
        body = f"""
        Olá!

        Obrigado por se inscrever para receber notificações da SimpleLib!

        Você receberá notificações por email sempre que novos artigos forem publicados.

        Se você não solicitou esta inscrição, pode ignorar este email.

        Atenciosamente,
        Equipe SimpleLib
        """
        
        print(f"📧 Simulando envio de email de confirmação para: {email}")
        print(f"Assunto: {subject}")
        print(f"Conteúdo: {body}")
        
        # Em ambiente real, enviar email de verdade:
        # msg = MIMEMultipart()
        # msg['From'] = email_service.email_user
        # msg['To'] = email
        # msg['Subject'] = subject
        # msg.attach(MIMEText(body, 'plain'))
        # 
        # with smtplib.SMTP(email_service.smtp_server, email_service.smtp_port) as server:
        #     server.starttls()
        #     server.login(email_service.email_user, email_service.email_password)
        #     server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email de confirmação: {e}")
        return False
