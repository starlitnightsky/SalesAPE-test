# Joke Generator Frontend

A modern React frontend for the Joke Generator API. This application provides a user-friendly interface for requesting jokes using natural language.

## Features

- Natural language joke requests
- Modern, responsive UI
- Support for both single and two-part jokes
- Loading states and error handling
- Mobile-friendly design

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend API running on http://localhost:8000

## Setup

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Start the development server:

```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`

## Usage

1. Type your joke request in the input field (e.g., "Tell me a programming joke")
2. Click "Get Joke" or press Enter
3. The joke will be displayed with its category and content

## Development

- Built with React and TypeScript
- Uses modern CSS features (CSS variables, flexbox, etc.)
- Responsive design for all screen sizes
- Error handling and loading states

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`. Make sure the backend is running before using the frontend.
