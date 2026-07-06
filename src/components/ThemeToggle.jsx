import React from 'react';
import { Moon, Sun } from 'lucide-react';

export default function ThemeToggle({ theme, toggleTheme }) {
  return (
    <button 
      className="flex items-center justify-center w-9 h-9 rounded-lg text-text-primary transition-all duration-200 hover:bg-border-primary active:scale-95" 
      onClick={toggleTheme} 
      aria-label="Toggle mode"
    >
      {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );
}
