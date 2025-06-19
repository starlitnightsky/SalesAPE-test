import React, { useState, useEffect } from 'react';
import './App.css';
import { JokeResponse, AIAnalysis } from './types/joke';
import { jokeService } from './services/jokeService';
import { JokeDisplay } from './components/JokeDisplay';
import { JokeRequestSection } from './components/JokeRequestSection';
import { AIAnalysisDisplay } from './components/AIAnalysisDisplay';

interface TabJokes {
  jokes: JokeResponse[];
  hasMore: boolean;
  currentPage: number;
  aiAnalysis?: AIAnalysis;
  contextResponse?: string;
}

function App() {
  const [tabJokes, setTabJokes] = useState<Record<string, TabJokes>>({
    ask: { jokes: [], hasMore: false, currentPage: 1 },
    search: { jokes: [], hasMore: false, currentPage: 1 },
    id: { jokes: [], hasMore: false, currentPage: 1 }
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [request, setRequest] = useState('');
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('Any');
  const [searchQuery, setSearchQuery] = useState('');
  const [jokeId, setJokeId] = useState('');
  const [activeTab, setActiveTab] = useState('ask');
  const [amount, setAmount] = useState(5);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const data = await jokeService.getCategories();
      setCategories(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch categories');
    }
  };

  const handleError = (err: unknown) => {
    setError(err instanceof Error ? err.message : 'Something went wrong');
  };

  const updateTabJokes = (
    tab: string, 
    jokes: JokeResponse[], 
    hasMore: boolean, 
    page: number = 1,
    aiAnalysis?: AIAnalysis,
    contextResponse?: string
  ) => {
    setTabJokes(prev => ({
      ...prev,
      [tab]: {
        jokes: page === 1 ? jokes : [...prev[tab].jokes, ...jokes],
        hasMore,
        currentPage: page,
        aiAnalysis: page === 1 ? aiAnalysis : prev[tab].aiAnalysis,
        contextResponse: page === 1 ? contextResponse : prev[tab].contextResponse
      }
    }));
  };

  const askForJoke = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await jokeService.askForJoke(request, amount);
      updateTabJokes(
        'ask', 
        data.jokes, 
        data.has_more, 
        1, 
        data.ai_analysis, 
        data.context_response
      );
    } catch (err) {
      handleError(err);
      updateTabJokes('ask', [], false);
    } finally {
      setLoading(false);
    }
  };

  const searchJoke = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await jokeService.searchJoke(
        searchQuery,
        selectedCategory,
        tabJokes.search.currentPage,
        amount
      );
      updateTabJokes('search', data.jokes, data.has_more);
    } catch (err) {
      handleError(err);
      updateTabJokes('search', [], false);
    } finally {
      setLoading(false);
    }
  };

  const getJokeById = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jokeId) return;
    
    setLoading(true);
    setError(null);

    try {
      const data = await jokeService.getJokeById(jokeId);
      updateTabJokes('id', [data], false);
    } catch (err) {
      handleError(err);
      updateTabJokes('id', [], false);
    } finally {
      setLoading(false);
    }
  };

  const loadMore = async () => {
    if (!tabJokes[activeTab].hasMore || loading) return;

    setLoading(true);
    try {
      if (activeTab === 'search') {
        const data = await jokeService.searchJoke(
          searchQuery,
          selectedCategory,
          tabJokes.search.currentPage + 1,
          amount
        );
        updateTabJokes('search', data.jokes, data.has_more, tabJokes.search.currentPage + 1);
      }
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    setError(null);
  };

  const handleClearJokes = (tabId: string) => {
    setTabJokes(prev => ({
      ...prev,
      [tabId]: {
        jokes: [],
        hasMore: false,
        currentPage: 1
      }
    }));
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI-Powered Joke Generator</h1>
        <p>Ask for jokes naturally and see how AI understands your requests!</p>
      </header>

      <main className="App-main">
        <JokeRequestSection
          activeTab={activeTab}
          onTabChange={handleTabChange}
          request={request}
          onRequestChange={setRequest}
          searchQuery={searchQuery}
          onSearchQueryChange={setSearchQuery}
          jokeId={jokeId}
          onJokeIdChange={setJokeId}
          categories={categories}
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
          isLoading={loading}
          onAskForJoke={askForJoke}
          onSearchJoke={searchJoke}
          onGetJokeById={getJokeById}
          onClearJokes={handleClearJokes}
        />

        {error && <div className="error-message">{error}</div>}
        
        {/* Show AI Analysis for ask tab */}
        {activeTab === 'ask' && tabJokes.ask.aiAnalysis && (
          <AIAnalysisDisplay 
            analysis={tabJokes.ask.aiAnalysis}
            contextResponse={tabJokes.ask.contextResponse}
          />
        )}
        
        <div className="jokes-container">
          {tabJokes[activeTab].jokes.map((joke, index) => (
            <JokeDisplay key={index} joke={joke} />
          ))}
        </div>

        {tabJokes[activeTab].hasMore && (
          <button 
            className="load-more-button"
            onClick={loadMore}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Load More'}
          </button>
        )}
      </main>
    </div>
  );
}

export default App;
