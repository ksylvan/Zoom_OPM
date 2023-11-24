# Zoom OPM Tools

![Zoom OPM Tools][zoom-opm-tools-logo]

Welcome to the Zoom OPM Tools repository, a place created with a single clear intention: to make the
lives of Online Program Managers (OPMs) easier as they deliver the personal and business development
programs of [Landmark Worldwide][landmark] via [Zoom][zoom] to a global audience.

Every day, all over the world, Online Program Managers, in partnership with Landmark Program Leaders,
are expanding the reach of Landmark's transformative programs, creating the space inside which
individuals and organizations embark on their journey of personal and professional excellence and
effectiveness.

While this repository is meant to be used by OPMs who coordinate large meetings or workshops
via [Zoom][zoom], the software here is general purpose and can be used by anyone who runs
large Zoom meetings or seminars.

- [Zoom OPM Tools](#zoom-opm-tools)
  - [Confidentiality and Privacy](#confidentiality-and-privacy)
  - [Zoom OPM Tools components](#zoom-opm-tools-components)
    - [Frontend Zoom Meeting Tracker dashboard](#frontend-zoom-meeting-tracker-dashboard)
    - [Backend Server](#backend-server)
    - [The Zoom Manage utility application](#the-zoom-manage-utility-application)
  - [Platform Compatibility](#platform-compatibility)
  - [Features](#features)
  - [Quick Start](#quick-start)
    - [Commands](#commands)
      - [Commonly used commands](#commonly-used-commands)
      - [Roster filter lists](#roster-filter-lists)
      - [Miscellaneous commands](#miscellaneous-commands)
  - [Dependencies](#dependencies)
    - [Known Issues](#known-issues)
    - [Future Enhancements](#future-enhancements)
  - [Contributing](#contributing)
  - [License](#license)

## Confidentiality and Privacy

Please ensure you have the necessary permissions, and you're following
best practices when using scripts and automations during Zoom meetings.

Always respect privacy and confidentiality.

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

The dashboard is a simple [vue.js][vue-js] application that displays the cache of information
that is updated and stored by the backend server. The columns of the dashboard are clickable
and can be used to sort the data in the displayed table.

### Backend Server

The backend server serves as a bridge between the dashboard and the information gathered by
the `zoom-manage` utility application. It manages the database of events related to participants
joining the Zoom meeting and makes that information available to the dashboard.

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
Zoom version 5.16.6 (24664).

The backend component is a [FastAPI][fastapi] server written in Python3 that
serves the "Zoom Meeting Tracker" frontend written with JavaScript. You can
install python3 on your Mac using [homebrew][homebrew].

## Features

1. **Participant Roster Generation**: Generate a list of participants who've joined the Zoom meeting.
2. **Hands Raised Tracking**: Record a list of participants who've raised their hands at any point in time during the meeting.
3. **Camera Off Tracking**: Record a list of participants who have their camera turned off.
4. **Waiting Room Management**: Automate the process of admitting attendees from the waiting room.
5. **Logging**: Maintain a log of meeting activities and actions taken during the meeting.
6. **Integrated Server and Dashboard**: Run a backend server and open a Zoom Meeting Tracker dashboard for enhanced management.

## Quick Start

Clone this repository and ensure you can get the backend API server running.

```bash
git clone https://github.com/ksylvan/Zoom_OPM
```

1. Ensure that the Zoom application is running and that you're in a Zoom
   meeting.

2. Execute the `zoom-manage` script, to run the backend server.

   ```bash
   ./zoom-manage server
   ```

3. Start the dashboard.

   ```bash
   ./zoom-manage dashboard
   ```

   You can now execute specific commands as needed (for example, grab the current roster by using
   the `roster` command, or capture all the hands that are raised by using the `hands` command).

   The most common commands are also available in the dashboard.

### Commands

#### Commonly used commands

- **help**: Display a usage message detailing the available commands.
- **server**: Start the backend server. This will launch the server in its own terminal window.
- **dashboard**: Open the Zoom Meeting Tracker dashboard in a web browser.
- **reset**: Reset the tracking database.
- **roster**: Generate a current list of participants in the meeting. This is the default action if no command is specified.

#### Roster filter lists

- **hands**: Generate a list of participants who've raised their hands.
- **camera_off**: Generate list of camera off participants.
- **camera_on**: Generate list of participants who are on video.
- **no_audio** - get the list of participants not connected to audio.
- **muted** - get the list of participants who are muted.
- **unmuted** - get the list of participants who are unmuted.
- **phone**: List of participants dialing in by phone.

The lists are output into the `filtered.txt` file in the logs directory. If you set
the environment variable `ZOOM_DEBUG` then the filtered lists are also output on
the console (stderr).

```bash
% export ZOOM_DEBUG=true
% ./zoom-manage hands
=== Hand raised 10/29/2023 12:30:17 ===
1 James Tiberius Kirk
2 Spock
3 Leonard H McCoy
=== Hand raised 3 participants 10/29/2023 12:30:24 ===
```

#### Miscellaneous commands

- **admit**: Admit all attendees waiting in the Zoom waiting room.
- **breakout**: Manage creating breakout rooms.
  Run `./zoom-manage breakout help` for details and see [this documentation][breakout-readme]
  for the format of the breakout room files.

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

The backend server and dashboard require additional setup and may have their own dependencies.
Ensure that you've followed the provided [setup instructions][backend-docs].

### Known Issues

The script assumes that the Zoom app is installed. If the Zoom app is not
running, the script will start the Zoom app and create a dialog box prompting
the user to start a meeting.

### Future Enhancements

- Make the script more robust to variations in the Zoom application user interface.

- Assist with creating named Breakout Rooms.

- Port the [zoom-manage][zoom-manage-scrip] script to Windows. To contribute to a Windows version, please read [this note][windows] about potential pathways to make this happen.

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
[windows]: docs/Windows.md
[zoom-manage-scrip]: ./zoom-manage
[zoom-opm-tools-logo]: ./frontend/zoom-opm-tools.png
[breakout-readme]: ./breakout/README.md
