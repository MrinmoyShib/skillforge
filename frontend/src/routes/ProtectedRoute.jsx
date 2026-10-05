import { Navigate, Outlet, useLocation } from 'react-router';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function ProtectedRoute({ children }) {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <div className="flex justify-center p-8"><Spinner /></div>;
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />;
  
  return children ? children : <Outlet />;
}
