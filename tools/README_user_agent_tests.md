# User Agent Tests

This directory contains unit tests for the `get_user_agent()` function that demonstrate monkey-patching of `platform.system()` to test user agent selection for different operating systems.

## Test Files

### `test_user_agent.py`

Comprehensive test suite with 14 test cases covering:

- All supported operating systems (Windows, Darwin/macOS, Linux)
- Fallback behavior for unknown operating systems
- Edge cases (None, empty string, case sensitivity)
- User agent format validation
- Consistency checks
- Integration testing

### `test_user_agent_demo.py`

Simple demonstration showing the core monkey-patching concept with 4 basic test cases:

- Windows user agent
- Darwin (macOS) user agent
- Linux user agent
- Unknown OS fallback

## Running the Tests

### Using Python's built-in unittest module

```bash
# Run the comprehensive test suite
python test_user_agent.py

# Run the simple demo tests
python test_user_agent_demo.py
```

### Using pytest (if installed)

```bash
# Run all tests with verbose output
pytest test_user_agent*.py -v

# Run specific test file
pytest test_user_agent.py -v
```

## Test Output Example

```text
test_windows_ua (__main__.TestUserAgentDemo.test_windows_ua)
Test Windows user agent by monkey-patching platform.system. ... ok
test_darwin_ua (__main__.TestUserAgentDemo.test_darwin_ua)
Test Darwin (macOS) user agent by monkey-patching platform.system. ... ok
test_linux_ua (__main__.TestUserAgentDemo.test_linux_ua)
Test Linux user agent by monkey-patching platform.system. ... ok
test_unknown_os_fallback (__main__.TestUserAgentDemo.test_unknown_os_fallback)
Test unknown OS fallback by monkey-patching platform.system. ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

## Key Testing Concepts

### Monkey-Patching with unittest.mock.patch

The tests use Python's `unittest.mock.patch` decorator to monkey-patch the `platform.system()` function:

```python
@patch('stress_test.platform.system')
def test_windows_ua(self, mock_platform_system):
    # Mock platform.system to return "Windows"
    mock_platform_system.return_value = "Windows"

    # Call the function under test
    result = get_user_agent()

    # Assert the expected result
    expected = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    self.assertEqual(result, expected)
```

### Expected User Agent Strings

The tests verify that `get_user_agent()` returns these strings for each OS:

- **Windows**: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`
- **Darwin**: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`
- **Linux**: `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`
- **Unknown OS**: Falls back to Windows user agent string

## Dependencies

The tests require:

- Python 3.6+ (for unittest.mock)
- The `stress_test.py` file in the same directory
- No external dependencies required

## Test Coverage

The comprehensive test suite covers:

- ✅ Platform detection for Windows, Darwin, Linux
- ✅ Fallback behavior for unknown operating systems
- ✅ Edge cases (None, empty strings)
- ✅ Case sensitivity validation
- ✅ User agent format validation
- ✅ Consistency checks across multiple calls
- ✅ Verification that `platform.system()` is called
- ✅ Integration testing with real platform detection
