import React, { useState, useEffect } from 'react';
import './App.css';
import { JokeResponse } from './types/joke';
import { jokeService } from './services/jokeService';
import { JokeDisplay } from './components/JokeDisplay';
import { JokeRequestSection } from './components/JokeRequestSection';

interface TabJokes {
  jokes: JokeResponse[];
  hasMore: boolean;
  currentPage: number;
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

  const updateTabJokes = (tab: string, jokes: JokeResponse[], hasMore: boolean, page: number = 1) => {
    setTabJokes(prev => ({
      ...prev,
      [tab]: {
        jokes: page === 1 ? jokes : [...prev[tab].jokes, ...jokes],
        hasMore,
        currentPage: page
      }
    }));
  };

  const askForJoke = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await jokeService.askForJoke(request, amount);
      updateTabJokes('ask', data.jokes, data.has_more);
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

  return (
    <div className="App">
      <header className="App-header">
        <h1>Joke Generator</h1>
        <p>Multiple ways to get your jokes!</p>
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
        />

        {error && <div className="error-message">{error}</div>}
        
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
