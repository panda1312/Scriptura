// frontend/src/components/Navbar.jsx
import './Navbar.css';

export default function Navbar() {
  const toggleTheme = () => {
    const html = document.documentElement;
    html.dataset.theme = html.dataset.theme === 'dark' ? 'light' : 'dark';
  };

  return (
    <nav className="hig-navbar">
      <div className="hig-navbar-title">Scriptura</div>
      <button className="hig-theme-toggle" onClick={toggleTheme}>
        Toggle Theme
      </button>
    </nav>
  );
}
