import React from 'react';
import { JokeForm } from './JokeForm';
import { Tabs } from './Tabs';

interface JokeRequestSectionProps {
  activeTab: string;
  onTabChange: (tabId: string) => void;
  request: string;
  onRequestChange: (value: string) => void;
  searchQuery: string;
  onSearchQueryChange: (value: string) => void;
  jokeId: string;
  onJokeIdChange: (value: string) => void;
  categories: string[];
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
  isLoading: boolean;
  onAskForJoke: (e: React.FormEvent) => void;
  onSearchJoke: (e: React.FormEvent) => void;
  onGetJokeById: (e: React.FormEvent) => void;
}

export const JokeRequestSection: React.FC<JokeRequestSectionProps> = ({
  activeTab,
  onTabChange,
  request,
  onRequestChange,
  searchQuery,
  onSearchQueryChange,
  jokeId,
  onJokeIdChange,
  categories,
  selectedCategory,
  onCategoryChange,
  isLoading,
  onAskForJoke,
  onSearchJoke,
  onGetJokeById,
}) => {
  const tabs = [
    { id: 'ask', label: 'Ask for a Joke' },
    { id: 'search', label: 'Search Jokes' },
    { id: 'id', label: 'Get by ID' },
  ];

  return (
    <div className="joke-request-section">
      <Tabs tabs={tabs} activeTab={activeTab} onTabChange={onTabChange} />
      
      <div className="tab-content">
        {activeTab === 'ask' && (
          <JokeForm
            onSubmit={onAskForJoke}
            inputValue={request}
            onInputChange={onRequestChange}
            buttonText="Get Joke"
            placeholder="e.g., Tell me a programming joke"
            isLoading={isLoading}
          />
        )}

        {activeTab === 'search' && (
          <JokeForm
            onSubmit={onSearchJoke}
            inputValue={searchQuery}
            onInputChange={onSearchQueryChange}
            buttonText="Search"
            placeholder="Search for jokes..."
            isLoading={isLoading}
            categories={categories}
            selectedCategory={selectedCategory}
            onCategoryChange={onCategoryChange}
          />
        )}

        {activeTab === 'id' && (
          <JokeForm
            onSubmit={onGetJokeById}
            inputValue={jokeId}
            onInputChange={onJokeIdChange}
            buttonText="Get Joke"
            placeholder="Enter joke ID"
            isLoading={isLoading}
            inputType="number"
          />
        )}
      </div>
    </div>
  );
}; 