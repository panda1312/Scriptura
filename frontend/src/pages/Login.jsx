import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/users/login`,
        params,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      // Store the access token in localStorage
      localStorage.setItem('token', response.data.access_token);

      // Store the theme preference (from response) in localStorage
      if (response.data.theme) {
        localStorage.setItem('theme', response.data.theme);  // Store theme
        document.documentElement.setAttribute('data-theme', response.data.theme);  // Apply theme immediately
      }

      navigate('/dashboard');
    } catch (error) {
      alert('Login failed.');
    }
  };

  return (
    <div>
      <h2>Login to Scriptura</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
