import React from 'react';
import { cn } from '../lib/utils';

export function ShimmeringText({ children, className, ...props }) {
  return (
    <span
      className={cn(
        "inline-flex animate-shimmer bg-[linear-gradient(110deg,#a1a1aa,45%,#09090b,55%,#a1a1aa)] dark:bg-[linear-gradient(110deg,#71717a,45%,#fafafa,55%,#71717a)] bg-[length:200%_100%] bg-clip-text text-transparent",
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
