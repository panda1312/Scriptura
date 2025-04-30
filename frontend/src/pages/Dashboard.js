import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';

const Dashboard = () => {
  const [decks, setDecks] = useState([]);

  useEffect(() => {
    const fetchDecks = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/decks`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setDecks(response.data);
      } catch (error) {
        console.error('Failed to fetch decks:', error);
      }
    };

    fetchDecks();
  }, []);

  return (
    <div>
      <Navbar />
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
