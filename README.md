# AI-Powered Joke Generator Application

A modern web application that demonstrates LLM integration with 3rd party services. Built with React, TypeScript, and FastAPI, featuring an AI agent that understands natural language requests and intelligently fetches jokes from the JokeAPI.

## Features

- **AI-Powered Natural Language Processing**:
  - LLM integration for understanding user intent and mood
  - Intelligent category selection based on request analysis
  - Contextual response generation
  - Fallback to keyword matching if LLM is unavailable
- **Multiple Joke Request Methods**:
  - Natural language requests (e.g., "Tell me a programming joke")
  - Search by keywords and categories
  - Fetch jokes by ID
- **Modern UI/UX**:
  - Tabbed interface for different request methods
  - AI analysis display showing how the LLM interpreted requests
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

The application follows a modern microservices architecture with AI integration:

### Frontend

- React with TypeScript
- Component-based architecture
- Service layer for API communication
- AI analysis display component
- Responsive design with CSS variables
- Unit tests with Jest

### Backend

- FastAPI (Python)
- RESTful API design
- **LLM Service Integration**:
  - OpenAI GPT-3.5-turbo for request analysis
  - Intelligent category and keyword extraction
  - Contextual response generation
  - Graceful fallback to keyword matching
- Integration with JokeAPI.dev
- Error handling and validation
- CORS support

## Prerequisites

- Node.js 18 or higher
- Python 3.9 or higher
- Docker and Docker Compose (for containerized setup)
- **OpenAI API Key** (for LLM functionality)

## Setup Instructions

### Environment Configuration

1. Create a `.env` file in the `backend` directory:

   ```bash
   # OpenAI API Key for LLM integration
   # Get your API key from: https://platform.openai.com/api-keys
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/starlitnightsky/SalesAPE-test.git
   cd SalesAPE-test
   ```

2. Create the environment file as shown above

3. Start the application:

   ```bash
   docker-compose up --build
   ```

4. Access the application:
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

4. Create the `.env` file with your OpenAI API key

5. Start the server:
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

## How the AI Agent Works

The application demonstrates LLM integration with 3rd party services through:

1. **Request Analysis**: When a user submits a natural language request, the LLM analyzes:

   - User intent and mood
   - Appropriate joke category
   - Relevant keywords
   - Suggested number of jokes

2. **Intelligent API Interaction**: The analyzed request is used to:

   - Select the most appropriate category for the JokeAPI
   - Determine optimal number of jokes to fetch
   - Generate contextual responses

3. **Fallback Mechanism**: If the LLM is unavailable, the system gracefully falls back to keyword matching

4. **User Feedback**: The AI analysis is displayed to users, showing:
   - How their request was interpreted
   - Selected category and reasoning
   - Extracted keywords
   - User mood assessment

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

### New AI Endpoints

- `POST /api/ask` - Enhanced with LLM analysis
- `POST /api/analyze` - Analyze requests without fetching jokes

## Example Usage

Try these natural language requests to see the AI in action:

- "I'm feeling sad, cheer me up with some jokes"
- "Tell me some programming jokes for my developer friends"
- "I need some holiday cheer"
- "Give me some dark humor"
- "I love wordplay and puns"
