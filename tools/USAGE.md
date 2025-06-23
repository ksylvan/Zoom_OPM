# 🎯 **Zoom Meeting Stress Test Tool - WORKING VERSION**

## ✅ **Status: FULLY FUNCTIONAL**

**The stress testing automation is now working successfully!**

- Participants successfully join meetings muted
- Robust iframe detection implemented
- All major features working as intended

## Key Features

✅ **Auto-handles microphone/camera permissions**
✅ **Direct web app URL construction (no popups!)**
✅ **Participants join muted automatically**
✅ **Robust iframe and element detection**
✅ **Complete automation - no manual intervention**
✅ **Parallel and sequential execution modes**

## Recent Success

### 🎉 **Working Iframe Detection**

- Successfully detects and switches to iframe content
- Robust element detection with multiple selectors
- Debug logging shows all available buttons and elements
- Successfully clicks "Mute" and "Join" buttons

### 🔇 **Confirmed Muted Join**

- Participants automatically join muted (button shows "Unmute" after clicking)
- Smart detection of mute state
- Reduces audio interference during stress testing

### 🎤 **Auto-Permission Handling**

- Chrome automatically grants microphone/camera permissions
- Uses fake media devices for testing
- No manual intervention required

## Usage Examples

```bash
# Quick test with 1 participant (recommended first test)
/Users/kayvan/src/Zoom_OPM/.venv/bin/python tools/stress_test.py \
  --meeting-url "https://us06web.zoom.us/j/MEETINGID?pwd=PASSWORD" \
  --count 1

# Test with 3 participants sequentially
/Users/kayvan/src/Zoom_OPM/.venv/bin/python tools/stress_test.py \
  --meeting-url "https://us06web.zoom.us/j/MEETINGID?pwd=PASSWORD" \
  --count 3 --delay 1

# Stress test with 8 participants joining in parallel
/Users/kayvan/src/Zoom_OPM/.venv/bin/python tools/stress_test.py \
  --meeting-url "https://us06web.zoom.us/j/MEETINGID?pwd=PASSWORD" \
  --count 8 --parallel
```

## Success Indicators

When working correctly, you'll see:

```text
INFO - Successfully clicked Join button using selector '//button[contains(text(), 'Join')]' for TestUser1
INFO - Participant TestUser1 successfully joined the meeting
```

1. **Browser Windows**: Multiple Chrome windows open (one per participant)
2. **Direct Navigation**: Each goes straight to the Zoom meeting web app
3. **Auto-Join**: Automatically finds and clicks join buttons
4. **Muted Participants**: All participants join muted (TestUser1, TestUser2, etc.)
5. **Clean Logs**: Detailed logging shows each step

## Testing Notes

- **Start Small**: Begin with 2-3 participants to verify everything works
- **Resource Usage**: ~150MB RAM per participant
- **Meeting Duration**: Participants stay for 5 minutes by default
- **Logs**: Check `stress_test.log` for detailed activity logs
- **Graceful Shutdown**: Press Ctrl+C to cleanly disconnect all participants
- **Auto-Timeout**: If script is forcefully stopped, participants will timeout from Zoom in 2-3 minutes

## Meeting Host View

You'll see participants join with names like:

- TestUser1 (muted)
- TestUser2 (muted)
- TestUser3 (muted)
- etc.

All will appear muted and ready for your stress testing!
