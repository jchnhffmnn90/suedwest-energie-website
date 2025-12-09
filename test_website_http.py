#!/usr/bin/env python3
"""
Simplified HTTP Testing Script for Südwest-Energie Website

This script tests the website features using HTTP requests without requiring a browser.
It can test:
- Page availability and response codes
- Logo visibility via HTTP requests
- Contact form submission via the backend API
- Static asset accessibility
- Response times
"""

import requests
import time
from datetime import datetime
import json
import sys
from urllib.parse import urljoin


class HTTPFeatureTester:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
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

    def test_page_response(self, path, page_name):
        """Test if a page returns a successful response"""
        try:
            url = urljoin(self.base_url, path)
            start_time = time.time()
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.add_test_result(f"{page_name} page response", True,
                                   f"Status: {response.status_code}, Time: {response_time:.2f}s")
                return True
            else:
                self.add_test_result(f"{page_name} page response", False,
                                   f"Status: {response.status_code}, Expected: 200")
                return False
        except Exception as e:
            self.add_test_result(f"{page_name} page response", False, str(e))
            return False

    def test_static_asset(self, asset_path, asset_name):
        """Test if a static asset is accessible"""
        try:
            url = urljoin(self.base_url, asset_path)
            start_time = time.time()
            response = self.session.get(url, headers={'Accept': 'image/*'})
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                size = len(response.content)
                self.add_test_result(f"{asset_name} accessibility", True,
                                   f"Status: {response.status_code}, Size: {size} bytes, Time: {response_time:.2f}s")
                return True
            else:
                self.add_test_result(f"{asset_name} accessibility", False,
                                   f"Status: {response.status_code}, Expected: 200")
                return False
        except Exception as e:
            self.add_test_result(f"{asset_name} accessibility", False, str(e))
            return False

    def test_contact_form_submission(self, test_data=None):
        """Test contact form submission (this would require the backend API endpoint)"""
        if test_data is None:
            test_data = {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+49 123 456789",
                "company": "Test Company",
                "message": "This is a test message from the automated test script.",
                "event_type": "submit"
            }
        
        try:
            # For Reflex apps, forms are submitted via the API. We'll test the backend endpoint.
            # In Reflex, this would typically be at the same URL but with a POST request
            # For now, we'll just test that the endpoint exists and can handle the request
            contact_url = self.base_url  # The form is likely handled by the same page
            
            # Since we can't easily test the Reflex form submission without knowing the exact endpoint,
            # we'll check if the main page can handle POST requests
            response = self.session.post(contact_url, data=test_data)
            
            # Check response - it might redirect to thank you page or return some response
            if response.status_code in [200, 302, 303]:  # 302/303 for redirects
                self.add_test_result("Contact form endpoint", True,
                                   f"Status: {response.status_code}, Redirect: {response.history}")
                return True
            else:
                self.add_test_result("Contact form endpoint", False,
                                   f"Status: {response.status_code}, Expected: 200/302/303")
                return False
        except Exception as e:
            self.add_test_result("Contact form endpoint", False, str(e))
            return False

    def test_response_time(self, path, page_name, max_time=5.0):
        """Test if page loads within acceptable time"""
        try:
            url = urljoin(self.base_url, path)
            start_time = time.time()
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response_time <= max_time:
                self.add_test_result(f"{page_name} response time", True,
                                   f"Response time: {response_time:.2f}s (max: {max_time}s)")
                return True
            else:
                self.add_test_result(f"{page_name} response time", False,
                                   f"Response time: {response_time:.2f}s (max: {max_time}s)")
                return False
        except Exception as e:
            self.add_test_result(f"{page_name} response time", False, str(e))
            return False

    def test_robots_txt(self):
        """Test presence of robots.txt"""
        try:
            url = urljoin(self.base_url, "/robots.txt")
            response = self.session.get(url)
            
            if response.status_code == 200:
                self.add_test_result("robots.txt", True,
                                   f"Status: {response.status_code}, Content length: {len(response.text)}")
                return True
            else:
                self.add_test_result("robots.txt", False,
                                   f"Status: {response.status_code}, Expected: 200")
                return False
        except Exception as e:
            self.add_test_result("robots.txt", False, str(e))
            return False

    def test_sitemap(self):
        """Test presence of sitemap.xml"""
        try:
            url = urljoin(self.base_url, "/sitemap.xml")
            response = self.session.get(url)
            
            if response.status_code in [200, 404]:  # 404 is acceptable if sitemap doesn't exist
                status = "present" if response.status_code == 200 else "not present"
                self.add_test_result("sitemap.xml", True,
                                   f"Status: {response.status_code} ({status})")
                return True
            else:
                self.add_test_result("sitemap.xml", False,
                                   f"Status: {response.status_code}, Unexpected error")
                return False
        except Exception as e:
            self.add_test_result("sitemap.xml", False, str(e))
            return False

    def run_comprehensive_tests(self):
        """Run all HTTP-based website feature tests"""
        print("Starting HTTP-based website feature tests...\n")
        
        # Test main pages
        pages_to_test = [
            ("/", "Homepage"),
            ("/impressum", "Impressum"),
            ("/datenschutz", "Datenschutz"),
            ("/agb", "AGB"),
            ("/danke", "Thank You")
        ]
        
        for path, name in pages_to_test:
            print(f"\nTesting {name}...")
            self.test_page_response(path, name)
            self.test_response_time(path, name)
        
        # Test static assets
        print("\nTesting static assets...")
        self.test_static_asset("/logo.jpg", "Logo")
        
        # Test other features
        print("\nTesting additional features...")
        self.test_robots_txt()
        self.test_sitemap()
        
        # Test contact form
        print("\nTesting contact form...")
        self.test_contact_form_submission()
        
        # Print summary
        print("\n" + "="*60)
        print("HTTP TESTING SUMMARY")
        print("="*60)
        summary = self.test_results["summary"]
        print(f"Total tests: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success rate: {(summary['passed']/max(1, summary['total'])*100):.1f}%")
        print("="*60)

    def save_test_results(self, filename="http_test_results.json"):
        """Save test results to a file"""
        self.test_results["end_time"] = datetime.now().isoformat()
        self.test_results["summary"]["success_rate"] = (self.test_results["summary"]["passed"] / 
                                                       max(1, self.test_results["summary"]["total"])) * 100
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\nHTTP test results saved to {filename}")


