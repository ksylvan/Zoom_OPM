# Zoom Stress Testing Tool

An automated tool for stress testing Zoom meetings by simulating multiple participants joining via browser automation.

## Features

- **Fully Automated**: No manual intervention required - automatically joins meetings through browser
- **Multiple Participants**: Simulate multiple users joining with unique names
- **Isolated Sessions**: Each participant runs in a separate browser instance with isolated cookies/session data
- **Flexible Execution**: Choose between sequential or parallel participant joining
- **Comprehensive Logging**: Detailed logs of all activities and errors
- **Cross-Platform**: Works on macOS, Linux, and Windows

## How It Works

This tool uses Selenium WebDriver to:

1. Launch separate Chrome browser instances for each simulated participant
2. Navigate to the Zoom meeting URL with unique participant names
3. Automatically click "Join from Your Browser" to bypass the Zoom app popup
4. Handle audio/video permissions and join the meeting
5. Keep participants in the meeting for a specified duration

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser

### Quick Setup

Run the setup script to install all dependencies:

```bash
cd tools
./setup.sh
```

### Manual Installation

If you prefer to install manually:

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# ChromeDriver will be automatically managed by webdriver-manager
```

## Usage

### Basic Examples

```bash
# Basic test with 5 participants joining sequentially
python3 stress_test.py --meeting-url "https://zoom.us/wc/12345/join" --count 5

# Test with 10 participants joining in parallel (faster but more resource intensive)
python3 stress_test.py --meeting-url "https://zoom.us/wc/12345/join" --count 10 --parallel

# Custom delay between participants (default is 2 seconds)
python3 stress_test.py --meeting-url "https://zoom.us/wc/12345/join" --count 8 --delay 3.0
```

### Command Line Options

- `--meeting-url`: **(Required)** The Zoom meeting join URL
- `--count`: Number of simulated participants (default: 5)
- `--delay`: Delay in seconds between launching participants (default: 2.0)
- `--parallel`: Launch participants in parallel instead of sequentially

### Getting the Meeting URL

1. Start or schedule a Zoom meeting
2. Click "Invite" or "Copy Invitation"
3. Look for the join URL that looks like: `https://zoom.us/wc/XXXXXXXXX/join`
4. Use this URL with the `--meeting-url` parameter

## Important Considerations

### Resource Usage

- Each participant uses a separate Chrome browser instance
- Memory usage: ~100-200MB per participant
- CPU usage scales with participant count
- Recommended maximum: 10-15 participants on a typical laptop

### Network Impact

- Each participant creates a separate connection to Zoom
- Audio/video streams may consume significant bandwidth
- Consider your internet connection capacity

### Meeting Host Considerations

- The meeting host will see all test participants join
- Participants will appear with names like "TestUser1", "TestUser2", etc.
- Consider informing other meeting participants about the test

## Troubleshooting

### Common Issues

**Chrome not found**

- Ensure Google Chrome is installed
- On macOS: Chrome should be in `/Applications/Google Chrome.app`

**ChromeDriver issues**

- The tool uses webdriver-manager to automatically handle ChromeDriver
- If issues persist, try updating: `pip3 install --upgrade webdriver-manager`

**Permission errors**

- Chrome may prompt for microphone/camera permissions
- The script attempts to handle these automatically

**Meeting not loading**

- Verify the meeting URL is correct and the meeting is active
- Check your internet connection
- Some corporate networks may block automated browsers

### Logs

The tool creates a `stress_test.log` file with detailed information about each participant's activity.

## Advanced Usage

### Running in Headless Mode

To run browsers without visible windows (useful for servers), uncomment this line in the code:

```python
options.add_argument("--headless")
```

### Customizing Participant Behavior

You can modify the `join_meeting_as_participant` function to:

- Change how long participants stay in the meeting
- Add custom interactions (mute/unmute, chat, etc.)
- Handle different meeting scenarios

### Parallel vs Sequential Mode

- **Sequential**: Participants join one after another with specified delay
- **Parallel**: All participants start joining simultaneously
  - Faster overall execution
  - Higher resource usage
  - May overwhelm the system with too many participants

## Safety and Best Practices

1. **Start Small**: Begin with 2-3 participants to verify everything works
2. **Monitor Resources**: Watch your system's CPU and memory usage
3. **Network Consideration**: Be mindful of bandwidth usage
4. **Meeting Etiquette**: Inform other participants about stress testing
5. **Gradual Scaling**: Increase participant count gradually

## Example Output

```
2024-06-23 10:30:15,123 - INFO - Starting stress test with 5 participants
2024-06-23 10:30:15,124 - INFO - Meeting URL: https://zoom.us/wc/12345/join
2024-06-23 10:30:15,125 - INFO - Starting participant TestUser1 (ID: 1)
2024-06-23 10:30:18,456 - INFO - Clicking 'Join from Your Browser' for TestUser1
2024-06-23 10:30:21,789 - INFO - Participant TestUser1 successfully joined the meeting
2024-06-23 10:30:23,124 - INFO - Starting participant TestUser2 (ID: 2)
...
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## Disclaimer

This tool is for testing purposes only. Use responsibly and in compliance with Zoom's terms of service and your organization's policies.
