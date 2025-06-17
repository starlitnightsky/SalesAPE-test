import React, { useState, useEffect } from 'react';
import './App.css';
import { JokeResponse } from './types/joke';
import { jokeService } from './services/jokeService';
import { JokeDisplay } from './components/JokeDisplay';
import { JokeRequestSection } from './components/JokeRequestSection';

function App() {
  const [jokes, setJokes] = useState<JokeResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [request, setRequest] = useState('');
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('Any');
  const [searchQuery, setSearchQuery] = useState('');
  const [jokeId, setJokeId] = useState('');
  const [activeTab, setActiveTab] = useState('ask');
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);
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

  const askForJoke = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await jokeService.askForJoke(request, amount);
      setJokes(data.jokes || []);
      setHasMore(data.has_more);
      setCurrentPage(1);
    } catch (err) {
      handleError(err);
      setJokes([]);
    } finally {
      setLoading(false);
    }
  };

  const searchJoke = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await jokeService.searchJoke(searchQuery, selectedCategory, currentPage, amount);
      setJokes(data.jokes || []);
      setHasMore(data.has_more);
    } catch (err) {
      handleError(err);
      setJokes([]);
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
      setJokes([data]);
      setHasMore(false);
      setCurrentPage(1);
    } catch (err) {
      handleError(err);
      setJokes([]);
    } finally {
      setLoading(false);
    }
  };

  const loadMore = async () => {
    if (!hasMore || loading) return;

    setLoading(true);
    try {
      if (activeTab === 'search') {
        const data = await jokeService.searchJoke(searchQuery, selectedCategory, currentPage + 1, amount);
        setJokes(prev => [...(prev || []), ...(data.jokes || [])]);
        setHasMore(data.has_more);
        setCurrentPage(prev => prev + 1);
      }
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
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
          onTabChange={setActiveTab}
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
          {(jokes || []).map((joke, index) => (
            <JokeDisplay key={index} joke={joke} />
          ))}
        </div>

        {hasMore && (
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
