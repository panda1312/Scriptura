import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const toggleTheme = () => {
    const html = document.documentElement;
    html.dataset.theme = html.dataset.theme === 'dark' ? 'light' : 'dark';
  };

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
