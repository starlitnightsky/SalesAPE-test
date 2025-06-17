import React, { useState, useEffect } from 'react';
import './App.css';
import { JokeResponse } from './types/joke';
import { jokeService } from './services/jokeService';
import { JokeDisplay } from './components/JokeDisplay';
import { JokeRequestSection } from './components/JokeRequestSection';

function App() {
  const [joke, setJoke] = useState<JokeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [request, setRequest] = useState('');
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('Any');
  const [searchQuery, setSearchQuery] = useState('');
  const [jokeId, setJokeId] = useState('');
  const [activeTab, setActiveTab] = useState('ask');

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
      const data = await jokeService.askForJoke(request);
      setJoke(data);
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  const searchJoke = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await jokeService.searchJoke(searchQuery, selectedCategory);
      setJoke(data);
    } catch (err) {
      handleError(err);
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
      setJoke(data);
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
        {joke && <JokeDisplay joke={joke} />}
      </main>
    </div>
  );
}

export default App;
