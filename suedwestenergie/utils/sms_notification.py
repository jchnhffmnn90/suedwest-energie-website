"""SMS notification system for critical errors in Südwest-Energie website"""

import os
from typing import List, Dict, Optional
import logging

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("Twilio library not available. Install with: pip install twilio")


class SMSNotificationService:
    """Service class for sending SMS notifications for critical errors"""
    
    def __init__(self):
        if TWILIO_AVAILABLE:
            self.twilio_sid = os.getenv("TWILIO_SID")
            self.twilio_token = os.getenv("TWILIO_TOKEN")
            self.from_phone = os.getenv("TWILIO_FROM_PHONE", "+1234567890")
            self.notification_phones = os.getenv("NOTIFICATION_PHONES", "").split(",")
            
            # Setup logger
            self.logger = logging.getLogger(__name__)
        else:
            self.twilio_sid = None
            self.twilio_token = None
            self.from_phone = None
            self.notification_phones = []
            self.logger = logging.getLogger(__name__)
            self.logger.warning("Twilio library not available - SMS notifications disabled")
    
    def is_configured(self) -> bool:
        """Check if SMS service is properly configured"""
        if not TWILIO_AVAILABLE:
            return False
            
        return bool(
            self.twilio_sid and 
            self.twilio_token and 
            self.from_phone and
            self.notification_phones and 
            any(phone.strip() for phone in self.notification_phones)
        )
    
    def send_critical_error_notification(
        self, 
        error_title: str, 
        error_message: str, 
        error_code: Optional[str] = None
    ) -> bool:
        """Send critical error notification via SMS"""
        if not self.is_configured():
            self.logger.warning("SMS notification service not configured or Twilio not available")
            return False
        
        # Format the SMS message
        message_body = self._format_error_sms(error_title, error_message, error_code)
        
        success_count = 0
        for phone in self.notification_phones:
            phone = phone.strip()
            if not phone:
                continue
                
            try:
                client = Client(self.twilio_sid, self.twilio_token)
                
                message = client.messages.create(
                    body=message_body,
                    from_=self.from_phone,
                    to=phone
                )
                
                self.logger.info(f"Critical error SMS sent to {phone}. SID: {message.sid}")
                success_count += 1
                
            except Exception as e:
                self.logger.error(f"Failed to send SMS to {phone}: {str(e)}")
                return False
        
        return success_count > 0
    
    def _format_error_sms(self, error_title: str, error_message: str, error_code: Optional[str]) -> str:
        """Format error message for SMS (limited to 160 characters)"""
        # Create a concise message for SMS
        if error_code:
            header = f"[CRITICAL] SW-Energie: {error_code}"
        else:
            header = f"[CRITICAL] SW-Energie: Error"
        
        # Limit the message to fit in an SMS
        remaining_chars = 160 - len(header) - 10  # 10 for " - " and some buffer
        truncated_message = error_message[:remaining_chars]
        
        return f"{header} - {truncated_message}"


# Singleton instance
sms_service = SMSNotificationService()