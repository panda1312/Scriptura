import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const toggleTheme = async () => {
    const html = document.documentElement;
    const newTheme = html.dataset.theme === 'dark' ? 'light' : 'dark';
    html.dataset.theme = newTheme;
    localStorage.setItem('theme', newTheme);

    const token = localStorage.getItem('token');
    if (token) {
      try {
        await fetch(`${process.env.REACT_APP_API_URL}/users/update-theme`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ theme: newTheme }),
        });
      } catch (error) {
        console.error('Failed to update theme preference:', error);
      }
    }
  };

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.dataset.theme = savedTheme;
  }, []);

  return (
    <nav className="navbar">
      <Link to="/dashboard">Dashboard</Link>
      <button onClick={toggleTheme} style={{ marginLeft: '1rem' }}>
        Toggle Theme
      </button>
    </nav>
  );
};

export default Navbar;
