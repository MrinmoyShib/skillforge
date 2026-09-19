const SIZES = {
  sm: 'h-4 w-4 border-2',
  md: 'h-8 w-8 border-4',
  lg: 'h-12 w-12 border-4',
};

export default function Spinner({ size = 'md', className = '' }) {
  const sizeClasses = SIZES[size] || SIZES.md;
  return (
    <div className={`${sizeClasses} inline-block animate-spin rounded-full border-solid border-[var(--color-brand-primary)] border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite] ${className}`} role="status">
      <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">Loading...</span>
    </div>
  );
}
