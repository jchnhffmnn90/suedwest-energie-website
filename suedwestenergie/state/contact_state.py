"""State Management für das Kontaktformular"""

import reflex as rx
import re
from typing import Optional
from datetime import datetime
from suedwestenergie.utils.logger import log_error, log_info
from suedwestenergie.utils.analytics import track_form_submission
from suedwestenergie.utils.email import send_contact_form_notification
from suedwestenergie.utils.ninox_client import save_contact_to_ninox


class ContactFormState(rx.State):
    """State für das Kontaktformular"""

    name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    message: str = ""
    form_submitted: bool = False
    error_message: str = ""

    @rx.var
    def is_valid_email(self) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None

    def validate_form(self) -> Optional[str]:
        """Validate form data"""
        if not self.name.strip():
            return "Bitte geben Sie Ihren Namen ein."
        if not self.email.strip():
            return "Bitte geben Sie Ihre E-Mail-Adresse ein."
        if not self.is_valid_email:
            return "Bitte geben Sie eine gültige E-Mail-Adresse ein."
        if not self.company.strip():
            return "Bitte geben Sie Ihr Unternehmen an."
        if len(self.message.strip()) < 10:
            return "Die Nachricht muss mindestens 10 Zeichen enthalten."
        return None

    async def submit_form(self):
        """Handle form submission with validation and error handling"""
        log_info("Contact form submission initiated", "ContactFormState.submit_form")

        validation_error = self.validate_form()
        if validation_error:
            self.error_message = validation_error
            log_info(f"Validation error: {validation_error}", "ContactFormState.submit_form")
            return

        try:
            # Reset any previous error messages
            self.error_message = ""

            # Log the form submission
            log_info(f"Form submitted by {self.name} ({self.email}) from {self.company}", "ContactFormState.submit_form")

            # Track form submission event
            track_form_submission("contact_form")

            # Prepare data for Ninox database
            form_data = {
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "company": self.company,
                "message": self.message,
                "submitted_at": datetime.now().isoformat()
            }

            # Save to Ninox database
            try:
                ninox_saved = save_contact_to_ninox(form_data)
                if ninox_saved:
                    log_info("Contact form data successfully saved to Ninox database", "ContactFormState.submit_form")
                else:
                    log_error("Failed to save contact form data to Ninox database", "ContactFormState.submit_form")
            except Exception as ninox_error:
                log_error(f"Error saving to Ninox database: {ninox_error}", "ContactFormState.submit_form")

            # Attempt to send notification email
            email_sent = send_contact_form_notification(
                self.name,
                self.email,
                self.phone,
                self.company,
                self.message
            )

            if not email_sent:
                log_info("Email notification not sent - check email configuration", "ContactFormState.submit_form")

            # Mark form as submitted and redirect
            self.form_submitted = True
            yield rx.redirect("/danke")

        except Exception as e:
            log_error(e, "ContactFormState.submit_form")
            self.error_message = "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."

    def reset_form(self):
        """Reset form fields"""
        self.name = ""
        self.email = ""
        self.phone = ""
        self.company = ""
        self.message = ""
        self.form_submitted = False
        self.error_message = ""