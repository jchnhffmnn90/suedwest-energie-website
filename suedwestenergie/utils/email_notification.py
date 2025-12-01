"""Email notification system for critical errors in Südwest-Energie website"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import json
from datetime import datetime
import logging


class EmailNotificationService:
    """Service class for sending email notifications for critical errors"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_username = os.getenv("EMAIL_USERNAME")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@suedwestenergie.de")
        self.notification_emails = os.getenv("NOTIFICATION_EMAILS", "").split(",")
        
        # Setup logger
        self.logger = logging.getLogger(__name__)
    
    def is_configured(self) -> bool:
        """Check if email service is properly configured"""
        return bool(
            self.email_username and 
            self.email_password and 
            self.notification_emails and 
            any(email.strip() for email in self.notification_emails)
        )
    
    def send_critical_error_notification(
        self, 
        error_title: str, 
        error_message: str, 
        error_code: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> bool:
        """Send critical error notification via email"""
        if not self.is_configured():
            self.logger.warning("Email notification service not configured")
            return False
        
        subject = f"[CRITICAL ERROR] Südwest-Energie - {error_title}"
        body = self._format_error_email(error_message, error_code, context)
        
        success_count = 0
        for recipient in self.notification_emails:
            recipient = recipient.strip()
            if not recipient:
                continue
                
            try:
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = recipient
                msg['Subject'] = subject
                
                msg.attach(MIMEText(body, 'html'))
                
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email_username, self.email_password)
                
                text = msg.as_string()
                server.sendmail(self.from_email, recipient, text)
                server.quit()
                
                self.logger.info(f"Critcal error email sent to {recipient}")
                success_count += 1
                
            except Exception as e:
                self.logger.error(f"Failed to send email to {recipient}: {str(e)}")
                return False
        
        return success_count > 0
    
    def _format_error_email(self, error_message: str, error_code: Optional[str], context: Optional[Dict]) -> str:
        """Format error message for email"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background-color: #f5f5f5; 
                }}
                .container {{ 
                    max-width: 600px; 
                    margin: 0 auto; 
                    background-color: white; 
                    border-radius: 8px; 
                    overflow: hidden; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                }}
                .header {{ 
                    background-color: #d32f2f; 
                    color: white; 
                    padding: 20px; 
                    text-align: center; 
                }}
                .header h1 {{ 
                    margin: 0; 
                    font-size: 24px; 
                }}
                .content {{ 
                    padding: 30px; 
                }}
                .info-section {{ 
                    margin-bottom: 20px; 
                    padding-bottom: 15px; 
                    border-bottom: 1px solid #eee; 
                }}
                .info-label {{ 
                    font-weight: bold; 
                    color: #555; 
                    margin-bottom: 5px; 
                }}
                .info-value {{ 
                    margin-left: 10px; 
                    color: #333; 
                }}
                .error-message {{ 
                    background-color: #ffebee; 
                    padding: 15px; 
                    border-radius: 4px; 
                    border-left: 4px solid #d32f2f; 
                    margin: 15px 0; 
                }}
                .context {{ 
                    background-color: #f9f9f9; 
                    padding: 15px; 
                    border-radius: 4px; 
                    font-family: monospace; 
                    font-size: 14px; 
                    overflow-x: auto; 
                }}
                .footer {{ 
                    background-color: #f5f5f5; 
                    padding: 15px; 
                    text-align: center; 
                    color: #666; 
                    font-size: 12px; 
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 CRITICAL ERROR ALERT</h1>
                </div>
                <div class="content">
                    <div class="info-section">
                        <div class="info-label">Timestamp:</div>
                        <div class="info-value">{timestamp}</div>
                    </div>
                    <div class="info-section">
                        <div class="info-label">Error Code:</div>
                        <div class="info-value">{error_code or 'N/A'}</div>
                    </div>
                    <div class="info-section">
                        <div class="info-label">System:</div>
                        <div class="info-value">Südwest-Energie Website</div>
                    </div>
                    
                    <div class="error-message">
                        <h3>🚨 Error Message</h3>
                        <p>{error_message}</p>
                    </div>
                    
                    {f'<div class="context"><h3>📚 Context</h3><pre>{json.dumps(context, indent=2, default=str)}</pre></div>' if context else ''}
                    
                    <div class="footer">
                        This is an automated message from the Südwest-Energie monitoring system.<br>
                      </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html_body


# Singleton instance
email_service = EmailNotificationService()