import React from 'react';
import { FaGithub, FaTwitter, FaLinkedin, FaCodepen, FaCoffee } from 'react-icons/fa';

export default function SocialLinks() {
  const socials = [
    { icon: <FaGithub size={20} />, url: 'https://github.com/MukundhArul', label: 'GitHub' },
    { icon: <FaLinkedin size={20} />, url: '#', label: 'LinkedIn' },
    { icon: <FaTwitter size={20} />, url: '#', label: 'Twitter' },
    { icon: <FaCodepen size={20} />, url: '#', label: 'CodePen' },
    { icon: <FaCoffee size={20} />, url: '#', label: 'Buy me a coffee' },
  ];

  return (
    <section className="flex flex-wrap gap-3 px-8 pb-8">
      {socials.map((social, index) => (
        <a 
          key={index} 
          href={social.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="flex items-center justify-center w-12 h-12 rounded-xl border border-border-primary bg-bg-primary text-text-secondary transition-all duration-200 hover:border-text-primary hover:text-text-primary hover:bg-border-primary hover:-translate-y-0.5"
          aria-label={social.label}
        >
          {social.icon}
        </a>
      ))}
    </section>
  );
}
