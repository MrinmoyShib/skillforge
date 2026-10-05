import React, { forwardRef } from 'react';

export const Input = forwardRef(({
  label,
  error,
  helperText,
  className = '',
  id,
  type = 'text',
  ...props
}, ref) => {
  const inputId = id || props.name || Math.random().toString(36).substring(7);

  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wider">
          {label}
        </label>
      )}
      <input
        ref={ref}
        id={inputId}
        type={type}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
        className={`w-full px-3.5 py-2.5 bg-slate-900/80 border rounded-xl text-white placeholder-slate-500 text-sm transition-all focus:outline-none focus:ring-2 ${
          error
            ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20'
            : 'border-slate-800 focus:border-cyan-500 focus:ring-cyan-500/20'
        } ${className}`}
        {...props}
      />
      {error && (
        <p id={`${inputId}-error`} className="mt-1.5 text-xs text-red-400 font-medium">
          {error}
        </p>
      )}
      {!error && helperText && (
        <p id={`${inputId}-helper`} className="mt-1.5 text-xs text-slate-400">
          {helperText}
        </p>
      )}
    </div>
  );
});

Input.displayName = 'Input';

