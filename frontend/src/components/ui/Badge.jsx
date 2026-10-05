import React from 'react';

export function Badge({
  children,
  variant = 'default',
  size = 'md',
  className = '',
  ...props
}) {
  const baseClasses = 'inline-flex items-center font-semibold rounded-md uppercase tracking-wider font-mono';

  const variants = {
    default: 'bg-slate-800 text-slate-300 border border-slate-700',
    easy: 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/50',
    medium: 'bg-amber-950/60 text-amber-400 border border-amber-800/50',
    hard: 'bg-rose-950/60 text-rose-400 border border-rose-800/50',
    info: 'bg-indigo-950/60 text-indigo-400 border border-indigo-800/50',
    success: 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/50',
    warning: 'bg-amber-950/60 text-amber-400 border border-amber-800/50',
    danger: 'bg-rose-950/60 text-rose-400 border border-rose-800/50',
  };

  const sizes = {
    sm: 'text-[10px] px-1.5 py-0.5',
    md: 'text-[11px] px-2 py-0.5',
    lg: 'text-xs px-2.5 py-1',
  };

  return (
    <span
      className={`${baseClasses} ${variants[variant] || variants.default} ${sizes[size] || sizes.md} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}

export default Badge;

