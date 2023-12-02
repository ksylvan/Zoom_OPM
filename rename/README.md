# Rename Mappings Setup

Place files inside this directory using whatever naming scheme you want.

Each file should contain the names of participants to be renamed on entry to the meeting.

For example, you could have a file "WSO.txt" containing:

```text
# You can commment your renaming files
#

# ASL interpreters need "@"
Mickey Rooney->@Mickey Rooney

# Empty lines are also ignored
#

# Staff members with a preceding "#"
Jinendra Jain->#Jinendra Jain
```

Then invoke the `zoom-manager` application like this:

```bash
export ZOOM_RENAME_FILE=rename/your_file.txt
./zoom-manage roster
```

Note: If you want the automatic roster from the frontend to work correctly with this
functionality, you need to ensure that the shell that starts the backed server
has the ZOOM_RENAME_FILE environment variable correctly set up. For example:

```bash
export ZOOM_RENAME_FILE=rename/your_file.txt
./zoom-manage server
./zoom-manage dashboard
```

Alternatively, you can place a `.env` file in the `backend/` directory
that contains the following:

```bash
ZOOM_RENAME_FILE=rename/your_file.txt
```

Then in the dashboard, you can toggle the "Automatic Roster Update" button
and when any of the guests that needs to be renamed show up in the meeting,
they will be automatically renamed.