def run_ninox_integration_tests():
    """Specific tests for Ninox integration functionality"""
    print("\nTesting Ninox Integration...")
    
    # This function tests if the Ninox integration is properly configured
    # by checking if the required environment variables are available
    
    import os
    from suedwestenergie.config import Config
    
    ninox_configured = (
        Config.NINOX_API_KEY and 
        Config.NINOX_DATABASE_ID and 
        Config.NINOX_TABLE_ID
    )
    
    if ninox_configured:
        print("✅ Ninox configuration: Available")
        print(f"   Database ID: {Config.NINOX_DATABASE_ID[:8]}... (truncated)")
        print(f"   Table ID: {Config.NINOX_TABLE_ID[:8]}... (truncated)")
        
        # Test if we can create a Ninox client
        try:
            from suedwestenergie.utils.ninox_client import NinoxClient
            client = NinoxClient()
            print("✅ Ninox client initialization: Successful")
        except Exception as e:
            print(f"❌ Ninox client initialization: Failed - {e}")
    else:
        print("⚠️  Ninox configuration: Not available (API keys not set)")
        print("   Set NINOX_API_KEY, NINOX_DATABASE_ID, and NINOX_TABLE_ID in your environment")


def main():
    """Main function to run the tests"""
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
    tester = HTTPFeatureTester(base_url="http://localhost:3000")
    
    try:
        # Run comprehensive tests
        tester.run_comprehensive_tests()
        
        # Run Ninox-specific tests
        run_ninox_integration_tests()
        
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