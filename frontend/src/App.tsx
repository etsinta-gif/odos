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
              <Route path="masters/etl/upload" element={<ETLUpload />} />
              <Route path="etl/mapping/:batchGuid" element={<MappingApproval />} />
            </Route>
          </Routes>
        </TenantProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
