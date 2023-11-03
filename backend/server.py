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

from fastapi import Body, FastAPI, HTTPException
from fastapi import __version__ as fastapi_version
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DATABASE = 'zoom_meeting.db'
zoom_manage = "../zoom-manage"

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                host BOOLEAN DEFAULT 0,
                co_host BOOLEAN DEFAULT 0,
                PRIMARY KEY (name, status),
                CHECK ((host = 1 AND co_host = 0) OR (host = 0 AND co_host = 1) OR (host = 0 AND co_host = 0))
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                old_role TEXT,
                new_role TEXT
            )
        ''')

def reset_db():
    # Extract the base name of the database without the .db extension
    base_name = DATABASE.rsplit('.', 1)[0]
    
    # Get the current date and time in the format YYYYMMDD-HHMMSS
    current_datetime = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Form the new name
    backup_name = f"{base_name}-{current_datetime}.db"
    
    # Copy the database file to the new name
    shutil.copy2(DATABASE, backup_name)

    with sqlite3.connect(DATABASE) as conn:
        conn.execute('DROP TABLE IF EXISTS participants')
    init_db()

def get_participants(status):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT name, first_seen, last_seen FROM participants WHERE status = ?', (status,))
        return cur.fetchall()

def update_participant(name, status):
    match = re.match(r'^(.*?)\s+\(([^)]+)\)$', name)
    host, co_host = False, False

    if match:
        name, roles = match.groups()
        host = 'Host' in roles
        co_host = 'co-host' in roles.lower()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT name, host, co_host, first_seen FROM participants WHERE name = ? AND status = ?', (name, status))
        existing_participant = cur.fetchone()
        # If the participant already exists, check for a change in the host or co-host status
        if existing_participant:
            _, old_host, old_co_host, first_seen = existing_participant
            if old_host != host or old_co_host != co_host:
                # Determine the old and new roles
                old_role = 'Host' if old_host else 'Co-host' if old_co_host else 'Participant'
                new_role = 'Host' if host else 'Co-host' if co_host else 'Participant'
                # Log the role change event
                cur.execute(
                    'INSERT INTO events (name, timestamp, old_role, new_role) VALUES (?, ?, ?, ?)',
                    (name, current_time, old_role, new_role)
                )
            cur.execute(
                'UPDATE participants SET last_seen = ?, host = ?, co_host = ? WHERE name = ? AND status = ?',
                (current_time, host, co_host, name, status)
            )
        else:
            first_seen = current_time
            cur.execute(
                'INSERT INTO participants (name, status, first_seen, last_seen, host, co_host) VALUES (?, ?, ?, ?, ?, ?)',
                (name, status, current_time, current_time, host, co_host)
            )
        conn.commit()
        return (name, first_seen, current_time)

@app.get("/health")
async def read_health():
    current_datetime = datetime.now().strftime('%Y%m%d-%H%M%S')
    return {
        "python_version": python_version,
        "fastapi_version": fastapi_version,
        "current_datetime": current_datetime
    }

@app.get("/waiting")
def get_waiting_room():
    participants = get_participants('waiting')
    return {name: {'first_seen': first_seen, 'last_seen': last_seen} for name, first_seen, last_seen in participants}

@app.put("/waiting")
def update_waiting_room(name: str = Body(..., embed=True)):
    name, first_seen, last_seen = update_participant(name, 'waiting')
    return {name: {'first_seen': first_seen, 'last_seen': last_seen}}

@app.put("/waiting_list")
def update_waiting_list(names: List[str] = Body(...)):
    for name in names:
        update_participant(name, 'waiting')
    return {"message": f"Updated {len(names)} participants."}

@app.get("/joined")
def get_joined_meeting():
    participants = get_participants('joined')
    return {name: {'first_seen': first_seen, 'last_seen': last_seen} for name, first_seen, last_seen in participants}

@app.put("/joined")
def update_joined_meeting(name: str = Body(..., embed=True)):
    name, first_seen, last_seen = update_participant(name, 'joined')
    return {name: {'first_seen': first_seen, 'last_seen': last_seen}}

@app.put("/joined_list")
def update_joined_list(names: List[str] = Body(...)):
    for name in names:
        update_participant(name, 'joined')
    return {"message": f"Updated {len(names)} participants."}

@app.post("/reset")
def reset_meeting():
    reset_db()
    return {"message": "Database reset successfully."}

@app.post("/cmd_roster")
def execute_roster():
    result = subprocess.run([zoom_manage, "roster"], capture_output=True)
    return result

@app.post("/cmd_hands")
def execute_hands():
    result = subprocess.run([zoom_manage, "hands"], capture_output=True)
    return result

@app.post("/cmd_admit")
def execute_admit():
    result = subprocess.run([zoom_manage, "admit"], capture_output=True)
    return result

if __name__ == "__main__":
    init_db()  # Initialize the database
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
