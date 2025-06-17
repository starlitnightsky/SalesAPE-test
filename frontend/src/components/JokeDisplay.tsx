import React from 'react';
import { JokeResponse } from '../types/joke';

interface JokeDisplayProps {
  joke: JokeResponse;
}

export const JokeDisplay: React.FC<JokeDisplayProps> = ({ joke }) => {
  return (
    <div className="joke-container">
      <div className="joke-category">Category: {joke.category}</div>
      {joke.setup && joke.delivery ? (
        <>
          <p className="joke-setup">{joke.setup}</p>
          <p className="joke-delivery">{joke.delivery}</p>
        </>
      ) : (
        <p className="joke-text">{joke.joke}</p>
      )}
    </div>
  );
}; 