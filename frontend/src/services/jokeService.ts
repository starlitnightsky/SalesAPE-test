import { JokeResponse, JokesResponse, JokeAPIResponse, CategoriesResponse, JokeRequest } from '../types/joke';

const API_BASE_URL = 'http://localhost:8000';

export const jokeService = {
  async askForJoke(request: string, amount: number = 1): Promise<JokesResponse> {
    const response = await fetch(`${API_BASE_URL}/api/ask?amount=${amount}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ request }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch joke');
    }

    return response.json();
  },

  async searchJoke(query: string, category: string, page: number = 1, amount: number = 5): Promise<JokesResponse> {
    const response = await fetch(
      `${API_BASE_URL}/api/search?query=${encodeURIComponent(query)}&category=${encodeURIComponent(category)}&page=${page}&amount=${amount}`
    );

    if (!response.ok) {
      throw new Error('Failed to search jokes');
    }

    return response.json();
  },

  async getJokeById(id: string): Promise<JokeResponse> {
    const response = await fetch(`${API_BASE_URL}/api/joke/${id}`);

    if (!response.ok) {
      throw new Error('Failed to fetch joke');
    }

    const data: JokeAPIResponse = await response.json();
    return {
      category: data.category,
      setup: data.setup,
      delivery: data.delivery,
      joke: data.joke,
      is_safe: data.safe,
    };
  },

  async getCategories(): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/api/categories`);

    if (!response.ok) {
      throw new Error('Failed to fetch categories');
    }

    const data: CategoriesResponse = await response.json();
    return data.categories;
  },
}; 