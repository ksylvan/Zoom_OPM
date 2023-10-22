# Zoom Meeting Tracker API

This FastAPI server provides endpoints to manage and track participants of a Zoom meeting. It offers functionalities to monitor participants who are waiting to join the meeting and those who have already joined.

## Requirements

- Python 3.8 or newer
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ksylvan/Zoom_OPM
   cd Zoom_OPM/backend
   ```

2. Create a virual environment (optional)

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instal the required packages

   ```bash
   pip3 install -r requirements.txt
   ```

## Running the Server

1. If needed, activate the virtual environment

   ```bash
   source venv/bin/activate
   ```

2. Run the FastAPI server:

   ```bash
   python3 server.py
   ```

The server will start on <http://localhost:5000>

## API Endpoints

### 1. Get Participants in Waiting Room

- **URL**: `/waiting`
- **Method**: `GET`
- **Response**: Dictionary of participants waiting to join with their first and last seen timestamps.

### 2. Add/Update Participant in Waiting Room

- **URL**: `/waiting`
- **Method**: `PUT`
- **Request Body**: `name` of the participant (as JSON)
- **Response**: Updated participant details with their first and last seen timestamps.

### 3. Get Participants who have Joined the Meeting

- **URL**: `/joined`
- **Method**: `GET`
- **Response**: Dictionary of participants who have joined the meeting with their first and last seen timestamps.

### 4. Add/Update Participant who has Joined the Meeting

- **URL**: `/joined`
- **Method**: `PUT`
- **Request Body**: `name` of the participant (as JSON)
- **Response**: Updated participant details with their first and last seen timestamps.

### 5. Reset Meeting

- **URL**: `/reset`
- **Method**: `POST`
- **Response**: Confirmation message indicating the database has been reset.

Note: This method also copies the `zoom_meeting.db` file to `zoom_meeting-YYYYMMDD-HHMMSS.db`
before resetting the database.

## License

This software is provided under the MIT License. See the provided [LICENSE](../LICENSE) file for details.