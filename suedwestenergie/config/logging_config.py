"""Logging configuration for Südwest-Energie website"""

import os
from typing import Dict, List, Optional

# Default configuration values
DEFAULT_LOGGING_CONFIG = {
    # Logging settings
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "LOG_FILE": os.getenv("LOG_FILE", "suedwest_energie.log"),
    "MAX_LOG_SIZE": int(os.getenv("MAX_LOG_SIZE", "10485760")),  # 10MB
    "BACKUP_COUNT": int(os.getenv("BACKUP_COUNT", "5")),
    
    # Email notification settings
    "SMTP_SERVER": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "SMTP_PORT": int(os.getenv("SMTP_PORT", "587")),
    "EMAIL_USERNAME": os.getenv("EMAIL_USERNAME", ""),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD", ""),
    "FROM_EMAIL": os.getenv("FROM_EMAIL", "noreply@suedwestenergie.de"),
    "NOTIFICATION_EMAILS": os.getenv("NOTIFICATION_EMAILS", "").split(","),
    
    # SMS notification settings
    "TWILIO_SID": os.getenv("TWILIO_SID", ""),
    "TWILIO_TOKEN": os.getenv("TWILIO_TOKEN", ""),
    "TWILIO_FROM_PHONE": os.getenv("TWILIO_FROM_PHONE", ""),
    "NOTIFICATION_PHONES": os.getenv("NOTIFICATION_PHONES", "").split(","),
    
    # Error classification settings
    "CRITICAL_ERROR_CODES": os.getenv(
        "CRITICAL_ERROR_CODES", 
        "DB_ERROR,SMTP_ERROR,SYSTEM_ERROR,PERMISSION_ERROR"
    ).split(","),
    
    # Notification thresholds
    "NOTIFY_ON_ERROR_LEVEL": os.getenv("NOTIFY_ON_ERROR_LEVEL", "CRITICAL"),  # CRITICAL, ERROR, WARNING
    "NOTIFICATION_COOLDOWN_MINUTES": int(os.getenv("NOTIFICATION_COOLDOWN_MINUTES", "5")),
    
    # Log retention
    "RETENTION_DAYS": int(os.getenv("RETENTION_DAYS", "30")),
}

class LoggingConfig:
    """Configuration class for logging settings"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or DEFAULT_LOGGING_CONFIG.copy()
    
    @property
    def log_level(self) -> str:
        return self.config.get("LOG_LEVEL", "INFO")
    
    @property
    def log_file(self) -> str:
        return self.config.get("LOG_FILE", "suedwest_energie.log")
    
    @property
    def max_log_size(self) -> int:
        return self.config.get("MAX_LOG_SIZE", 10485760)
    
    @property
    def backup_count(self) -> int:
        return self.config.get("BACKUP_COUNT", 5)
    
    @property
    def smtp_server(self) -> str:
        return self.config.get("SMTP_SERVER", "smtp.gmail.com")
    
    @property
    def smtp_port(self) -> int:
        return self.config.get("SMTP_PORT", 587)
    
    @property
    def email_username(self) -> str:
        return self.config.get("EMAIL_USERNAME", "")
    
    @property
    def email_password(self) -> str:
        return self.config.get("EMAIL_PASSWORD", "")
    
    @property
    def from_email(self) -> str:
        return self.config.get("FROM_EMAIL", "noreply@suedwestenergie.de")
    
    @property
    def notification_emails(self) -> List[str]:
        emails = self.config.get("NOTIFICATION_EMAILS", [])
        return [email.strip() for email in emails if email.strip()]
    
    @property
    def twilio_sid(self) -> str:
        return self.config.get("TWILIO_SID", "")
    
    @property
    def twilio_token(self) -> str:
        return self.config.get("TWILIO_TOKEN", "")
    
    @property
    def twilio_from_phone(self) -> str:
        return self.config.get("TWILIO_FROM_PHONE", "")
    
    @property
    def notification_phones(self) -> List[str]:
        phones = self.config.get("NOTIFICATION_PHONES", [])
        return [phone.strip() for phone in phones if phone.strip()]
    
    @property
    def critical_error_codes(self) -> List[str]:
        codes = self.config.get("CRITICAL_ERROR_CODES", [])
        return [code.strip() for code in codes if code.strip()]
    
    @property
    def notify_on_error_level(self) -> str:
        return self.config.get("NOTIFY_ON_ERROR_LEVEL", "CRITICAL")
    
    @property
    def notification_cooldown_minutes(self) -> int:
        return self.config.get("NOTIFICATION_COOLDOWN_MINUTES", 5)
    
    @property
    def retention_days(self) -> int:
        return self.config.get("RETENTION_DAYS", 30)
    
    def is_email_configured(self) -> bool:
        """Check if email notifications are properly configured"""
        return (
            bool(self.email_username) and 
            bool(self.email_password) and 
            len(self.notification_emails) > 0
        )
    
    def is_sms_configured(self) -> bool:
        """Check if SMS notifications are properly configured"""
        return (
            bool(self.twilio_sid) and 
            bool(self.twilio_token) and 
            bool(self.twilio_from_phone) and 
            len(self.notification_phones) > 0
        )
    
    def is_notification_enabled(self) -> bool:
        """Check if any notification method is configured"""
        return self.is_email_configured() or self.is_sms_configured()


# Global config instance
logging_config = LoggingConfig()