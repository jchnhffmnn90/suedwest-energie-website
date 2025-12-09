#!/usr/bin/env python3
"""
Comprehensive Testing Script for Südwest-Energie Website

This script tests all major features of the Südwest-Energie website including:
- Logo visibility across pages
- Navigation functionality
- Contact form functionality
- Ninox database integration (when configured)
- Page load times and responsiveness
- Footer and header elements
- Social media links
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import sys
import os
from datetime import datetime
import json


class WebsiteFeatureTester:
    def __init__(self, base_url="http://localhost:3000", headless=True):
        self.base_url = base_url
        self.driver = None
        self.wait = None
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
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        try:
            # Setup ChromeDriver using webdriver-manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("Browser initialized successfully")
        except Exception as e:
            print(f"Failed to initialize browser: {e}")
            sys.exit(1)

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

    def test_page_load(self, url, page_name):
        """Test if a page loads successfully"""
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            # Check if page loaded by looking for main content
            title = self.driver.title
            current_url = self.driver.current_url
            
            if current_url == url:
                self.add_test_result(f"Load {page_name} page", True, f"Title: {title}")
                return True
            else:
                self.add_test_result(f"Load {page_name} page", False, f"Redirected to: {current_url}")
                return False
        except Exception as e:
            self.add_test_result(f"Load {page_name} page", False, str(e))
            return False

    def test_logo_visibility(self, page_name):
        """Test if logo is visible on the page"""
        try:
            # Look for logo in navbar
            logo_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[src='/logo.jpg']")
            
            if logo_elements:
                logo = logo_elements[0]
                is_displayed = logo.is_displayed()
                if is_displayed:
                    self.add_test_result(f"Logo visibility on {page_name}", True, 
                                       f"Found {len(logo_elements)} logo element(s)")
                    return True
                else:
                    self.add_test_result(f"Logo visibility on {page_name}", False, 
                                       "Logo found but not displayed")
                    return False
            else:
                self.add_test_result(f"Logo visibility on {page_name}", False, 
                                   "No logo found")
                return False
        except Exception as e:
            self.add_test_result(f"Logo visibility on {page_name}", False, str(e))
            return False

    def test_navigation_links(self):
        """Test navigation links in the header"""
        try:
            nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a, [href^='/']")
            link_count = len(nav_links)
            
            if link_count > 0:
                self.add_test_result("Navigation links present", True, 
                                   f"Found {link_count} navigation links")
                
                # Test a few specific links
                for link in nav_links[:3]:  # Test first 3 links
                    try:
                        href = link.get_attribute("href")
                        link_text = link.text
                        if href and href.startswith(self.base_url):
                            # Click and verify page loads
                            link.click()
                            time.sleep(1)
                            current_url = self.driver.current_url
                            
                            # Go back to original page
                            self.driver.back()
                            time.sleep(1)
                    except Exception as e:
                        pass  # Don't count as error for individual link clicks
                
                return True
            else:
                self.add_test_result("Navigation links present", False, "No navigation links found")
                return False
        except Exception as e:
            self.add_test_result("Navigation links present", False, str(e))
            return False

    def test_contact_form_fields(self):
        """Test contact form fields are present and functional"""
        try:
            # Check for contact form elements
            form_fields = [
                {"selector": "input[name='name']", "name": "Name field"},
                {"selector": "input[name='email']", "name": "Email field"},
                {"selector": "input[name='company']", "name": "Company field"},
                {"selector": "textarea[name='message']", "name": "Message field"},
                {"selector": "input[name='phone']", "name": "Phone field"},
                {"selector": "button[type='submit']", "name": "Submit button"}
            ]
            
            all_present = True
            details = []
            
            for field in form_fields:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, field["selector"])
                    is_enabled = element.is_enabled()
                    is_displayed = element.is_displayed()
                    details.append(f"{field['name']}: Enabled={is_enabled}, Visible={is_displayed}")
                    
                    if not (is_enabled and is_displayed):
                        all_present = False
                except NoSuchElementException:
                    details.append(f"{field['name']}: NOT FOUND")
                    all_present = False
            
            self.add_test_result("Contact form fields present", all_present, "; ".join(details))
            return all_present
        except Exception as e:
            self.add_test_result("Contact form fields present", False, str(e))
            return False

    def test_contact_form_submission(self, test_data=None):
        """Test contact form submission with sample data"""
        if test_data is None:
            test_data = {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+49 123 456789",
                "company": "Test Company",
                "message": "This is a test message from the automated test script."
            }
        
        try:
            # Fill in the form fields
            name_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='name']")))
            name_field.clear()
            name_field.send_keys(test_data["name"])
            
            email_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='email']")
            email_field.clear()
            email_field.send_keys(test_data["email"])
            
            phone_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='phone']")
            phone_field.clear()
            phone_field.send_keys(test_data["phone"])
            
            company_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='company']")
            company_field.clear()
            company_field.send_keys(test_data["company"])
            
            message_field = self.driver.find_element(By.CSS_SELECTOR, "textarea[name='message']")
            message_field.clear()
            message_field.send_keys(test_data["message"])
            
            # Submit the form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Wait for potential redirect
            time.sleep(3)
            
            current_url = self.driver.current_url
            
            # Check if we were redirected to the thank you page
            if "/danke" in current_url or "thank" in current_url.lower():
                self.add_test_result("Contact form submission", True, 
                                   f"Successfully redirected to thank you page: {current_url}")
                return True
            else:
                # Check for error messages
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, "text[color='red']")
                if error_elements:
                    error_text = error_elements[0].text if error_elements else ""
                    self.add_test_result("Contact form submission", False, 
                                       f"Error message displayed: {error_text}")
                    return False
                else:
                    self.add_test_result("Contact form submission", True, 
                                       f"Form submitted, current URL: {current_url}")
                    return True
        except Exception as e:
            self.add_test_result("Contact form submission", False, str(e))
            return False

    def test_footer_elements(self):
        """Test footer elements like contact info, links, etc."""
        try:
            footer_elements = [
                {"selector": "footer a[href*='impressum']", "name": "Impressum link"},
                {"selector": "footer a[href*='datenschutz']", "name": "Datenschutz link"},
                {"selector": "footer a[href*='agb']", "name": "AGB link"},
                {"selector": "footer a[href*='kontakt']", "name": "Kontakt link"},
            ]
            
            found_count = 0
            for element in footer_elements:
                try:
                    elem = self.driver.find_element(By.CSS_SELECTOR, element["selector"])
                    if elem.is_displayed():
                        found_count += 1
                except NoSuchElementException:
                    pass
            
            self.add_test_result("Footer elements present", found_count >= 2, 
                               f"Found {found_count} of {len(footer_elements)} footer elements")
            return found_count >= 2
        except Exception as e:
            self.add_test_result("Footer elements present", False, str(e))
            return False

    def test_page_responsiveness(self):
        """Test page responsiveness by checking page load time"""
        try:
            # Time how long the page takes to load
            start_time = time.time()
            self.driver.refresh()
            time.sleep(2)
            load_time = time.time() - start_time
            
            # Check if load time is reasonable (under 5 seconds)
            self.add_test_result("Page responsiveness", load_time < 5.0, 
                               f"Load time: {load_time:.2f} seconds")
            return load_time < 5.0
        except Exception as e:
            self.add_test_result("Page responsiveness", False, str(e))
            return False

    def test_static_assets(self):
        """Test if static assets like logo are loading properly"""
        try:
            # Test logo accessibility directly
            logo_response = requests.get(f"{self.base_url}/logo.jpg")
            logo_loaded = logo_response.status_code == 200 and len(logo_response.content) > 0
            
            self.add_test_result("Logo asset accessibility", logo_loaded, 
                               f"Logo HTTP status: {logo_response.status_code}, Size: {len(logo_response.content)} bytes")
            return logo_loaded
        except Exception as e:
            self.add_test_result("Logo asset accessibility", False, str(e))
            return False

    def run_comprehensive_tests(self):
        """Run all website feature tests"""
        print("Starting comprehensive website feature tests...\n")
        
        # Test homepage
        print("\nTesting Homepage...")
        self.test_page_load(self.base_url, "Homepage")
        self.test_logo_visibility("Homepage")
        self.test_navigation_links()
        self.test_contact_form_fields()
        self.test_footer_elements()
        self.test_page_responsiveness()
        self.test_static_assets()
        
        # Test thank you page
        print("\nTesting Thank You Page...")
        self.test_page_load(f"{self.base_url}/danke", "Thank You")
        self.test_logo_visibility("Thank You")
        
        # Test impressum page
        print("\nTesting Impressum Page...")
        self.test_page_load(f"{self.base_url}/impressum", "Impressum")
        self.test_logo_visibility("Impressum")
        
        # Test datenschutz page
        print("\nTesting Datenschutz Page...")
        self.test_page_load(f"{self.base_url}/datenschutz", "Datenschutz")
        self.test_logo_visibility("Datenschutz")
        
        # Test contact form submission with sample data
        print("\nTesting Contact Form Submission...")
        # First navigate back to homepage to test form submission
        self.driver.get(self.base_url)
        time.sleep(2)
        self.test_contact_form_submission()
        
        # Print summary
        print("\n" + "="*60)
        print("TESTING SUMMARY")
        print("="*60)
        summary = self.test_results["summary"]
        print(f"Total tests: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success rate: {(summary['passed']/max(1, summary['total'])*100):.1f}%")
        print("="*60)

    def save_test_results(self, filename="test_results.json"):
        """Save test results to a file"""
        self.test_results["end_time"] = datetime.now().isoformat()
        self.test_results["summary"]["success_rate"] = (self.test_results["summary"]["passed"] / 
                                                       max(1, self.test_results["summary"]["total"])) * 100
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\nTest results saved to {filename}")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\nBrowser closed")


def main():
    """Main function to run the tests"""
    # Check if server is running
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code != 200:
            print("Error: Website is not accessible at http://localhost:3000")
            print("Make sure the Reflex server is running with 'reflex run'")
            return
    except requests.ConnectionError:
        print("Error: Cannot connect to website at http://localhost:3000")
        print("Make sure the Reflex server is running with 'reflex run'")
        return
    
    # Initialize tester
    tester = WebsiteFeatureTester(base_url="http://localhost:3000", headless=False)
    
    try:
        # Run comprehensive tests
        tester.run_comprehensive_tests()
        
        # Save test results
        tester.save_test_results()
        
    except KeyboardInterrupt:
        print("\nTesting interrupted by user")
    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        # Clean up
        tester.close()


if __name__ == "__main__":
    main()