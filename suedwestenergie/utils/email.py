"""Email utilities for production contact form"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from suedwestenergie.config import Config
from suedwestenergie.utils.logger import log_error, log_info


class EmailService:
    """Service class for sending emails"""
    
    @staticmethod
    def send_contact_form_email(name: str, email: str, phone: str, company: str, message: str) -> bool:
        """
        Send contact form submission via email
        
        Args:
            name: Name of the person submitting the form
            email: Email address of the person
            phone: Phone number of the person
            company: Company name
            message: Message content
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Check if email settings are configured
            if not Config.EMAIL_HOST or not Config.EMAIL_HOST_USER or not Config.EMAIL_HOST_PASSWORD:
                log_info("Email settings not configured, skipping email sending", "EmailService.send_contact_form_email")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_HOST_USER
            msg['To'] = Config.EMAIL
            msg['Subject'] = f"Neue Kontaktanfrage von {name} ({company})"
            
            # Email body
            body = f"""
            Neue Kontaktanfrage erhalten:
            
            Name: {name}
            E-Mail: {email}
            Telefon: {phone}
            Unternehmen: {company}
            Nachricht: {message}
            
            Diese Nachricht wurde über das Kontaktformular der Südwest-Energie Website gesendet.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) as server:
                server.starttls(context=context)
                server.login(Config.EMAIL_HOST_USER, Config.EMAIL_HOST_PASSWORD)
                server.sendmail(Config.EMAIL_HOST_USER, Config.EMAIL, msg.as_string())
            
            log_info(f"Contact form email sent successfully to {Config.EMAIL}", "EmailService.send_contact_form_email")
            return True
            
        except Exception as e:
            log_error(e, "EmailService.send_contact_form_email")
            return False


def send_contact_form_notification(name: str, email: str, phone: str, company: str, message: str) -> bool:
    """
    Send contact form notification using the EmailService
    
    Args:
        name: Name of the person submitting the form
        email: Email address of the person
        phone: Phone number of the person
        company: Company name
        message: Message content
        
    Returns:
        True if notification was sent successfully, False otherwise
    """
    return EmailService.send_contact_form_email(name, email, phone, company, message)