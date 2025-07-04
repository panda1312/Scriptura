import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import './styles/theme.css';
import './styles/dark-theme.css'; // this should come after theme.css
import './styles/global.css';
import './index.css';
import './components/Navbar.css';


function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

export default App;
