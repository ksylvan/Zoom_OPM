#!/usr/bin/env python3

"""
Copyright (c) 2023 Kayvan A. Sylvan

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import re
import shutil
import sqlite3
import subprocess
from datetime import datetime
from sys import version as python_version
from typing import List
import os

from dotenv import load_dotenv

from fastapi import Body, FastAPI
from fastapi import __version__ as fastapi_version
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DATABASE = "zoom_meeting.db"
ZOOM_MANAGE = "../zoom-manage"

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db():
    """
    Initialize the SQLite database and create the necessary tables if they do not exist.
    This function creates two tables: `participants` and `events`.
    The `participants` table stores information about participants in the Zoom meeting,
    while the `events` table logs changes in participant roles.
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS participants (
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                host BOOLEAN DEFAULT 0,
                co_host BOOLEAN DEFAULT 0,
                PRIMARY KEY (name, status),
                CHECK ((host = 1 AND co_host = 0) OR
                    (host = 0 AND co_host = 1) OR (host = 0 AND co_host = 0)
                )
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                old_role TEXT,
                new_role TEXT
            )
        """
        )


def reset_db():
    """
    Reset the database by dropping existing tables and reinitializing the schema.
    """
    # Extract the base name of the database without the .db extension
    base_name = DATABASE.rsplit(".", 1)[0]

    # Get the current date and time in the format YYYYMMDD-HHMMSS
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Form the new name
    backup_name = f"{base_name}-{current_datetime}.db"

    # Copy the database file to the new name
    shutil.copy2(DATABASE, backup_name)

    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DROP TABLE IF EXISTS participants")
    init_db()


def get_participants(status):
    """Retrieve participants from the database based on their status.

    Args:
        status (str): The status of the participants to retrieve.

    Returns:
        List[Tuple[str, str, str]]: A list of tuples containing participant information.
    """
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT name, first_seen, last_seen FROM participants WHERE status = ?",
            (status,),
        )
        return cur.fetchall()


def update_participant(name, status):
    """Update or insert a participant in the database."""
    match = re.match(r"^(.*?)\s+\(([^)]+)\)$", name)
    host, co_host = False, False

    if match:
        name, roles = match.groups()
        host = "Host" in roles
        co_host = "co-host" in roles.lower()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT name, host, co_host, first_seen "
            "FROM participants WHERE name = ? AND status = ?",
            (name, status),
        )
        existing_participant = cur.fetchone()
        # If the participant already exists, check for a change in the host or co-host status
        if existing_participant:
            _, old_host, old_co_host, first_seen = existing_participant
            if old_host != host or old_co_host != co_host:
                # Determine the old and new roles
                old_role = (
                    "Host" if old_host else "Co-host" if old_co_host else "Participant"
                )
                new_role = "Host" if host else "Co-host" if co_host else "Participant"
                # Log the role change event
                cur.execute(
                    "INSERT INTO events (name, timestamp, old_role, new_role) VALUES (?, ?, ?, ?)",
                    (name, current_time, old_role, new_role),
                )
            cur.execute(
                "UPDATE participants SET last_seen = ?, host = ?, "
                "co_host = ? WHERE name = ? AND status = ?",
                (current_time, host, co_host, name, status),
            )
        else:
            first_seen = current_time
            cur.execute(
                "INSERT INTO participants (name, status, first_seen, "
                "last_seen, host, co_host) VALUES (?, ?, ?, ?, ?, ?)",
                (name, status, current_time, current_time, host, co_host),
            )
        conn.commit()
        return (name, first_seen, current_time)


@app.get("/health")
async def read_health():
    """Check the health of the FastAPI application."""
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
    return {
        "python_version": python_version,
        "fastapi_version": fastapi_version,
        "current_datetime": current_datetime,
    }


@app.get("/waiting")
def get_waiting_room():
    """Retrieve participants in the waiting room."""
    participants = get_participants("waiting")
    return {
        name: {"first_seen": first_seen, "last_seen": last_seen}
        for name, first_seen, last_seen in participants
    }


@app.put("/waiting")
def update_waiting_room(name: str = Body(..., embed=True)):
    """Update or insert a participant in the waiting room."""
    name, first_seen, last_seen = update_participant(name, "waiting")
    return {name: {"first_seen": first_seen, "last_seen": last_seen}}


@app.put("/waiting_list")
def update_waiting_list(names: List[str] = Body(...)):
    """Update or insert multiple participants in the waiting room."""
    for name in names:
        update_participant(name, "waiting")
    return {"message": f"Updated {len(names)} participants."}


@app.get("/joined")
def get_joined_meeting():
    """Retrieve participants who have joined the meeting."""
    participants = get_participants("joined")
    return {
        name: {"first_seen": first_seen, "last_seen": last_seen}
        for name, first_seen, last_seen in participants
    }


@app.put("/joined")
def update_joined_meeting(name: str = Body(..., embed=True)):
    """Update or insert a participant who has joined the meeting."""
    name, first_seen, last_seen = update_participant(name, "joined")
    return {name: {"first_seen": first_seen, "last_seen": last_seen}}


@app.put("/joined_list")
def update_joined_list(names: List[str] = Body(...)):
    """Update or insert multiple participants who have joined the meeting."""
    for name in names:
        update_participant(name, "joined")
    return {"message": f"Updated {len(names)} participants."}


@app.post("/reset")
def reset_meeting():
    """Reset the database by dropping existing tables and reinitializing the schema."""
    reset_db()
    return {"message": "Database reset successfully."}


@app.post("/cmd_roster")
def execute_roster():
    """Execute the `zoom-manage roster` command to get the current roster."""
    result = subprocess.run([ZOOM_MANAGE, "roster"], capture_output=True, check=True)
    return result


@app.post("/cmd_hands")
def execute_hands():
    """Execute the `zoom-manage hands` command to get participant hands."""
    result = subprocess.run([ZOOM_MANAGE, "hands"], capture_output=True, check=True)
    return result


@app.post("/cmd_admit")
def execute_admit():
    """Execute the `zoom-manage admit` command to admit participants from the waiting room."""
    result = subprocess.run([ZOOM_MANAGE, "admit"], capture_output=True, check=True)
    return result


@app.get("/env")
def get_environment_variables():
    """Retrieve environment variables for the FastAPI application."""
    # Convert the os.environ dict to a regular dict for FastAPI to handle it properly
    env_vars = dict(os.environ)
    return env_vars


if __name__ == "__main__":
    init_db()  # Initialize the database
    load_dotenv()  # Load the .env file if it exists
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000)
