import { jokeService } from '../jokeService';

// Mock fetch
global.fetch = jest.fn();

describe('jokeService', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  describe('askForJoke', () => {
    it('should fetch a joke successfully', async () => {
      const mockResponse = {
        jokes: [{
          category: 'Programming',
          setup: 'Why do programmers prefer dark mode?',
          delivery: 'Because light attracts bugs!',
          is_safe: true
        }],
        total: 1,
        page: 1,
        has_more: false
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const result = await jokeService.askForJoke('Tell me a programming joke', 1);
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/ask?amount=1',
        expect.any(Object)
      );
    });

    it('should handle errors', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false
      });

      await expect(jokeService.askForJoke('Tell me a joke')).rejects.toThrow('Failed to fetch joke');
    });
  });

  describe('searchJoke', () => {
    it('should search jokes successfully', async () => {
      const mockResponse = {
        jokes: [{
          category: 'Programming',
          joke: 'Why do programmers prefer dark mode?',
          is_safe: true
        }],
        total: 1,
        page: 1,
        has_more: false
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const result = await jokeService.searchJoke('programming', 'Programming', 1, 5);
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/search?query=programming&category=Programming&page=1&amount=5'
      );
    });
  });

  describe('getJokeById', () => {
    it('should fetch a joke by ID successfully', async () => {
      const mockResponse = {
        error: false,
        category: 'Programming',
        type: 'single',
        joke: 'Why do programmers prefer dark mode?',
        flags: {},
        id: 1,
        safe: true,
        lang: 'en'
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const result = await jokeService.getJokeById('1');
      expect(result).toEqual({
        category: 'Programming',
        joke: 'Why do programmers prefer dark mode?',
        is_safe: true
      });
    });
  });

  describe('getCategories', () => {
    it('should fetch categories successfully', async () => {
      const mockResponse = {
        categories: ['Programming', 'Misc', 'Dark']
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const result = await jokeService.getCategories();
      expect(result).toEqual(['Programming', 'Misc', 'Dark']);
    });
  });
}); 