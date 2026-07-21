import apiClient from '../api/client';

export interface User {
  user_id: number;
  username: string;
  email?: string;
  full_name?: string;
  company_id: number;
  roles: string[];
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

export interface Company {
  company_id: number;
  company_code: string;
  company_name: string;
}

export const authService = {
  async login(username: string, password: string): Promise<LoginResponse> {
    const response = await apiClient.post('/auth/login', { username, password });
    return response.data;
  },

  async refresh(refreshToken: string): Promise<LoginResponse> {
    const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  },

  async logout(refreshToken?: string): Promise<void> {
    await apiClient.post('/auth/logout', refreshToken ? { refresh_token: refreshToken } : {});
  },

  async me(): Promise<User> {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  async companies(): Promise<Company[]> {
    const response = await apiClient.get('/auth/companies');
    return response.data;
  },
};
