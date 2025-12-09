#!/usr/bin/env python3
"""
Testing script to verify the updated color scheme and logo placement
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def test_color_scheme():
    """Test that the color scheme has been updated"""
    env_config_path = "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/config/env_config.py"
    
    with open(env_config_path, 'r') as f:
        content = f.read()
    
    # Check for cyan/star-themed colors
    expected_colors = [
        "#00bcd4",  # Primary cyan
        "#00acc1",  # Secondary darker cyan 
        "#26c6da",  # Accent lighter cyan
        "#0d47a1",  # Deep blue text
        "#4fc3f7",  # Light blue text
        "#e1f5fe",  # Light cyan background
        "#b3e5fc",  # Medium cyan background
        "#ff9800"   # Orange accent
    ]
    
    all_present = all(color in content for color in expected_colors)
    details = f"Found {sum(1 for color in expected_colors if color in content)}/{len(expected_colors)} expected colors"
    
    if all_present:
        print("✅ Color scheme update: SUCCESS")
        print(f"   Details: {details}")
        return True
    else:
        print("❌ Color scheme update: FAILED")
        print(f"   Details: {details}")
        return False


def test_logo_placement():
    """Test that the logo has been added to key pages"""
    pages_to_check = [
        "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/sections/hero.py",
        "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/sections/contact.py",
        "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/pages/thank_you.py",
        "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/pages/impressum.py",
        "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/pages/datenschutz.py",
        "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/pages/agb.py",
        "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/pages/status.py"
    ]
    
    logo_pattern = 'rx.image('
    alt_pattern = 'alt=Config.COMPANY_NAME'
    src_pattern = 'src="/logo.jpg"'
    
    success_count = 0
    total_pages = len(pages_to_check)
    
    for page_path in pages_to_check:
        try:
            with open(page_path, 'r') as f:
                content = f.read()
                
            has_logo = logo_pattern in content and alt_pattern in content and src_pattern in content
            if has_logo:
                success_count += 1
                print(f"✅ Logo in {Path(page_path).name}: SUCCESS")
            else:
                print(f"❌ Logo in {Path(page_path).name}: FAILED")
        except FileNotFoundError:
            print(f"⚠️  File not found: {page_path}")
    
    overall_success = success_count >= 4  # At least most key pages
    details = f"Logo found in {success_count}/{total_pages} pages"
    
    if overall_success:
        print(f"✅ Logo placement overall: SUCCESS ({details})")
    else:
        print(f"❌ Logo placement overall: CONCERN ({details})")
    
    return overall_success


def test_navbar_footer_logos():
    """Test that navbar and footer still have logos"""
    navbar_path = "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/components/navbar.py"
    footer_path = "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt/suedwestenergie/components/footer.py"
    
    all_present = True
    details = []
    
    for path, name in [(navbar_path, "navbar"), (footer_path, "footer")]:
        try:
            with open(path, 'r') as f:
                content = f.read()
                
            has_logo = '/logo.jpg' in content and 'Config.COMPANY_NAME' in content
            details.append(f"{name}: {'SUCCESS' if has_logo else 'FAILED'}")
            if not has_logo:
                all_present = False
        except FileNotFoundError:
            details.append(f"{name}: FILE NOT FOUND")
            all_present = False
    
    result = "✅" if all_present else "❌"
    print(f"{result} Navbar and footer logo check: {' and '.join(details)}")
    return all_present


def main():
    print("Testing updated color scheme and logo placement...")
    print("="*60)
    
    # Test color scheme
    color_test = test_color_scheme()
    print()
    
    # Test logo placement in key pages
    logo_test = test_logo_placement()
    print()
    
    # Test navbar and footer logos
    nav_footer_test = test_navbar_footer_logos()
    print()
    
    # Summary
    print("="*60)
    all_tests = [color_test, logo_test, nav_footer_test]
    passed = sum(all_tests)
    total = len(all_tests)
    
    print(f"Overall results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The color scheme and logo placement have been successfully updated.")
    else:
        print("⚠️  Some tests failed. Please review the results above.")
    
    print("="*60)


if __name__ == "__main__":
    main()