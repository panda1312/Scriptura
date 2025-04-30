import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const toggleTheme = () => {
    const html = document.documentElement;
    const newTheme = html.dataset.theme === 'dark' ? 'light' : 'dark';
    html.dataset.theme = newTheme;
    localStorage.setItem('theme', newTheme);
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
