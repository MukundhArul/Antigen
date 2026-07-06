import React, { useState, useEffect } from 'react';
import ProfileHeader from './components/ProfileHeader';
import SocialLinks from './components/SocialLinks';
import ThemeToggle from './components/ThemeToggle';

function App() {
  const [theme, setTheme] = useState('dark');

  // On mount, apply the theme class to body
  useEffect(() => {
    document.body.className = theme;
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <div className="app-container">
      <header>
        <div className="header-title text-gradient">Mukundh Arul</div>
        <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
      </header>
      
      <div className="scroll-area">
        <ProfileHeader />
        <div style={{ padding: '24px 24px 8px 24px' }}>
          <h2 style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-secondary)' }}>Connect</h2>
        </div>
        <SocialLinks />
      </div>
    </div>
  );
}

export default App;
