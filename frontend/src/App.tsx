import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { TenantProvider } from './context/TenantContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/layout/Layout';

import Login from './pages/Login';
import MastersDashboard from './pages/Dashboard/Masters';
import RedFlags from './pages/Dashboard/RedFlags';
import ETLUpload from './pages/ETL/Upload';
import MappingApproval from './pages/ETL/MappingApproval';
import PartyDefaultsPage from './pages/Party/Defaults';
import ReportsList from './pages/Reports/ReportsList';
import ReportBuilder from './pages/Reports/ReportBuilder';
import DashboardList from './pages/Dashboards/DashboardList';
import DashboardView from './pages/Dashboards/DashboardView';
import TrendsView from './pages/Trends/TrendsView';
import RuleManagement from './pages/Alerts/RuleManagement';
import NotificationCenter from './pages/Alerts/NotificationCenter';
import AuditLog from './pages/Alerts/AuditLog';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <TenantProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<MastersDashboard />} />
              <Route path="dashboard/redflags" element={<RedFlags />} />
              <Route path="dashboard/party-defaults" element={<PartyDefaultsPage />} />
              <Route path="reports" element={<ReportsList />} />
              <Route path="reports/new" element={<ReportBuilder />} />
              <Route path="reports/:reportId" element={<ReportBuilder />} />
              <Route path="dashboards" element={<DashboardList />} />
              <Route path="dashboards/:dashboardId" element={<DashboardView />} />
              <Route path="trends" element={<TrendsView />} />
              <Route path="alerts/rules" element={<RuleManagement />} />
              <Route path="alerts/notifications" element={<NotificationCenter />} />
              <Route path="alerts/audit" element={<AuditLog />} />
              <Route path="masters/etl/upload" element={<ETLUpload />} />
              <Route path="etl/mapping/:batchGuid" element={<MappingApproval />} />
            </Route>
          </Routes>
        </TenantProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
