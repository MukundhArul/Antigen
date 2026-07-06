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
    <section className="social-grid">
      {socials.map((social, index) => (
        <a 
          key={index} 
          href={social.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="social-button"
          aria-label={social.label}
        >
          {social.icon}
        </a>
      ))}
    </section>
  );
}
