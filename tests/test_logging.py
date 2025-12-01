"""Unit tests for the logging and notification system of Südwest-Energie website"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from datetime import datetime
from suedwestenergie.utils.logger import AdvancedLogger, LogLevel, LogEntry, log_errors
from suedwestenergie.utils.email_notification import EmailNotificationService
from suedwestenergie.utils.sms_notification import SMSNotificationService
from suedwestenergie.config.logging_config import LoggingConfig, DEFAULT_LOGGING_CONFIG


class TestLoggingConfig(unittest.TestCase):
    """Test logging configuration class"""
    
    def setUp(self):
        # Create a temporary environment
        self.temp_env = {
            'LOG_LEVEL': 'DEBUG',
            'EMAIL_USERNAME': 'test@example.com',
            'EMAIL_PASSWORD': 'testpass',
            'NOTIFICATION_EMAILS': 'admin@example.com,tech@example.com',
            'TWILIO_SID': 'test_sid',
            'TWILIO_TOKEN': 'test_token',
            'TWILIO_FROM_PHONE': '+1234567890',
            'NOTIFICATION_PHONES': '+1234567890,+1234567891',
        }
    
    def test_config_properties(self):
        """Test that configuration properties are correctly loaded"""
        config = LoggingConfig()
        
        # Test default values
        self.assertEqual(config.log_level, 'INFO')
        self.assertEqual(config.smtp_server, 'smtp.gmail.com')
        self.assertEqual(config.smtp_port, 587)
        
        # Test with custom config
        custom_config = LoggingConfig({
            'LOG_LEVEL': 'DEBUG',
            'SMTP_SERVER': 'smtp.test.com',
            'SMTP_PORT': 465,
            'EMAIL_USERNAME': 'test@test.com',
            'EMAIL_PASSWORD': 'password',
            'NOTIFICATION_EMAILS': ['admin@test.com'],
            'TWILIO_SID': 'test_sid',
            'TWILIO_TOKEN': 'test_token',
            'TWILIO_FROM_PHONE': '+1234567890',
            'NOTIFICATION_PHONES': ['+1234567890'],
        })
        
        self.assertEqual(custom_config.log_level, 'DEBUG')
        self.assertEqual(custom_config.smtp_server, 'smtp.test.com')
        self.assertEqual(custom_config.smtp_port, 465)
    
    def test_is_email_configured(self):
        """Test email configuration check"""
        config = LoggingConfig()
        
        # Test unconfigured
        self.assertFalse(config.is_email_configured())
        
        # Test with minimal configuration
        config.config['EMAIL_USERNAME'] = 'test@example.com'
        config.config['EMAIL_PASSWORD'] = 'password'
        config.config['NOTIFICATION_EMAILS'] = ['admin@example.com']
        self.assertTrue(config.is_email_configured())
    
    def test_is_sms_configured(self):
        """Test SMS configuration check"""
        config = LoggingConfig()
        
        # Test unconfigured
        self.assertFalse(config.is_sms_configured())
        
        # Test with minimal configuration
        config.config['TWILIO_SID'] = 'test_sid'
        config.config['TWILIO_TOKEN'] = 'test_token'
        config.config['TWILIO_FROM_PHONE'] = '+1234567890'
        config.config['NOTIFICATION_PHONES'] = ['+1234567890']
        self.assertTrue(config.is_sms_configured())


class TestAdvancedLogger(unittest.TestCase):
    """Test the advanced logger functionality"""
    
    def setUp(self):
        self.logger = AdvancedLogger(name="test_logger")
    
    def test_log_levels(self):
        """Test different log levels"""
        with patch.object(self.logger.logger, 'debug') as mock_debug, \
             patch.object(self.logger.logger, 'info') as mock_info, \
             patch.object(self.logger.logger, 'warning') as mock_warning, \
             patch.object(self.logger.logger, 'error') as mock_error, \
             patch.object(self.logger.logger, 'critical') as mock_critical:
            
            # Test each log level
            self.logger.debug("Debug message")
            mock_debug.assert_called_once()
            
            mock_debug.reset_mock()
            self.logger.info("Info message")
            mock_info.assert_called_once()
            
            mock_info.reset_mock()
            self.logger.warning("Warning message")
            mock_warning.assert_called_once()
            
            mock_warning.reset_mock()
            self.logger.error("Error message")
            mock_error.assert_called_once()
            
            mock_error.reset_mock()
            self.logger.critical("Critical message")
            mock_critical.assert_called_once()
    
    def test_log_with_context(self):
        """Test logging with context information"""
        test_context = {"user_id": 123, "session_id": "abc123"}
        
        with patch.object(self.logger.logger, 'error') as mock_error:
            self.logger.error("Error with context", context=test_context)
            mock_error.assert_called_once()
    
    def test_log_with_error_code(self):
        """Test logging with error code"""
        with patch.object(self.logger.logger, 'error') as mock_error:
            self.logger.error("Error with code", error_code="TEST_ERROR_001")
            mock_error.assert_called_once()
    
    def test_log_entry_creation(self):
        """Test log entry creation"""
        timestamp = datetime.now()
        entry = LogEntry(
            timestamp=timestamp,
            level=LogLevel.ERROR,
            message="Test error",
            context={"test": "value"},
            error_code="TEST_ERROR"
        )
        
        self.assertEqual(entry.timestamp, timestamp)
        self.assertEqual(entry.level, LogLevel.ERROR)
        self.assertEqual(entry.message, "Test error")
        self.assertEqual(entry.context, {"test": "value"})
        self.assertEqual(entry.error_code, "TEST_ERROR")


class TestEmailNotificationService(unittest.TestCase):
    """Test email notification service"""
    
    def setUp(self):
        # Temporarily set environment variables for testing
        os.environ['EMAIL_USERNAME'] = 'test@example.com'
        os.environ['EMAIL_PASSWORD'] = 'testpass'
        os.environ['NOTIFICATION_EMAILS'] = 'admin@example.com,tech@example.com'
        os.environ['FROM_EMAIL'] = 'noreply@example.com'
        
        self.email_service = EmailNotificationService()
    
    def tearDown(self):
        # Clean up environment variables
        del os.environ['EMAIL_USERNAME']
        del os.environ['EMAIL_PASSWORD']
        del os.environ['NOTIFICATION_EMAILS']
        del os.environ['FROM_EMAIL']
    
    def test_is_configured(self):
        """Test email service configuration check"""
        self.assertTrue(self.email_service.is_configured())
    
    def test_format_error_email(self):
        """Test email formatting"""
        error_msg = "Test error occurred"
        error_code = "TEST_ERROR_001"
        context = {"user": "test", "action": "login"}
        
        html_body = self.email_service._format_error_email(error_msg, error_code, context)
        
        # Check that important elements are in the email
        self.assertIn("CRITICAL ERROR ALERT", html_body)
        self.assertIn(error_msg, html_body)
        self.assertIn(error_code, html_body)
        self.assertIn("Südwest-Energie Website", html_body)
    
    @patch('smtplib.SMTP')
    def test_send_critical_error_notification(self, mock_smtp):
        """Test sending critical error notification"""
        # Mock the SMTP server
        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance
        mock_smtp.return_value.__exit__.return_value = None
        
        # Temporarily enable email configuration
        original_emails = os.environ.get('NOTIFICATION_EMAILS')
        os.environ['NOTIFICATION_EMAILS'] = 'admin@example.com'
        
        result = self.email_service.send_critical_error_notification(
            "Test Error", 
            "A test error occurred", 
            "TEST_ERROR_001",
            {"user": "test"}
        )
        
        self.assertTrue(result)
        # Clean up
        if original_emails:
            os.environ['NOTIFICATION_EMAILS'] = original_emails
        else:
            del os.environ['NOTIFICATION_EMAILS']


class TestSMSNotificationService(unittest.TestCase):
    """Test SMS notification service"""
    
    def setUp(self):
        # Temporarily set environment variables for testing
        os.environ['TWILIO_SID'] = 'test_sid'
        os.environ['TWILIO_TOKEN'] = 'test_token'
        os.environ['TWILIO_FROM_PHONE'] = '+1234567890'
        os.environ['NOTIFICATION_PHONES'] = '+1234567890'
        
        self.sms_service = SMSNotificationService()
    
    def tearDown(self):
        # Clean up environment variables if they exist
        keys_to_remove = ['TWILIO_SID', 'TWILIO_TOKEN', 'TWILIO_FROM_PHONE', 'NOTIFICATION_PHONES']
        for key in keys_to_remove:
            if key in os.environ:
                del os.environ[key]
    
    def test_format_error_sms(self):
        """Test SMS formatting"""
        error_title = "Test Error"
        error_msg = "A test error occurred"
        error_code = "TEST_ERROR_001"
        
        sms_body = self.sms_service._format_error_sms(error_title, error_msg, error_code)
        
        self.assertIn("SW-Energie", sms_body)
        self.assertIn(error_code, sms_body)
        self.assertIn("A test error occurred", sms_body)
        
        # Ensure it's within SMS character limit
        self.assertLess(len(sms_body), 160)


class TestLogErrorsDecorator(unittest.TestCase):
    """Test the log_errors decorator"""
    
    def test_log_errors_decorator_success(self):
        """Test decorator when function succeeds"""
        @log_errors("Test function error")
        def test_func():
            return "success"
        
        result = test_func()
        self.assertEqual(result, "success")
    
    def test_log_errors_decorator_exception(self):
        """Test decorator when function raises exception"""
        @log_errors("Test function error")
        def test_func():
            raise ValueError("Test error")
        
        with patch('suedwestenergie.utils.logger.logger') as mock_logger:
            with self.assertRaises(ValueError):
                test_func()
            
            # Check that error was logged
            mock_logger.error.assert_called()


if __name__ == '__main__':
    unittest.main()