# Joke Search API

A FastAPI-based backend service that integrates with the JokeAPI to provide a natural language interface for requesting jokes. Users can ask for jokes in plain English, and the API will intelligently determine the appropriate category and return a matching joke.

## Features

- Natural language joke requests (e.g., "Tell me a programming joke")
- Automatic category detection from user requests
- Support for both single and two-part jokes
- Safe mode enabled by default
- CORS enabled for frontend integration
- Comprehensive error handling

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message
- `POST /api/ask`: Ask for a joke using natural language
  - Example: `{"request": "Tell me a programming joke"}`
- `GET /api/joke/{joke_id}`: Get a specific joke by ID
- `GET /api/search?query={search_term}&category={category}`: Search for jokes by term and optional category
- `GET /api/categories`: Get list of available joke categories

## Example Requests

1. Natural Language Request:

```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{"request": "Tell me a programming joke"}'
```

2. Search by Category:

```bash
curl "http://localhost:8000/api/search?query=bug&category=Programming"
```

3. Get Categories:

```bash
curl "http://localhost:8000/api/categories"
```

## Running Tests

```bash
pytest
```

## API Documentation

Once the server is running, you can access:

- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`
