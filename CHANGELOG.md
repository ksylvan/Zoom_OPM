# Changelog

All notable changes to the Zoom OPM (Organization & Participant Management) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-01

### Added
- Enhanced breakout room menu lookup resilience for Zoom ≥6.4.6
- Configurable breakout room keywords via `ZOOM_BREAKOUT_KEYWORDS` environment variable
- Automatic menu structure debugging with full menu dumps saved to `logs/zoom-menu-dump-YYYYMMDD.txt`
- Comprehensive hardening improvements to make script more resilient against future UI changes
- Enhanced error handling and debugging capabilities
- Support for multiple breakout room naming conventions (e.g., "Breakout", "Breakout Rooms")
- Automatic menu discovery fallback with detailed logging

### Changed
- Breakout room functionality now uses configurable keyword searches instead of hard-coded strings
- Improved menu discovery logic with better error reporting
- Enhanced debug output when `ZOOM_DEBUG` environment variable is set

### Fixed
- Breakout room menu lookup compatibility issues with Zoom version 6.4.6 and later
- Menu discovery failures now provide comprehensive debugging information
- Improved resilience against Zoom UI changes and menu reorganization

### Technical Details
- Default breakout keywords: "Breakout,Breakout Rooms" (comma-separated)
- Menu dumps include complete menu bar structure, sub-menu exploration, and timestamp information
- Maintains full backward compatibility with existing functionality
- No breaking changes to command-line interface

## [1.0.0] - 2024-XX-XX

### Added
- Initial release of Zoom OPM tools
- Participant roster generation and tracking
- Hands raised tracking and camera status monitoring
- Waiting room management automation
- Meeting activity logging
- Integrated backend server with FastAPI
- Interactive dashboard for meeting management
- Stress testing tools for load testing
- Support for participant renaming and co-host management
- Breakout room creation and management functionality

### Features
- Cross-platform compatibility (macOS focus with Windows pathway documentation)
- Real-time participant monitoring
- Comprehensive meeting analytics
- Automated meeting management workflows
- RESTful API for integration with other tools

### Compatibility
- macOS Sonoma (14.5) and later
- Zoom versions 5.17.11+ through 6.4.6+
- Python 3.8+ for backend components
- AppleScript-based automation for native macOS integration
