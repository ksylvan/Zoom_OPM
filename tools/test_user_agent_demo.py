#!/usr/bin/env python

"""
Simple demonstration of monkey-patching platform.system() for testing get_user_agent().

This is a minimal example showing the core concept requested in the task.
"""

import unittest
from unittest.mock import patch
import sys
import os
from stress_test import get_user_agent


# Add the current directory to the Python path so we can import from stress_test
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestUserAgentDemo(unittest.TestCase):
    """Simple demonstration of monkey-patching platform.system for UA testing."""

    @patch("stress_test.platform.system")
    def test_windows_ua(self, mock_platform_system):
        """Test Windows user agent by monkey-patching platform.system."""
        # Arrange: Mock platform.system to return "Windows"
        mock_platform_system.return_value = "Windows"

        # Act: Call get_user_agent()
        result = get_user_agent()

        # Assert: Verify the expected Windows user agent string
        expected = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        self.assertEqual(result, expected)

    @patch("stress_test.platform.system")
    def test_darwin_ua(self, mock_platform_system):
        """Test Darwin (macOS) user agent by monkey-patching platform.system."""
        # Arrange: Mock platform.system to return "Darwin"
        mock_platform_system.return_value = "Darwin"

        # Act: Call get_user_agent()
        result = get_user_agent()

        # Assert: Verify the expected Darwin user agent string
        expected = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        self.assertEqual(result, expected)

    @patch("stress_test.platform.system")
    def test_linux_ua(self, mock_platform_system):
        """Test Linux user agent by monkey-patching platform.system."""
        # Arrange: Mock platform.system to return "Linux"
        mock_platform_system.return_value = "Linux"

        # Act: Call get_user_agent()
        result = get_user_agent()

        # Assert: Verify the expected Linux user agent string
        expected = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        self.assertEqual(result, expected)

    @patch("stress_test.platform.system")
    def test_unknown_os_fallback(self, mock_platform_system):
        """Test unknown OS fallback by monkey-patching platform.system."""
        # Arrange: Mock platform.system to return an unknown OS
        mock_platform_system.return_value = "UnknownOS"

        # Act: Call get_user_agent()
        result = get_user_agent()

        # Assert: Verify it falls back to the generic (Windows) user agent
        expected = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
