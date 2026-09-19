import { Link } from 'react-router';

export default function NotFoundPage() {
  return (
    <div className="flex flex-col items-center py-20">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="text-[var(--color-text-secondary)] mb-8">The page you are looking for does not exist.</p>
      <Link to="/" className="text-[var(--color-brand-primary)] hover:underline">Go Home</Link>
    </div>
  );
}
