import apiClient from './client';

export type AlertRecord = {
  red_flag_id: number;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  category: string;
  message: string;
  status: 'OPEN' | 'RESOLVED' | 'IGNORED';
  record_type: string;
  record_id: number;
  field?: string | null;
  reported_value?: string | null;
  expected_value?: string | null;
  resolution_notes?: string | null;
  created_at?: string;
  resolved_at?: string | null;
};

export type AlertSummary = {
  total: number;
  by_status: Record<string, number>;
  by_severity: Record<string, number>;
  by_category: Record<string, number>;
};

export type AlertRule = {
  rule_id: number;
  name: string;
  description?: string | null;
  category: string;
  conditions: Record<string, unknown>;
  actions: Array<Record<string, unknown>>;
  escalation_policy_id?: number | null;
  priority: number;
  is_active: boolean;
  created_at?: string;
};

export type AlertNotification = {
  notification_id: number;
  type: 'EMAIL' | 'IN_APP' | 'WEBHOOK';
  subject: string;
  content: string;
  sent_at?: string;
  read: boolean;
  delivered: boolean;
  error_message?: string | null;
};

export type AlertAuditLog = {
  log_id: number;
  action: string;
  details?: Record<string, unknown> | null;
  performed_at?: string;
};

export type EscalationPolicy = {
  policy_id: number;
  name: string;
  description?: string | null;
  levels: Array<Record<string, unknown>>;
  default_assignee_role?: string | null;
  is_active: boolean;
};

export const alertsService = {
  async list(params?: { status?: string; severity?: string; category?: string; limit?: number }) {
    const response = await apiClient.get('/alerts/red-flags', { params });
    return response.data as { total_records: number; records: AlertRecord[] };
  },

  async summary() {
    const response = await apiClient.get('/alerts/red-flags/summary');
    return response.data as AlertSummary;
  },

  async resolve(redFlagId: number, resolutionNotes?: string) {
    const response = await apiClient.put(`/alerts/red-flags/${redFlagId}/resolve`, {
      status: 'RESOLVED',
      resolution_notes: resolutionNotes,
    });
    return response.data;
  },

  async ignore(redFlagId: number, resolutionNotes?: string) {
    const response = await apiClient.put(`/alerts/red-flags/${redFlagId}/ignore`, {
      status: 'IGNORED',
      resolution_notes: resolutionNotes,
    });
    return response.data;
  },

  async listRules(params?: { category?: string; is_active?: boolean }) {
    const response = await apiClient.get('/alerts/rules', { params });
    return response.data as AlertRule[];
  },

  async getRule(ruleId: number) {
    const response = await apiClient.get(`/alerts/rules/${ruleId}`);
    return response.data as AlertRule;
  },

  async createRule(payload: {
    name: string;
    description?: string;
    category: string;
    conditions: Record<string, unknown>;
    actions: Array<Record<string, unknown>>;
    escalation_policy_id?: number;
    priority: number;
  }) {
    const response = await apiClient.post('/alerts/rules', payload);
    return response.data as { rule_id: number; message: string };
  },

  async updateRule(ruleId: number, payload: Record<string, unknown>) {
    const response = await apiClient.put(`/alerts/rules/${ruleId}`, payload);
    return response.data as { message: string };
  },

  async deleteRule(ruleId: number) {
    const response = await apiClient.delete(`/alerts/rules/${ruleId}`);
    return response.data as { message: string };
  },

  async testRule(ruleId: number, redFlagId: number) {
    const response = await apiClient.post(`/alerts/rules/${ruleId}/test`, { red_flag_id: redFlagId });
    return response.data as { triggered: boolean; actions: Array<Record<string, unknown>> };
  },

  async listEscalationPolicies() {
    const response = await apiClient.get('/alerts/escalation-policies');
    return response.data as EscalationPolicy[];
  },

  async createEscalationPolicy(payload: {
    name: string;
    description?: string;
    levels: Array<Record<string, unknown>>;
    default_assignee_role?: string;
  }) {
    const response = await apiClient.post('/alerts/escalation-policies', payload);
    return response.data as { policy_id: number; message: string };
  },

  async listNotifications(params?: { limit?: number; read?: boolean }) {
    const response = await apiClient.get('/alerts/notifications', { params });
    return response.data as AlertNotification[];
  },

  async markNotificationRead(notificationId: number) {
    const response = await apiClient.put(`/alerts/notifications/${notificationId}/read`);
    return response.data as { message: string };
  },

  async listAuditLogs(params?: { limit?: number; action?: string; red_flag_id?: number }) {
    const response = await apiClient.get('/alerts/audit', { params });
    return response.data as AlertAuditLog[];
  },

  async runAutoResolve() {
    const response = await apiClient.post('/alerts/automation/auto-resolve');
    return response.data as { resolved: number; red_flag_ids: number[] };
  },

  async checkEscalations() {
    const response = await apiClient.post('/alerts/automation/check-escalations');
    return response.data as { escalated: number; details: Array<Record<string, unknown>> };
  },
};
