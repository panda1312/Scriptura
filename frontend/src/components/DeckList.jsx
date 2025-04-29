import React from 'react';

const DeckList = ({ decks }) => {
  return (
    <div>
      <h2>Your Decks</h2>
      <ul>
        {decks.map(deck => (
          <li key={deck.id}>{deck.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default DeckList;
