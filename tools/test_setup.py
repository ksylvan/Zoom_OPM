#!/usr/bin/env python3

"""
Demo script to test if the Selenium setup is working correctly.
This script opens a browser, navigates to Google, and closes it.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def test_selenium_setup():
    """Test if Selenium and ChromeDriver are working correctly"""
    print("Testing Selenium setup...")

    try:
        # Create Chrome options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Initialize Chrome driver with automatic driver management
        print("Installing/updating ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print("Opening browser...")
        driver.get("https://www.google.com")
        print("Successfully opened Google!")

        # Wait a moment
        time.sleep(2)

        # Close browser
        driver.quit()
        print("Browser closed successfully.")
        print("✅ Selenium setup is working correctly!")
        return True

    except Exception as e:
        print(f"❌ Error during setup test: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Google Chrome is installed")
        print("2. Try running: pip3 install --upgrade selenium webdriver-manager")
        print("3. Check your internet connection (needed to download ChromeDriver)")
        return False


if __name__ == "__main__":
    success = test_selenium_setup()
    sys.exit(0 if success else 1)
