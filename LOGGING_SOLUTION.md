# Südwest-Energie Smart Logging Solution

## Overview

This document describes the smart logging solution implemented for the Südwest-Energie website. The solution provides comprehensive logging capabilities with automatic notifications for critical errors via email and SMS.

## Features

- **Multi-level logging**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Context-aware logging**: Include relevant context with each log entry
- **Error classification**: Automatic identification of critical errors
- **Email notifications**: Automatic email alerts for critical errors
- **SMS notifications**: SMS alerts for critical errors using Twilio
- **Configurable**: Environment-based configuration for flexibility
- **Asynchronous processing**: Non-blocking notification delivery
- **Thread-safe**: Safe to use in multi-threaded environments

## Architecture

The logging solution consists of the following components:

### Core Components
1. **AdvancedLogger**: Main logging class with notification capabilities
2. **EmailNotificationService**: Handles email delivery for critical errors
3. **SMSNotificationService**: Handles SMS delivery for critical errors
4. **LoggingConfig**: Configuration management for all settings

### File Structure
```
suedwestenergie/
├── config/
│   ├── logging_config.py    # Configuration management
├── utils/
│   ├── logger.py           # Main logger implementation
│   ├── email_notification.py # Email notification service
│   └── sms_notification.py   # SMS notification service
└── tests/
    └── test_logging.py     # Unit tests
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
# Add these to your requirements.txt if not already present:
# twilio>=8.0.0  # For SMS notifications
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and customize the values:

```bash
cp .env.example .env
```

Then edit `.env` with your specific configuration values.

### 3. Environment Variables

#### Logging Configuration
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE`: Path to the log file
- `MAX_LOG_SIZE`: Maximum size of log file in bytes
- `BACKUP_COUNT`: Number of backup log files to keep
- `RETENTION_DAYS`: Number of days to retain logs

#### Email Configuration
- `SMTP_SERVER`: SMTP server address (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (default: 587)
- `EMAIL_USERNAME`: SMTP username
- `EMAIL_PASSWORD`: SMTP password or app password
- `FROM_EMAIL`: Sender email address
- `NOTIFICATION_EMAILS`: Comma-separated list of recipient emails

#### SMS Configuration (Twilio)
- `TWILIO_SID`: Twilio Account SID
- `TWILIO_TOKEN`: Twilio Auth Token
- `TWILIO_FROM_PHONE`: Twilio phone number
- `NOTIFICATION_PHONES`: Comma-separated list of recipient phone numbers

#### Error Classification
- `CRITICAL_ERROR_CODES`: Comma-separated list of critical error codes
- `NOTIFY_ON_ERROR_LEVEL`: Minimum error level to trigger notifications
- `NOTIFICATION_COOLDOWN_MINUTES`: Minimum time between notifications

## Usage

### Basic Logging

```python
from suedwestenergie.utils.logger import logger, debug, info, warning, error, critical

# Direct method calls
logger.info("User logged in successfully", context={"user_id": 123})
logger.error("Database connection failed", error_code="DB_ERROR_001")

# Convenience functions
info("Application started")
error("Invalid user input", context={"user_id": 456, "input": ""})
critical("System failure", context={"server": "web-01"}, error_code="SYSTEM_ERROR_001")
```

### Logging with Context

Context provides additional information that's helpful for debugging:

```python
logger.error(
    "Payment processing failed",
    context={
        "user_id": 123,
        "transaction_id": "txn_123456",
        "amount": 150.00,
        "currency": "EUR",
        "payment_method": "credit_card"
    },
    error_code="PAYMENT_ERROR_001"
)
```

### Using the Error Logging Decorator

The `log_errors` decorator automatically logs exceptions from functions:

```python
from suedwestenergie.utils.logger import log_errors

@log_errors("Contact form submission failed", level=logger.LogLevel.ERROR)
async def submit_contact_form(name, email, message):
    # Your implementation here
    pass
```

### Integration with Reflex State Handlers

Example integration with the existing contact form state:

```python
import reflex as rx
from suedwestenergie.utils.logger import logger, log_errors

class ContactFormState(rx.State):
    # ... existing code ...

    @log_errors("Contact form processing failed", level=logger.LogLevel.ERROR)
    async def submit_form(self):
        """Handle form submission with automatic error logging"""
        try:
            # Reset any previous error messages
            self.error_message = ""

            # Your contact form processing code here
            # e.g., sending email, saving to database, etc.
            print(f"Form submitted: {self.name}, {self.email}, {self.company}, {self.message}")

            # Log successful submission
            logger.info(
                "Contact form submitted successfully",
                context={
                    "user_email": self.email,
                    "company": self.company,
                    "message_length": len(self.message)
                }
            )

            # Mark form as submitted and redirect
            self.form_submitted = True
            return rx.redirect("/danke")

        except Exception as e:
            # This error will be automatically logged by the decorator
            logger.error(f"Contact form processing failed: {str(e)}", error_code="FORM_ERROR_001")
            self.error_message = "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."
            raise
```

## Notification Mechanism

### Critical Error Detection

The system automatically detects critical errors based on:

1. Log level (CRITICAL level logs always trigger notifications)
2. Error codes matching the `CRITICAL_ERROR_CODES` configuration
3. Certain error patterns in messages

### Email Notifications

When a critical error is detected, an HTML email is sent to all configured recipients with:

- Clear subject line indicating the error
- Error message and code
- Timestamp of the error
- Full context information in a readable format
- Responsive design for mobile viewing

### SMS Notifications

For time-sensitive critical errors, SMS messages are sent to configured phone numbers with:

- Concise error information
- Error code for quick identification
- Optimized message length for SMS (max 160 characters)

## Testing

Run the unit tests to verify the logging system:

```bash
python -m pytest tests/test_logging.py
```

## Best Practices

1. **Use appropriate log levels**: 
   - DEBUG: Detailed information for diagnostic purposes
   - INFO: General information about application flow
   - WARNING: Something unexpected happened but application continues
   - ERROR: A function failed to perform
   - CRITICAL: Application may not be able to continue

2. **Include useful context**: Always add relevant context information that can help with debugging

3. **Use error codes consistently**: Define and use consistent error codes across your application

4. **Monitor notification volume**: Set up notification cooldowns to avoid alert fatigue

5. **Secure credentials**: Never hardcode credentials, always use environment variables

## Monitoring and Maintenance

- Regularly review logs for patterns and recurring issues
- Monitor notification effectiveness and adjust thresholds as needed
- Rotate credentials periodically
- Maintain the list of critical error codes based on actual incidents