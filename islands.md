# Let's count some islands

Create an application that simulates a 10x10 grid where each cell is randomly assigned as either **land** or **sea**, and implements logic to calculate the number of **islands**. An island is one or more land cells connected horizontally or vertically (not diagonally).

## Requirements

### Backend API

- Implement an API to handle the generation and analysis of the grid
- Endpoints / commands should include functionalities like:
  - Generating a new random grid (each cell has a 50/50 chance of being land or sea)
  - Retrieving the current grid
  - Calculating and returning the number of islands in the current grid
- Use any programming language and framework of your choice (e.g., Django, Express.js, Rails, Gin, etc.)

### Frontend

- Develop a simple frontend interface that:
  - Displays the current 10x10 grid, clearly differentiating land and sea
  - Allows users to generate a new grid
  - Shows the calculated number of islands
- Use any frontend framework or library you’re comfortable with (React, Vue, plain HTML/CSS/JS, etc.)

### Focus

If you're applying for a backend role, focus on the backend API and agent logic. If you're applying for a frontend role, focus on the UI and user experience. If you're applying for a full-stack role, feel free to do both!

### Use of AI

We encourage you to use AI tools to assist you in your work, but please ensure that you critique any AI-generated code, and ensure that you understand how it works. We want to see your thought process and how you approach the problem.

### General guidance

- You should use engineering best practices where appropriate. Principles we value include: performance, readability, testability, scalability, and simplicity
- Use a clean separation of concerns between components of your solution. If you’re using a frontend, apply patterns like MVVM or similar
- Please use git, and commit often so we can understand how you approached the problem
- Do not spend more than 2 hours on this. If you are unable to finish, then consider writing some notes on how you would have proceeded

### Bonus points

- Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- Provide Docker configuration files (`Dockerfile`, `docker-compose.yml`, etc.) to make the project easy to run locally
- Include a README with:
  - Instructions for building and running your application
  - A brief overview of your architectural decisions
- Include unit tests or integration tests to ensure the correctness of the island-counting logic and API endpoints

### Submission

Either zip up your solution (including the `.git` folder) and send it over, or share a link to a repository on a cloud git service, such as GitHub, GitLab, or Bitbucket.
