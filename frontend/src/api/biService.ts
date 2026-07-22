import apiClient from './client';

export type ReportDefinition = {
  report_id?: number;
  name: string;
  description?: string;
  category: string;
  output_format: string;
  definition: {
    source: string;
    dimensions: string[];
    metrics: Array<{ field: string; aggregation: string; alias: string }>;
    filters: Array<{ field: string; operator: string; value: unknown }>;
    order_by?: Array<{ field: string; direction: string }>;
    limit?: number;
  };
  is_scheduled?: boolean;
  schedule_config?: { frequency: string; day?: string | number; time: string; recipients: string[] };
  is_public?: boolean;
};

export const biService = {
  async listReports() {
    const response = await apiClient.get('/bi/reports/');
    return response.data as Array<Record<string, unknown>>;
  },

  async getReport(reportId: number) {
    const response = await apiClient.get(`/bi/reports/${reportId}`);
    return response.data as Record<string, unknown>;
  },

  async createReport(payload: ReportDefinition) {
    const response = await apiClient.post('/bi/reports/', payload);
    return response.data as Record<string, unknown>;
  },

  async updateReport(reportId: number, payload: Partial<ReportDefinition>) {
    const response = await apiClient.put(`/bi/reports/${reportId}`, payload);
    return response.data as Record<string, unknown>;
  },

  async deleteReport(reportId: number) {
    const response = await apiClient.delete(`/bi/reports/${reportId}`);
    return response.data as Record<string, unknown>;
  },

  async executeReport(reportId: number) {
    const response = await apiClient.post(`/bi/reports/${reportId}/execute`);
    return response.data as { columns: string[]; data: Array<Record<string, unknown>> };
  },

  async exportReport(reportId: number, format: 'pdf' | 'excel' | 'csv' | 'html') {
    const response = await apiClient.get(`/bi/reports/${reportId}/export/${format}`, { responseType: 'blob' });
    return response;
  },

  async scheduleReport(reportId: number, schedule: { frequency: string; day?: string | number; time: string; recipients: string[] }) {
    const response = await apiClient.post(`/bi/reports/${reportId}/schedule`, schedule);
    return response.data;
  },

  async listDashboards() {
    const response = await apiClient.get('/bi/dashboards/');
    return response.data as Array<Record<string, unknown>>;
  },

  async createDashboard(payload: { name: string; description?: string; layout?: Record<string, unknown> }) {
    const response = await apiClient.post('/bi/dashboards/', payload);
    return response.data as Record<string, unknown>;
  },

  async getDashboard(dashboardId: number) {
    const response = await apiClient.get(`/bi/dashboards/${dashboardId}`);
    return response.data as Record<string, unknown>;
  },

  async deleteDashboard(dashboardId: number) {
    const response = await apiClient.delete(`/bi/dashboards/${dashboardId}`);
    return response.data as Record<string, unknown>;
  },

  async addWidget(dashboardId: number, payload: Record<string, unknown>) {
    const response = await apiClient.post(`/bi/dashboards/${dashboardId}/widgets`, payload);
    return response.data as Record<string, unknown>;
  },

  async executeWidget(dashboardId: number, widgetId: number) {
    const response = await apiClient.post(`/bi/dashboards/${dashboardId}/widgets/${widgetId}/execute`);
    return response.data as { columns: string[]; data: Array<Record<string, unknown>> };
  },

  async getTrend(metric: string, days = 30) {
    const response = await apiClient.get(`/bi/trends/${metric}?days=${days}`);
    return response.data as { metric: string; days: number; data: Array<{ date: string; count: number }> };
  },

  async getTrendSummary() {
    const response = await apiClient.get('/bi/trends/summary');
    return response.data as Record<string, { data: Array<{ date: string; count: number }> }>;
  },
};
