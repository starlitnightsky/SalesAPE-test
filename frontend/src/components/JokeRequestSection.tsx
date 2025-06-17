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
  onClearJokes: (tabId: string) => void;
}

interface TabConfig {
  id: string;
  label: string;
  inputValue: string;
  onInputChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  buttonText: string;
  placeholder: string;
  inputType?: 'number' | 'text';
  showCategories?: boolean;
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
  onClearJokes,
}) => {
  const tabs = [
    { id: 'ask', label: 'Ask for a Joke' },
    { id: 'search', label: 'Search Jokes' },
    { id: 'id', label: 'Get by ID' },
  ];

  const tabConfigs: Record<string, TabConfig> = {
    ask: {
      id: 'ask',
      label: 'Ask for a Joke',
      inputValue: request,
      onInputChange: onRequestChange,
      onSubmit: onAskForJoke,
      buttonText: 'Get Joke',
      placeholder: 'e.g., Tell me a programming joke',
      inputType: 'text',
    },
    search: {
      id: 'search',
      label: 'Search Jokes',
      inputValue: searchQuery,
      onInputChange: onSearchQueryChange,
      onSubmit: onSearchJoke,
      buttonText: 'Search',
      placeholder: 'Search for jokes...',
      inputType: 'text',
      showCategories: true,
    },
    id: {
      id: 'id',
      label: 'Get by ID',
      inputValue: jokeId,
      onInputChange: onJokeIdChange,
      onSubmit: onGetJokeById,
      buttonText: 'Get Joke',
      placeholder: 'Enter joke ID',
      inputType: 'number',
    },
  };

  return (
    <div className="joke-request-section">
      <Tabs tabs={tabs} activeTab={activeTab} onTabChange={onTabChange} />
      
      <div className="tab-content">
        <div className="tab-form-container">
          <JokeForm
            {...tabConfigs[activeTab]}
            isLoading={isLoading}
            categories={tabConfigs[activeTab].showCategories ? categories : undefined}
            selectedCategory={tabConfigs[activeTab].showCategories ? selectedCategory : undefined}
            onCategoryChange={tabConfigs[activeTab].showCategories ? onCategoryChange : undefined}
          />
          <button 
            className="clear-button"
            onClick={() => onClearJokes(activeTab)}
            disabled={isLoading}
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}; 