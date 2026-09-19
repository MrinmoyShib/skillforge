import React, { Suspense } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router';
import AppLayout from '../components/layout/AppLayout';
import ProtectedRoute from './ProtectedRoute';
import AdminRoute from './AdminRoute';
import AdminLayout from '../components/layout/AdminLayout';
import Spinner from '../components/feedback/Spinner';

// Student Pages
const HomePage = React.lazy(() => import('../pages/HomePage'));
const LoginPage = React.lazy(() => import('../pages/LoginPage'));
const RegisterPage = React.lazy(() => import('../pages/RegisterPage'));
const DashboardPage = React.lazy(() => import('../pages/DashboardPage'));
const ProblemsPage = React.lazy(() => import('../pages/ProblemsPage'));
const ProblemDetailPage = React.lazy(() => import('../pages/ProblemDetailPage'));
const ProjectsPage = React.lazy(() => import('../pages/ProjectsPage'));
const ProjectWorkspacePage = React.lazy(() => import('../pages/ProjectWorkspacePage'));
const PortfolioPage = React.lazy(() => import('../pages/PortfolioPage'));
const LeaderboardPage = React.lazy(() => import('../pages/LeaderboardPage'));
const AchievementsPage = React.lazy(() => import('../pages/AchievementsPage'));
const SettingsPage = React.lazy(() => import('../pages/SettingsPage'));
const NotFoundPage = React.lazy(() => import('../pages/NotFoundPage'));

// Admin Studio Pages
const AdminDashboardPage = React.lazy(() => import('../pages/admin/AdminDashboardPage'));
const AdminProblemsPage = React.lazy(() => import('../pages/admin/AdminProblemsPage'));
const AdminProjectsPage = React.lazy(() => import('../pages/admin/AdminProjectsPage'));
const AdminUsersPage = React.lazy(() => import('../pages/admin/AdminUsersPage'));
const AdminSubmissionsPage = React.lazy(() => import('../pages/admin/AdminSubmissionsPage'));

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
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center bg-[#0b0f19]"><Spinner size="lg" /></div>}>
      <RouterProvider router={router} />
    </Suspense>
  );
}
