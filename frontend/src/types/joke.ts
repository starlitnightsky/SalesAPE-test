export interface JokeResponse {
  category: string;
  setup?: string;
  delivery?: string;
  joke?: string;
  is_safe: boolean;
}

export interface JokesResponse {
  jokes: JokeResponse[];
  total: number;
  page: number;
  has_more: boolean;
}

export interface JokeAPIResponse {
  error: boolean;
  category: string;
  type: string;
  setup?: string;
  delivery?: string;
  joke?: string;
  flags: Record<string, boolean>;
  id: number;
  safe: boolean;
  lang: string;
}

export interface CategoriesResponse {
  categories: string[];
}

export interface JokeRequest {
  request: string;
} 