import { Navigate, Outlet } from 'react-router';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <div className="flex justify-center p-8"><Spinner /></div>;
  if (!user) return <Navigate to="/login" replace />;
  
  return children ? children : <Outlet />;
}
