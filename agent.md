# Let's build a simple AI-powered agent

Create a simple application that combines an AI agent with a third-party API. Your agent should receive input from a user, reason about it, and return a response based on data it fetches from an API.

You can use a free API available online (e.g., [EmojiHub](https://github.com/cheatsnake/emojihub), [SWAPI](https://swapi.dev/), [JokeAPI](https://jokeapi.dev/), etc.), or mock one yourself.

## Example ideas

- If you use EmojiHub: Ask the user how they’re feeling, and return an emoji that matches that mood.
- If you use SWAPI: Let the user describe a Star Wars character, and try to return matching data from the API.
- If you use a jokes API: Let the user ask for a joke by category, and fetch it dynamically.

You don’t need to copy one of these suggestions – feel free to come up with your own use case!

## Requirements

### Backend API

- Implement an API that exposes your agent's functionality
- It should accept user input (e.g., a feeling, a character description, a joke category)
- It should process that input (e.g., using basic prompt engineering or keyword matching)
- It should query a third-party API (or a mock version) and return a relevant response
- Use any language and framework you like (Node.js, Python, Ruby, Go, etc.)

### Frontend

- Build a simple UI that:
  - Accepts user input
  - Displays the agent’s response in a readable format
- Any framework is fine (React, Svelte, Vue, plain HTML/CSS/JS)
- Make sure the UI is user-friendly and visually appealing
- When using a third-party API, ensure that the UI handles loading states and errors gracefully

### Focus

If you're applying for a backend role, focus on the backend API and agent logic. If you're applying for a frontend role, focus on the UI and user experience. If you're applying for a full-stack role, feel free to do both!

### Use of AI

We encourage you to use AI tools to assist you in your work, but please ensure that you critique any AI-generated code, and ensure that you understand how it works. We want to see your thought process and how you approach the problem.

### General guidance

- We’re interested in how you think about and structure your code
- The AI/agent logic doesn’t need to be complex – even simple prompt engineering is great
- Use engineering best practices (clean code, sensible abstractions, error handling)
- You don’t need a database – storing everything in memory or in a flat file is fine
- Use git, and commit often so we can see how you approached the problem
- Please spend no more than 2 hours on this. If you don’t finish, include notes on how you would continue

### Bonus points

- Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- Add Docker configuration (Dockerfile, docker-compose.yml) for easy local setup
- Include a README with:
  - Setup and usage instructions
  - A short description of how your agent works and why you built it that way
- Write unit tests or integration tests for your agent logic or API interactions

### Submission

Either zip up your solution (including the `.git` folder) and send it over, or share a link to a repository on a cloud git service, such as GitHub, GitLab, or Bitbucket.
