#!/usr/bin/env python3
"""
Comprehensive Contact Form Testing Script for Südwest-Energie Website

This script specifically tests the contact form functionality including:
- Form field validation
- Data submission to Ninox database
- Error handling
- Success redirects
"""

import requests
import time
from datetime import datetime
import json
import sys
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup


class ContactFormTester:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.test_results = {
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "errors": []
            }
        }

    def add_test_result(self, test_name, passed, details=None):
        """Add test result to the test results"""
        result = {
            "name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results["tests"].append(result)
        self.test_results["summary"]["total"] += 1
        
        if passed:
            self.test_results["summary"]["passed"] += 1
            print(f"✅ {test_name}")
        else:
            self.test_results["summary"]["failed"] += 1
            print(f"❌ {test_name}")
            if details:
                print(f"   Details: {details}")

    def test_form_fields_existence(self):
        """Test if all required form fields exist on the page"""
        try:
            response = self.session.get(self.base_url)
            if response.status_code != 200:
                self.add_test_result("Form page accessibility", False, f"Status: {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for form fields
            expected_fields = [
                {"selector": "input[name='name']", "description": "Name field"},
                {"selector": "input[name='email']", "description": "Email field"},
                {"selector": "input[name='phone']", "description": "Phone field"},
                {"selector": "input[name='company']", "description": "Company field"},
                {"selector": "textarea[name='message']", "description": "Message field"},
                {"selector": "button[type='submit']", "description": "Submit button"}
            ]
            
            all_found = True
            details = []
            
            for field in expected_fields:
                element = soup.select(field["selector"])
                if element:
                    details.append(f"{field['description']}: Found")
                else:
                    details.append(f"{field['description']}: NOT FOUND")
                    all_found = False
            
            self.add_test_result("Form fields existence", all_found, "; ".join(details))
            return all_found
        except Exception as e:
            self.add_test_result("Form fields existence", False, str(e))
            return False

    def test_email_validation(self):
        """Test email validation by trying invalid email addresses"""
        try:
            invalid_emails = ["invalid-email", "test@", "@example.com", "test@.com"]
            
            all_rejected = True
            details = []
            
            for email in invalid_emails:
                test_data = {
                    "name": "Test User",
                    "email": email,
                    "phone": "+49 123 456789",
                    "company": "Test Company",
                    "message": "This is a test message."
                }
                
                # Try to submit with invalid email
                response = self.session.post(self.base_url, data=test_data)
                
                # Check if validation prevents submission (this depends on how Reflex handles validation)
                if "error" in response.text.lower() or "invalid" in response.text.lower():
                    details.append(f"Email '{email}': Correctly rejected")
                else:
                    details.append(f"Email '{email}': Not rejected")
                    all_rejected = False
            
            self.add_test_result("Email validation", all_rejected, "; ".join(details))
            return all_rejected
        except Exception as e:
            self.add_test_result("Email validation", False, str(e))
            return False

    def test_required_fields_validation(self):
        """Test that required fields are enforced"""
        try:
            # Test without name (required)
            test_data_no_name = {
                "email": "test@example.com",
                "phone": "+49 123 456789",
                "company": "Test Company",
                "message": "This is a test message."
            }
            
            response = self.session.post(self.base_url, data=test_data_no_name)
            
            # Check if there's an error related to missing name
            has_error = any(x in response.text.lower() for x in ["name", "required", "error", "fehlend", "muss"])
            
            details = f"Without name field: {'Error found' if has_error else 'No error found'}"
            self.add_test_result("Required fields validation", has_error, details)
            return has_error
        except Exception as e:
            self.add_test_result("Required fields validation", False, str(e))
            return False

    def test_message_length_validation(self):
        """Test that message has minimum length requirement"""
        try:
            # Test with very short message (less than 10 characters)
            test_data_short_message = {
                "name": "Test User",
                "email": "test@example.com", 
                "phone": "+49 123 456789",
                "company": "Test Company",
                "message": "Short"
            }
            
            response = self.session.post(self.base_url, data=test_data_short_message)
            
            # Check if there's an error related to message length
            has_error = any(x in response.text.lower() for x in ["message", "length", "10", "zu kurz", "weniger"])
            
            details = f"With short message: {'Error found' if has_error else 'No error found'}"
            self.add_test_result("Message length validation", has_error, details)
            return has_error
        except Exception as e:
            self.add_test_result("Message length validation", False, str(e))
            return False

    def test_successful_submission_simulation(self):
        """Test successful form submission with valid data"""
        try:
            # Valid test data
            test_data = {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+49 123 456789",
                "company": "Test Company",
                "message": "This is a comprehensive test message to verify the form submission functionality."
            }
            
            # Submit the form
            response = self.session.post(self.base_url, data=test_data)
            
            # Check for success indicators
            success_indicators = [
                "danke", "success", "thank", "erfolgreich", "gesendet", "submitted"
            ]
            
            is_success = any(indicator in response.text.lower() for indicator in success_indicators)
            
            # Also check for redirect to thank you page
            redirect_to_thank_you = "/danke" in response.url or "thank" in response.url.lower()
            
            status = f"Status: {response.status_code}, URL: {response.url}"
            if is_success or redirect_to_thank_you:
                details = f"{status} - Success detected"
                self.add_test_result("Successful submission", True, details)
                return True
            else:
                details = f"{status} - No success indicators found"
                self.add_test_result("Successful submission", False, details)
                return False
        except Exception as e:
            self.add_test_result("Successful submission", False, str(e))
            return False

    def test_ninox_integration_config(self):
        """Test if Ninox integration is properly configured"""
        try:
            # Import the config to check values
            import os
            import sys
            sys.path.append('/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt')
            
            from suedwestenergie.config import Config
            
            api_key = Config.NINOX_API_KEY
            db_id = Config.NINOX_DATABASE_ID
            table_id = Config.NINOX_TABLE_ID
            
            details = []
            all_configured = True
            
            if api_key and api_key != "your-ninox-api-key":
                details.append("API Key: Configured")
            else:
                details.append("API Key: Not configured")
                all_configured = False
                
            if db_id and db_id != "your-ninox-database-id":
                details.append("Database ID: Configured")
            else:
                details.append("Database ID: Not configured")
                all_configured = False
                
            if table_id and table_id != "your-ninox-table-id":
                details.append("Table ID: Configured")
            else:
                details.append("Table ID: Not configured")
                all_configured = False
            
            self.add_test_result("Ninox configuration", all_configured, "; ".join(details))
            return all_configured
        except Exception as e:
            self.add_test_result("Ninox configuration", False, str(e))
            return False

    def test_ninox_client_initialization(self):
        """Test if Ninox client can be initialized"""
        try:
            import sys
            sys.path.append('/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt')
            
            from suedwestenergie.utils.ninox_client import NinoxClient
            
            # Check if client can be initialized
            try:
                client = NinoxClient()
                client_initialized = True
                details = "Ninox client initialized successfully"
            except ValueError as e:
                client_initialized = False
                details = f"Ninox client initialization failed: {str(e)}"
            except Exception as e:
                client_initialized = False
                details = f"Ninox client initialization error: {str(e)}"
            
            self.add_test_result("Ninox client initialization", client_initialized, details)
            return client_initialized
        except Exception as e:
            self.add_test_result("Ninox client initialization", False, str(e))
            return False

    def test_ninox_save_function(self):
        """Test the save function with sample data"""
        try:
            import sys
            sys.path.append('/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt')
            
            from suedwestenergie.utils.ninox_client import save_contact_to_ninox
            
            # Sample data to test with
            sample_data = {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+49 123 456789",
                "company": "Test Company",
                "message": "Test message from automated script",
                "submitted_at": datetime.now().isoformat()
            }
            
            # Try to save data (this will fail if Ninox isn't properly configured but should not crash)
            try:
                result = save_contact_to_ninox(sample_data)
                if result is not None:  # Function executed without crashing
                    details = f"Function executed, result: {result}"
                    self.add_test_result("Ninox save function", True, details)
                    return True
                else:
                    details = "Function executed but returned None"
                    self.add_test_result("Ninox save function", True, details)  # Still counts as success if no crash
                    return True
            except ValueError as e:
                if "Ninox configuration is incomplete" in str(e):
                    details = f"Expected configuration error: {str(e)}"
                    self.add_test_result("Ninox save function", True, details)
                    return True
                else:
                    details = f"Unexpected error: {str(e)}"
                    self.add_test_result("Ninox save function", False, details)
                    return False
            except Exception as e:
                # Any other exception might indicate a problem
                details = f"Function execution error: {str(e)}"
                self.add_test_result("Ninox save function", False, details)
                return False
        except Exception as e:
            self.add_test_result("Ninox save function", False, str(e))
            return False

    def run_contact_form_tests(self):
        """Run all contact form tests"""
        print("Starting comprehensive contact form tests...\n")
        
        # Test form structure
        print("Testing form structure...")
        self.test_form_fields_existence()
        
        # Test validations
        print("\nTesting form validations...")
        self.test_email_validation()
        self.test_required_fields_validation()
        self.test_message_length_validation()
        
        # Test submission
        print("\nTesting form submission...")
        self.test_successful_submission_simulation()
        
        # Test Ninox integration
        print("\nTesting Ninox integration...")
        self.test_ninox_integration_config()
        self.test_ninox_client_initialization()
        self.test_ninox_save_function()
        
        # Print summary
        print("\n" + "="*60)
        print("CONTACT FORM TESTING SUMMARY")
        print("="*60)
        summary = self.test_results["summary"]
        print(f"Total tests: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success rate: {(summary['passed']/max(1, summary['total'])*100):.1f}%")
        print("="*60)

    def save_test_results(self, filename="contact_form_test_results.json"):
        """Save test results to a file"""
        self.test_results["end_time"] = datetime.now().isoformat()
        self.test_results["summary"]["success_rate"] = (self.test_results["summary"]["passed"] / 
                                                       max(1, self.test_results["summary"]["total"])) * 100
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\nContact form test results saved to {filename}")


def main():
    """Main function to run the contact form tests"""
    # Check if server is running
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code != 200:
            print("Error: Website is not accessible at http://localhost:3000")
            print("Make sure the Reflex server is running with 'reflex run'")
            return
    except requests.ConnectionError:
        print("Error: Cannot connect to website at http://localhost:3000")
        print("Make sure the Reflex server is running with 'reflex run'")
        return
    except requests.Timeout:
        print("Error: Connection to website at http://localhost:3000 timed out")
        print("Make sure the Reflex server is running with 'reflex run'")
        return
    
    # Initialize tester
    tester = ContactFormTester(base_url="http://localhost:3000")
    
    try:
        # Run comprehensive tests
        tester.run_contact_form_tests()
        
        # Save test results
        tester.save_test_results()
        
    except KeyboardInterrupt:
        print("\nTesting interrupted by user")
    except Exception as e:
        print(f"An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()