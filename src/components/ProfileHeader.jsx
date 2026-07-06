import React from 'react';
import { MapPin, Briefcase, Mail } from 'lucide-react';

export default function ProfileHeader() {
  return (
    <section className="profile-section">
      <div className="avatar-container">
        {/* Placeholder image from unsplash for a clean look */}
        <img 
          className="avatar-image" 
          src="https://images.unsplash.com/photo-1531891437562-4301cf35b7e4?auto=format&fit=crop&q=80&w=256&h=256" 
          alt="Profile Avatar" 
        />
      </div>
      <div>
        <h1 className="profile-name">
          Mukundh Arul
        </h1>
        <p className="profile-bio">
          Creating with code. Small details matter. <br />
          Full Stack Developer & Design Engineer.
        </p>
      </div>

      <div className="info-grid">
        <div className="info-item">
          <div className="info-icon-wrapper">
            <Briefcase size={16} />
          </div>
          <span>Software Engineer</span>
        </div>
        <div className="info-item">
          <div className="info-icon-wrapper">
            <MapPin size={16} />
          </div>
          <span>Earth, Milky Way</span>
        </div>
        <div className="info-item">
          <div className="info-icon-wrapper">
            <Mail size={16} />
          </div>
          <span>hello@example.com</span>
        </div>
      </div>
    </section>
  );
}
