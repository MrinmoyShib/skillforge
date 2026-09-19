import { createBrowserRouter, RouterProvider } from 'react-router';
import AppLayout from '../components/layout/AppLayout';
import ProtectedRoute from './ProtectedRoute';
import AdminRoute from './AdminRoute';
import AdminLayout from '../components/layout/AdminLayout';

// Student Pages
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import DashboardPage from '../pages/DashboardPage';
import ProblemsPage from '../pages/ProblemsPage';
import ProblemDetailPage from '../pages/ProblemDetailPage';
import ProjectsPage from '../pages/ProjectsPage';
import ProjectWorkspacePage from '../pages/ProjectWorkspacePage';
import PortfolioPage from '../pages/PortfolioPage';
import LeaderboardPage from '../pages/LeaderboardPage';
import AchievementsPage from '../pages/AchievementsPage';
import SettingsPage from '../pages/SettingsPage';
import NotFoundPage from '../pages/NotFoundPage';

// Admin Studio Pages
import AdminDashboardPage from '../pages/admin/AdminDashboardPage';
import AdminProblemsPage from '../pages/admin/AdminProblemsPage';
import AdminProjectsPage from '../pages/admin/AdminProjectsPage';
import AdminUsersPage from '../pages/admin/AdminUsersPage';
import AdminSubmissionsPage from '../pages/admin/AdminSubmissionsPage';

const router = createBrowserRouter([
  // Main Student Platform Routes
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "login", element: <LoginPage /> },
      { path: "register", element: <RegisterPage /> },
      { path: "problems", element: <ProblemsPage /> },
      { path: "problems/:slug", element: <ProblemDetailPage /> },
      { path: "projects", element: <ProjectsPage /> },
      { path: "projects/:slug", element: <ProjectWorkspacePage /> },
      { path: "portfolio/:username", element: <PortfolioPage /> },
      { path: "leaderboard", element: <LeaderboardPage /> },
      { path: "achievements", element: <AchievementsPage /> },
      {
        path: "dashboard",
        element: (
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        )
      },
      {
        path: "settings",
        element: (
          <ProtectedRoute>
            <SettingsPage />
          </ProtectedRoute>
        )
      },
      { path: "*", element: <NotFoundPage /> }
    ]
  },

  // Enterprise Admin Command Center Routes (Staff Only)
  {
    path: "/admin",
    element: (
      <AdminRoute>
        <AdminLayout />
      </AdminRoute>
    ),
    children: [
      { index: true, element: <AdminDashboardPage /> },
      { path: "problems", element: <AdminProblemsPage /> },
      { path: "projects", element: <AdminProjectsPage /> },
      { path: "users", element: <AdminUsersPage /> },
      { path: "submissions", element: <AdminSubmissionsPage /> },
    ]
  }
]);

export default function AppRoutes() {
  return <RouterProvider router={router} />;
}
