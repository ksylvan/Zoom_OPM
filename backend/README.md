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

2. Create a virtual environment

   On the Mac, the easiest way to do thi is using the [`uv` tool][uv].

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv .env/zoom
   ```

   The output will look like this:

   ```text
   Using Python 3.12.3 interpreter at: /opt/homebrew/opt/python@3.12/bin/python3.12
   Creating virtualenv at: .env/zoom
   Activate with: source .env/zoom/bin/activate
   ```

3. Install the required packages

   ```bash
   source .env/zoom/bin/activate
   uv pip install -r requirements.txt
   ```

## Running the Server

1. Activate the virtual environment

   ```bash
   source .env/zoom/bin/activate
   ```

2. Run the FastAPI server:

   ```bash
   python3 server.py
   ```

The server will start on <http://localhost:5000>

You can also see the auto-generated Swagger style interactive documentation at
[http://localhost:5000/doc][fastapi-swagger] or ReDoc style page at [http://localhost:5000/redoc][fastapi-redoc].
See the [Fast API Documentation][fastapi-docs] for more information.

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

- **URL**: `/joined_list`
- **Method**: `PUT`
- **Request Body**: `names` of the participant (as JSON)
- **Response**: Updated participant details with their first and last seen timestamps.

### 5. Add/Update Participant in the Waiting Room

- **URL**: `/waiting`
- **Method**: `PUT`
- **Request Body**: `name` of the participant (as JSON)
- **Response**: Updated participant details with their first and last seen timestamps.

- **URL**: `/waiting_list`
- **Method**: `PUT`
- **Request Body**: `names` of the participant (as JSON)
- **Response**: Updated participant details with their first and last seen timestamps.

### 6. Reset Meeting

- **URL**: `/reset`
- **Method**: `POST`
- **Response**: Confirmation message indicating the database has been reset.

Note: This method also copies the `zoom_meeting.db` file to `zoom_meeting-YYYYMMDD-HHMMSS.db`
before resetting the database.

### 7. Meeting Roster

- **URL**: `/cmd_roster`
- **Method**: `POST`
- **Response**: Run the `zoom-manager roster` command.

### 8. Capture Hands

- **URL**: `/cmd_hands`
- **Method**: `POST`
- **Response**: Run the `zoom-manager hands` command.

### 9. Admit All

- **URL**: `/cmd_admit`
- **Method**: `POST`
- **Response**: Run the `zoom-manager admit` command.

### 10. Read Health

- **URL**: `/health`
- **Method**: `GET`
- **Response**: Returns a JSON object containing python version, fastpai version, and the current datetime.

### 11. Environment Variables

- **URL**: `/env`
- **Method**: `GET`
- **Response**: Returns a JSON object containing all the environment variables. This is useful for seeing if
  the `ZOOM_RENAME_FILE` environment variable is set up (so auto-renaming of participants will work).

## License

This software is provided under the MIT License. See the provided [LICENSE](../LICENSE) file for details.

[fastapi-swagger]: http://localhost:5000/docs
[fastapi-redoc]: http://localhost:5000/redoc
[fastapi-docs]: https://fastapi.tiangolo.com/#interactive-api-docs
[uv]: https://github.com/astral-sh/uv
