import apiClient from './client';

export type Phase1Filters = { period_from: string; period_to: string };

export type Phase1Payload = Record<string, any>;

async function get(path: string, filters: Phase1Filters): Promise<Phase1Payload> {
  const response = await apiClient.get(path, { params: filters });
  return response.data as Phase1Payload;
}

export const phase1DashboardService = {
  pnlPerformance(filters: Phase1Filters) {
    return get('/bi/phase1/pnl-performance', filters);
  },
  workingCapital(filters: Phase1Filters) {
    return get('/bi/phase1/working-capital', filters);
  },
  portfolioHealth(filters: Phase1Filters) {
    return get('/bi/phase1/portfolio-health', filters);
  },
  async export(kind: 'pnl-performance' | 'working-capital' | 'portfolio-health', filters: Phase1Filters, format: 'csv' | 'excel' | 'pdf') {
    return apiClient.get(`/bi/phase1/${kind}/export`, { params: { ...filters, format }, responseType: 'blob' });
  },
};
