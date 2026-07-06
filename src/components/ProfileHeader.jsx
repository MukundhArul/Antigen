import React from 'react';
import { MapPin, Briefcase, Mail } from 'lucide-react';
import { ShimmeringText } from './ShimmeringText';

export default function ProfileHeader() {
  return (
    <section className="flex flex-col gap-4 p-8 border-b border-dashed border-border-primary">
      <div className="w-24 h-24 rounded-full overflow-hidden relative border-2 border-border-primary">
        <img 
          className="w-full h-full object-cover" 
          src="https://images.unsplash.com/photo-1531891437562-4301cf35b7e4?auto=format&fit=crop&q=80&w=256&h=256" 
          alt="Profile Avatar" 
        />
      </div>
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-1 flex items-center gap-2">
          Mukundh Arul
        </h1>
        <div className="mt-2">
          <ShimmeringText className="font-mono text-sm">
            Creating with code. Small details matter.
          </ShimmeringText>
        </div>
        <p className="text-base text-text-secondary leading-relaxed mt-2">
          Full Stack Developer & Design Engineer.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-3 pt-4">
        <div className="flex items-center gap-3 font-mono text-sm text-text-primary">
          <div className="flex items-center justify-center w-8 h-8 rounded-md bg-border-primary/50 text-text-secondary border border-glass-border">
            <Briefcase size={16} />
          </div>
          <span>Software Engineer</span>
        </div>
        <div className="flex items-center gap-3 font-mono text-sm text-text-primary">
          <div className="flex items-center justify-center w-8 h-8 rounded-md bg-border-primary/50 text-text-secondary border border-glass-border">
            <MapPin size={16} />
          </div>
          <span>Earth, Milky Way</span>
        </div>
        <div className="flex items-center gap-3 font-mono text-sm text-text-primary">
          <div className="flex items-center justify-center w-8 h-8 rounded-md bg-border-primary/50 text-text-secondary border border-glass-border">
            <Mail size={16} />
          </div>
          <span>hello@example.com</span>
        </div>
      </div>
    </section>
  );
}
