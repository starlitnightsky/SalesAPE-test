# Joke Generator Application

A modern web application that provides multiple ways to discover and enjoy jokes. Built with React, TypeScript, and FastAPI.

## Features

- **Multiple Joke Request Methods**:
  - Natural language requests (e.g., "Tell me a programming joke")
  - Search by keywords and categories
  - Fetch jokes by ID
- **Modern UI/UX**:
  - Tabbed interface for different request methods
  - Responsive design
  - Loading states and error handling
  - Pagination support
- **Type Safety**:
  - Full TypeScript implementation
  - Type-safe API responses
- **Docker Support**:
  - Easy local development setup
  - Production-ready configuration

## Architecture

The application follows a modern microservices architecture:

### Frontend

- React with TypeScript
- Component-based architecture
- Service layer for API communication
- Responsive design with CSS variables
- Unit tests with Jest

### Backend

- FastAPI (Python)
- RESTful API design
- Integration with JokeAPI.dev
- Error handling and validation
- CORS support

## Prerequisites

- Node.js 18 or higher
- Python 3.9 or higher
- Docker and Docker Compose (for containerized setup)

## Setup Instructions

### Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/starlitnightsky/SalesAPE-test.git
   cd SalesAPE-test
   ```

2. Start the application:

   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Manual Setup

#### Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Test

### Running Tests

Frontend tests:

```bash
cd frontend
npm test
```

Backend tests:

```bash
cd backend
python app/main.py
pytest tests/test_main.py
```

## API Documentation

The backend API documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
