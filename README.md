# ScheduleAI — AI-Based Meeting Scheduler

ScheduleAI is an AI-based meeting scheduling application that recommends suitable meeting times by considering participant availability, working hours, meeting duration, and preferences.

The application consists of a React frontend and a FastAPI backend with a machine-learning-based recommendation component.

## Features

- AI-based meeting time recommendations
- Participant availability and conflict checking
- Meeting duration and priority selection
- Multiple recommended time slots
- Time-zone-aware scheduling interface
- Meeting booking management
- Backend API built with FastAPI

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS
- Lucide React

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Scikit-learn
- Joblib

## Project Structure

    ScheduleAI/
    ├── frontend/
    │   ├── src/
    │   ├── index.html
    │   ├── package.json
    │   └── package-lock.json
    │
    ├── backend/
    │   ├── app/
    │   │   ├── core/
    │   │   ├── ml/
    │   │   ├── models/
    │   │   ├── db.py
    │   │   └── main.py
    │   ├── data/
    │   ├── tests/
    │   ├── requirements.txt
    │   └── meeting_ranker.joblib
    │
    └── README.md

## Prerequisites

Install the following before running the application:

- Python 3.10 or later
- Node.js LTS and npm
- Git

## Installation

### 1. Clone the Repository

Open a terminal and run:

    git clone YOUR_REPOSITORY_URL
    cd ScheduleAI

Replace `YOUR_REPOSITORY_URL` with the HTTPS URL of your GitHub repository.

### 2. Set Up the Backend

Open a terminal in the project directory.

Navigate to the backend:

    cd backend

Create a virtual environment:

    python -m venv .venv

Activate it on Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install the dependencies:

    pip install -r requirements.txt

Start the backend:

    python -m uvicorn app.main:app --reload

The backend will run at:

    http://127.0.0.1:8000

### 3. Verify the Backend

Open the API documentation in your browser:

    http://127.0.0.1:8000/docs

The API documentation allows you to inspect and test the available endpoints.

The health-check endpoint is:

    http://127.0.0.1:8000/api/health

Keep the backend terminal running.

### 4. Set Up the Frontend

Open a second terminal in the project directory.

Navigate to the frontend:

    cd frontend

Install dependencies:

    npm ci

Start the development server:

    npm run dev

Open the URL displayed in the terminal. By default, it is:

    http://localhost:5173

Keep the frontend terminal running.

## Running the Application

To use ScheduleAI locally, run both services simultaneously:

| Component | Local URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000 |
| API Documentation | http://127.0.0.1:8000/docs |

The frontend and backend must both be running.

## API Endpoints

The backend currently provides endpoints for:

- Health checks
- User management
- Calendar event management
- Meeting time recommendations
- Feedback submission

Refer to the FastAPI documentation at `/docs` for endpoint details and request schemas.

## Database

The backend uses SQLite for local development.

The database is initialized by the backend. Each developer may have a separate local database.

Do not commit personal data, credentials, or local database files to GitHub.

## Troubleshooting

### Python or pip is not recognized

Install Python and ensure it is available on your system PATH.

### Uvicorn is not installed

Activate the backend virtual environment and run:

    pip install -r requirements.txt

### npm is not recognized

Install Node.js LTS and restart your terminal.

### Port 8000 is already in use

Stop the other process using port 8000 before starting the backend.

### Port 5173 is already in use

Vite may offer another available port. Open the URL shown in the terminal.

### Frontend cannot connect to the backend

Ensure the backend is running and that the frontend's API URL points to:

    http://127.0.0.1:8000

Check the backend CORS configuration if browser requests are blocked.

## Development Notes

- Run the frontend and backend in separate terminals.
- Keep local virtual environments and `node_modules` out of Git.
- Do not commit secrets or personal credentials.
- Ensure required model files are included in the repository or provide instructions to obtain them.
- The frontend's booking and persistence functionality should be verified against the backend before assuming all data is stored in the database.

## License

Add your project's license here if applicable.
