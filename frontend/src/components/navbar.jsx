import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

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
    <nav className="hig-navbar">
      <div className="hig-navbar-title">Scriptura</div>
      <div>
        <Link to="/dashboard" className="hig-nav-link">Dashboard</Link>
        <button className="hig-theme-toggle" onClick={toggleTheme}>
          Toggle Theme
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
