import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import '../styles/card.css';  // Assuming card styles are in styles folder
import '../styles/button.css';

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
    <>
      <Navbar />
      <main style={{ padding: 'var(--spacing-lg)' }}>
        <h2 className="hig-heading" style={{ marginBottom: 'var(--spacing-md)' }}>
          Your Decks
        </h2>
        <div style={{ display: 'grid', gap: 'var(--spacing-md)' }}>
          {decks.length > 0 ? (
            decks.map(deck => (
              <div key={deck.id} className="hig-card">
                <h3 style={{ marginBottom: 'var(--spacing-sm)' }}>{deck.name}</h3>
                <button className="hig-button">Review</button>
              </div>
            ))
          ) : (
            <p style={{ color: 'var(--color-muted)' }}>No decks found.</p>
          )}
        </div>
      </main>
    </>
  );
};

export default Dashboard;
