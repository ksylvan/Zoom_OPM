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

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sqlite3
import shutil

app = FastAPI()

DATABASE = 'zoom_meeting.db'

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
                PRIMARY KEY (name, status)
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
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT name FROM participants WHERE name = ? AND status = ?', (name, status))
        if cur.fetchone():
            cur.execute('UPDATE participants SET last_seen = ? WHERE name = ? AND status = ?', (current_time, name, status))
        else:
            cur.execute('INSERT INTO participants (name, status, first_seen, last_seen) VALUES (?, ?, ?, ?)', (name, status, current_time, current_time))
        conn.commit()

@app.get("/waiting")
def get_waiting_room():
    participants = get_participants('waiting')
    return {name: {'first_seen': first_seen, 'last_seen': last_seen} for name, first_seen, last_seen in participants}

@app.put("/waiting")
def update_waiting_room(name: str = Body(..., embed=True)):
    update_participant(name, 'waiting')
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT name, first_seen, last_seen FROM participants WHERE name = ? AND status = ?', (name, 'waiting'))
        name, first_seen, last_seen = cur.fetchone()
    return {name: {'first_seen': first_seen, 'last_seen': last_seen}}

@app.get("/joined")
def get_joined_meeting():
    participants = get_participants('joined')
    return {name: {'first_seen': first_seen, 'last_seen': last_seen} for name, first_seen, last_seen in participants}

@app.put("/joined")
def update_joined_meeting(name: str = Body(..., embed=True)):
    update_participant(name, 'joined')
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT name, first_seen, last_seen FROM participants WHERE name = ? AND status = ?', (name, 'joined'))
        name, first_seen, last_seen = cur.fetchone()
    return {name: {'first_seen': first_seen, 'last_seen': last_seen}}

@app.post("/reset")
def reset_meeting():
    reset_db()
    return {"message": "Database reset successfully."}

if __name__ == "__main__":
    init_db()  # Initialize the database
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
