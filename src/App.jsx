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
    <div className="w-full h-screen max-w-[500px] sm:max-h-[888px] relative bg-bg-primary flex flex-col sm:border sm:border-border-primary sm:rounded-3xl sm:shadow-2xl sm:overflow-hidden transition-all duration-300">
      <header className="px-6 py-4 flex justify-between items-center border-b border-border-primary sticky top-0 bg-card-bg backdrop-blur-md z-50">
        <div className="font-semibold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-text-primary to-text-secondary">
          Mukundh Arul
        </div>
        <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
      </header>
      
      <div className="flex-1 overflow-y-auto overflow-x-hidden no-scrollbar">
        <ProfileHeader />
        <div className="px-8 pt-6 pb-2">
          <h2 className="text-sm uppercase tracking-widest text-text-secondary font-mono">Connect</h2>
        </div>
        <SocialLinks />
      </div>
    </div>
  );
}

export default App;
