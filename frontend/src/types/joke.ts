export interface JokeResponse {
  category: string;
  setup?: string;
  delivery?: string;
  joke?: string;
  is_safe: boolean;
}

export interface AIAnalysis {
  category: string;
  keywords: string[];
  reasoning: string;
  user_mood: string;
  suggested_amount: number;
}

export interface JokesResponse {
  jokes: JokeResponse[];
  total: number;
  page: number;
  has_more: boolean;
  ai_analysis?: AIAnalysis;
  context_response?: string;
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