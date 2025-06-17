import React from 'react';

interface JokeFormProps {
  onSubmit: (e: React.FormEvent) => void;
  inputValue: string;
  onInputChange: (value: string) => void;
  buttonText: string;
  placeholder: string;
  isLoading: boolean;
  categories?: string[];
  selectedCategory?: string;
  onCategoryChange?: (category: string) => void;
  inputType?: 'text' | 'number';
}

export const JokeForm: React.FC<JokeFormProps> = ({
  onSubmit,
  inputValue,
  onInputChange,
  buttonText,
  placeholder,
  isLoading,
  categories,
  selectedCategory,
  onCategoryChange,
  inputType = 'text'
}) => {
  return (
    <form onSubmit={onSubmit} className="joke-form">
      <input
        type={inputType}
        value={inputValue}
        onChange={(e) => onInputChange(e.target.value)}
        placeholder={placeholder}
        className="joke-input"
      />
      {categories && onCategoryChange && (
        <select
          value={selectedCategory}
          onChange={(e) => onCategoryChange(e.target.value)}
          className="category-select"
        >
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      )}
      <button type="submit" disabled={isLoading} className="joke-button">
        {isLoading ? 'Loading...' : buttonText}
      </button>
    </form>
  );
}; 