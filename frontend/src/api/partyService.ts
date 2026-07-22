import apiClient from './client';

export type PartyDefaultsRecord = {
  id: number;
  type: 'LENDER' | 'CONNECTOR';
  name: string;
  default_gst_rate: number;
  default_tds_rate: number;
  max_commission: number | null;
};

export const partyService = {
  async getLenders() {
    const response = await apiClient.get('/masters/lenders/');
    return response.data as Array<Record<string, unknown>>;
  },

  async getConnectors() {
    const response = await apiClient.get('/masters/connectors/');
    return response.data as Array<Record<string, unknown>>;
  },

  async updateLender(lenderId: number, payload: { default_gst_rate: number; default_tds_rate: number; max_commission: number | null }) {
    const response = await apiClient.put(`/masters/lenders/${lenderId}`, payload);
    return response.data;
  },

  async updateConnector(connectorId: number, payload: { default_gst_rate: number; default_tds_rate: number; max_commission: number | null }) {
    const response = await apiClient.put(`/masters/connectors/${connectorId}`, payload);
    return response.data;
  },
};
