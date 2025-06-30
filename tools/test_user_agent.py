#!/usr/bin/env python3

"""
Unit tests for the get_user_agent() function.

These tests monkey-patch platform.system() to return different operating system
values and verify that get_user_agent() returns the expected user agent strings.
"""

import unittest
from unittest.mock import patch
import sys
import os
from stress_test import get_user_agent

# Add the current directory to the Python path so we can import from stress_test
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestGetUserAgent(unittest.TestCase):
    """Test cases for the get_user_agent() function."""

    def setUp(self):
        """Set up test fixtures with expected user agent strings."""
        # Expected user agent strings for each platform
        self.expected_user_agents = {
            "Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Darwin": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Linux": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        # Generic fallback user agent (should be same as Windows)
        self.generic_fallback = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

    @patch("stress_test.platform.system")
    def test_windows_user_agent(self, mock_platform_system):
        """Test that Windows returns the correct user agent string."""
        mock_platform_system.return_value = "Windows"
        result = get_user_agent()
        self.assertEqual(result, self.expected_user_agents["Windows"])

    @patch("stress_test.platform.system")
    def test_darwin_user_agent(self, mock_platform_system):
        """Test that Darwin (macOS) returns the correct user agent string."""
        mock_platform_system.return_value = "Darwin"
        result = get_user_agent()
        self.assertEqual(result, self.expected_user_agents["Darwin"])

    @patch("stress_test.platform.system")
    def test_linux_user_agent(self, mock_platform_system):
        """Test that Linux returns the correct user agent string."""
        mock_platform_system.return_value = "Linux"
        result = get_user_agent()
        self.assertEqual(result, self.expected_user_agents["Linux"])

    @patch("stress_test.platform.system")
    def test_unknown_os_fallback(self, mock_platform_system):
        """Test that unknown OS returns the generic fallback user agent."""
        mock_platform_system.return_value = "FreeBSD"
        result = get_user_agent()
        self.assertEqual(result, self.generic_fallback)

    @patch("stress_test.platform.system")
    def test_empty_os_fallback(self, mock_platform_system):
        """Test that empty OS string returns the generic fallback user agent."""
        mock_platform_system.return_value = ""
        result = get_user_agent()
        self.assertEqual(result, self.generic_fallback)

    @patch("stress_test.platform.system")
    def test_none_os_fallback(self, mock_platform_system):
        """Test that None OS returns the generic fallback user agent."""
        mock_platform_system.return_value = None
        result = get_user_agent()
        self.assertEqual(result, self.generic_fallback)

    @patch("stress_test.platform.system")
    def test_case_sensitivity(self, mock_platform_system):
        """Test that OS detection is case-sensitive."""
        # Test lowercase - should fallback to generic
        mock_platform_system.return_value = "windows"
        result = get_user_agent()
        self.assertEqual(result, self.generic_fallback)

        # Test mixed case - should fallback to generic
        mock_platform_system.return_value = "DARWIN"
        result = get_user_agent()
        self.assertEqual(result, self.generic_fallback)

    @patch("stress_test.platform.system")
    def test_other_unix_systems(self, mock_platform_system):
        """Test that other Unix-like systems return the generic fallback."""
        unix_systems = ["FreeBSD", "OpenBSD", "NetBSD", "AIX", "SunOS"]

        for system in unix_systems:
            with self.subTest(system=system):
                mock_platform_system.return_value = system
                result = get_user_agent()
                self.assertEqual(result, self.generic_fallback)

    def test_user_agent_format_validity(self):
        """Test that all user agent strings follow expected format."""
        # Test each supported platform
        with patch("stress_test.platform.system") as mock_platform:
            for os_name in ["Windows", "Darwin", "Linux"]:
                with self.subTest(os_name=os_name):
                    mock_platform.return_value = os_name
                    result = get_user_agent()

                    # Check that user agent contains expected components
                    self.assertIn("Mozilla/5.0", result)
                    self.assertIn("AppleWebKit/537.36", result)
                    self.assertIn("Chrome/131.0.0.0", result)
                    self.assertIn("Safari/537.36", result)

    def test_user_agent_consistency(self):
        """Test that multiple calls with same OS return consistent results."""
        with patch("stress_test.platform.system") as mock_platform:
            for os_name in ["Windows", "Darwin", "Linux"]:
                with self.subTest(os_name=os_name):
                    mock_platform.return_value = os_name

                    # Call multiple times
                    result1 = get_user_agent()
                    result2 = get_user_agent()
                    result3 = get_user_agent()

                    # All results should be identical
                    self.assertEqual(result1, result2)
                    self.assertEqual(result2, result3)

    @patch("stress_test.platform.system")
    def test_platform_system_called(self, mock_platform_system):
        """Test that platform.system() is actually called."""
        mock_platform_system.return_value = "Linux"
        get_user_agent()
        mock_platform_system.assert_called_once()

    def test_all_user_agents_are_different(self):
        """Test that each supported OS has a unique user agent string."""
        user_agents = []

        with patch("stress_test.platform.system") as mock_platform:
            for os_name in ["Windows", "Darwin", "Linux"]:
                mock_platform.return_value = os_name
                ua = get_user_agent()
                user_agents.append(ua)

        # Check that all user agents are unique
        self.assertEqual(len(user_agents), len(set(user_agents)))

    def test_user_agent_contains_os_specific_info(self):
        """Test that user agent strings contain OS-specific information."""
        with patch("stress_test.platform.system") as mock_platform:
            # Windows should contain Windows NT
            mock_platform.return_value = "Windows"
            result = get_user_agent()
            self.assertIn("Windows NT", result)

            # Darwin should contain Macintosh
            mock_platform.return_value = "Darwin"
            result = get_user_agent()
            self.assertIn("Macintosh", result)

            # Linux should contain X11 and Linux
            mock_platform.return_value = "Linux"
            result = get_user_agent()
            self.assertIn("X11", result)
            self.assertIn("Linux", result)


class TestUserAgentIntegration(unittest.TestCase):
    """Integration tests for user agent functionality."""

    def test_real_platform_detection(self):
        """Test that the function works with the real platform.system() call."""
        # This test calls the actual function without mocking
        # It should return a valid user agent string
        result = get_user_agent()

        # Basic validation
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("Mozilla/5.0", result)
        self.assertIn("Chrome/131.0.0.0", result)


if __name__ == "__main__":
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTest(loader.loadTestsFromTestCase(TestGetUserAgent))
    suite.addTest(loader.loadTestsFromTestCase(TestUserAgentIntegration))

    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)

    # Exit with appropriate code
    EXIT_CODE = 0 if res.wasSuccessful() else 1
    print(f"\nTests completed. Exit code: {EXIT_CODE}")
    sys.exit(EXIT_CODE)
