import { ToastProvider } from './components/feedback/Toast';
import { AuthProvider } from './context/AuthContext';
import AppRoutes from './routes/AppRoutes';
import ErrorBoundary from './components/feedback/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </ToastProvider>
    </ErrorBoundary>
  );
}

export default App;
