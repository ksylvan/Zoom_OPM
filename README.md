# Zoom OPM Tools

Welcome to the Zoom OPM Tools repository, a place created with a single clear intention: to make the
lives of Online Program Managers (OPMs) easier as they deliver the personal and business development
programs of [Landmark Worldwide][landmark] via [Zoom][zoom] to a global audience.

Every day, all over the world, Online Program Managers, in partnership wth Landmark Program Leaders,
are expanding the reach of Landmark's transformative programs, creating the space inside which
individuals and organizations embark on their journey of personal and professional excellence and
effectveness.

While this repository is meant to be used by OPMs who coordinate large meetings or wokshops
via [Zoom][zoom], the scripts are general purpose and can be used by anyone who runs large Zoom meetings
or seminars.

## Table of Contents

- [Zoom OPM Tools](#zoom-opm-tools)
  - [Table of Contents](#table-of-contents)
  - [Zoom Roster script](#zoom-roster-script)
  - [Platform Compatibility](#platform-compatibility)
    - [Features](#features)
    - [Usage](#usage)
    - [Script Overview](#script-overview)
    - [Known Issues](#known-issues)
    - [Future Enhancements](#future-enhancements)
  - [Contributing](#contributing)
  - [License](#license)

## Zoom Roster script

This script automates the process of generating a roster list from a running Zoom
meeting. It creates two files in the `logs/` subdirectory of the directory from
which the script is run, namely `YYYYMMDD-log.txt` and `YYYYMMDD-roster.txt`,
where `YYYYMMDD` is the current date.

The script checks if the Zoom app is running, whether a Zoom meeting is in progress,
and queries the Participants pane to gather the list of participants.

## Platform Compatibility

This is an AppleScript application built to run natively on macOS, making it
compatible with most macOS versions spanning from the older releases to the latest.

It has been tested on macOS Sonoma (14.0) on an Apple M2 MacBook Air, running
Zoom version 5.16.2 (23409).

### Features

- Checks for a running Zoom application and an active Zoom meeting.
- Creates and manages a `logs/` subdirectory for storing log and roster files.
- Logs events and errors to a `YYYYMMDD-log.txt` file.
- Generates a `YYYYMMDD-roster.txt` file with a list of participants in the
  current Zoom meeting.
- Utilizes AppleScript's GUI Scripting capabilities to interact with the Zoom
  application's user interface.

### Usage

Ensure that your Zoom application is installed.

Run the script using the following command in the terminal:

```shell
./zoom-roster.applescript
```

The script will create a logs/ subdirectory (if it doesn't already exist)
in the directory from which the script is run.

Inside the logs/ subdirectory, you will find the YYYYMMDD-log.txt and
YYYYMMDD-roster.txt files. The YYYYMMDD-log.txt file contains log entries
generated during the script's execution, and the YYYYMMDD-roster.txt file
contains the list of participants in the current Zoom meeting.

### Script Overview

The script is structured into several handler functions and a main() function
that orchestrates the execution of these handlers. Here's a brief description of
some of the key handlers:

- setUpFiles() sets up the log and roster files in the logs/ subdirectory.
- checkZoomRunning() checks if the Zoom app is running.
- startParticipantWindow() activates the Participants pane in the Zoom app.
- generateRoster() gathers the names of participants and writes them to the YYYYMMDD-roster.txt file.
- logMessage() and writeToRoster() are utility functions for writing to the log and roster files, respectively.
- main() is the entry point of the script, invoking the other handlers in the correct order and handling any errors that occur.

### Known Issues

The script assumes that the Zoom app is installed. If the Zoom app is not
running, the script will start the Zoom app and create a dialog box prompting
the user to start a meeting.

Every once in a while, "System Events" will fail to communicate with the Zoom Meeting window and
the script will abort. When this happens, you will see a dialog box with a message like the following: "Error:
Can’t get every text item of missing value. (-1728)" with a "Quit" button. Clicking on "Quit" and
re-running the script again will work.

### Future Enhancements

Improve error handling and reporting.

Make the script more robust to variations in the Zoom app's user interface.

## Contributing

Feel free to fork this repository and submit pull requests for any enhancements or
bug fixes you contribute.

## License

This script is released under the MIT License.

[landmark]: https://www.landmarkworldwide.com/
[zoom]: http://zoom.us