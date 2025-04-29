import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [decks, setDecks] = useState([]);

  useEffect(() => {
    axios.get('/decks')
      .then(response => setDecks(response.data))
      .catch(error => console.error(error));
  }, []);

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

export default Dashboard;
