# Zoom OPM Tools

Welcome to the Zoom OPM Tools repository, a place created with a single clear intention: to make the
lives of Online Program Managers (OPMs) easier as they deliver the personal and business development
programs of [Landmark Worldwide][landmark] via [Zoom][zoom] to a global audience.

Every day, all over the world, Online Program Managers, in partnership wth Landmark Program Leaders,
are expanding the reach of Landmark's transformative programs, creating the space inside which
individuals and organizations embark on their journey of personal and professional excellence and
effectveness.

While this repository is meant to be used by OPMs who coordinate large meetings or wokshops
via [Zoom][zoom], the software here is general purpose and can be used by anyone who runs
large Zoom meetings or seminars.

- [Zoom OPM Tools](#zoom-opm-tools)
  - [Zoom OPM Tools components](#zoom-opm-tools-components)
    - [Frontend Zoom Meeting Tracker dashboard](#frontend-zoom-meeting-tracker-dashboard)
    - [Backend Server](#backend-server)
    - [The Zoom Manage utility application](#the-zoom-manage-utility-application)
  - [Platform Compatibility](#platform-compatibility)
  - [Features](#features)
  - [How to Use](#how-to-use)
  - [Commands](#commands)
  - [Dependencies](#dependencies)
    - [Known Issues](#known-issues)
    - [Future Enhancements](#future-enhancements)
  - [Contributing](#contributing)
  - [License](#license)

## Zoom OPM Tools components

This package is composed of a few interconnected components:

1. The frontend dashboard.
2. The backend server that is used to store the Zoom Meeting participation information
   (who joined, who was in the "Waiting Room").
3. The `zoom-manage` utility.

These components interact with each other and the Zoom application as illustrated here:

![Architecture][architecture-diagram]

### Frontend Zoom Meeting Tracker dashboard

There is a web dashboard for the "Zoom Meeting Tracker".

![Dasboard][dashboard-pic]

The dashboard is a simple [vue.js][vue-js] application that displays the cache of informmation
that is updated and stored by the backend server. The columns of the dashboard are clickable
and can be used to sort the data in the displayed table.

### Backend Server

The backend server serves as a bridge between the dashboard and the information gathered by
the `zoom-manage` utility application. It manages the database of events related to participants
joining the Zoom meeting and makes that information available to the dahsboard.

See the documentation for the Backend Server and its API [here][backend-docs].

### The Zoom Manage utility application

The `zoom-manange` script is a utility written in AppleScript designed to help manage
Zoom meetings with ease. This script automates common tasks such as tracking participants,
handling the waiting room, monitoring raised hands, and logging meeting activities.

It creates three files in the `logs/` subdirectory of the directory from
which the script is run, namely `YYYYMMDD-log.txt`, `YYYYMMDD-roster.txt`,
and `YYYYMMDD-hands.txt`, where `YYYYMMDD` is the current date.

## Platform Compatibility

This is an AppleScript application built to run natively on macOS, making it
compatible with most macOS versions spanning from the older releases to the latest.

It has been tested on macOS Sonoma (14.0) on an Apple M2 MacBook Air, running
Zoom version 5.16.2 (23409).

The backend component is a [FastAPI][fastapi] server written in Python3 that
serves the "Zoom Meeting Tracker" frontend written with Javascript. You can
install python3 on your Mac using [homebrew][homebrew].

## Features

1. **Participant Roster Generation**: Generate a list of participants who've joined the Zoom meeting.
2. **Hands Raised Tracking**: Record a list of participants who've raised their hands at any point in time during the meeting.
3. **Waiting Room Management**: Automate the process of admitting attendees from the waiting room.
4. **Logging**: Maintain a log of meeting activities and actions taken during the meeting.
5. **Integrated Server and Dashboard**: Run a backend server and open a Zoom Meeting Tracker dashboard for enhanced management.

## How to Use

1. Ensure that the Zoom application is running and that you're in a Zoom
   meeting.
2. Execute the script, providing a specific command if needed.

## Commands

- **help**: Display a usage message detailing the available commands.
- **server**: Start the backend server. This will launch the server in its own terminal window.
- **dashboard**: Open the Zoom Meeting Tracker dashboard in a web browser.
- **reset**: Reset the tracking database.
- **roster**: Generate a current list of participants in the meeting. This is the default action if no command is specified.
- **hands**: Generate a list of participants who've raised their hands.
- **admit**: Admit all attendees waiting in the Zoom waiting room.

To execute a command, use the following syntax:

```shell
/path/to/zoom-manage [command]
```

For example:

```shell
/path/to/zoom-manage roster
```

This will generate a roster of current participants in the Zoom meeting.

## Dependencies

The backend server and dashboard require additional setup and may have their own dependencies. Ensure that you've followed any provided setup instructions.

### Known Issues

The script assumes that the Zoom app is installed. If the Zoom app is not
running, the script will start the Zoom app and create a dialog box prompting
the user to start a meeting.

### Future Enhancements

- Make the script more robust to variations in the Zoom application user interface.

- Assist with craeting named Breakout Rooms.

## Contributing

Feel free to fork this repository and submit pull requests for any enhancements or
bug fixes you contribute.

## License

This work is Copyright (c) 2023, [Kayvan A. Sylvan][linkedin] and is released under the MIT License.

[landmark]: https://www.landmarkworldwide.com/
[zoom]: http://zoom.us
[linkedin]: https://www.linkedin.com/in/kayvansylvan/
[fastapi]: https://fastapi.tiangolo.com/
[vue-js]: https://vuejs.org/
[homebrew]: https://brew.sh/
[backend-docs]: backend/README.md
[dashboard-pic]: docs/dashboard.png
[architecture-diagram]: docs/ZoomMeetingComponents.png
