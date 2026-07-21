import apiClient from './client';

export type UploadResult = {
  status: 'success' | 'mapping_required' | 'upload_failed' | 'validation_failed' | 'promotion_failed' | 'staged';
  mode?: 'strict_template' | 'dynamic_mapping';
  batch_guid?: string;
  message?: string;
  proposal?: unknown;
  upload?: unknown;
  promotion?: unknown;
  detail?: unknown;
  file_name?: string;
  entity_type?: string;
};

export type MappingColumn = {
  source_column: string;
  suggested_target_table?: string;
  suggested_target_field?: string;
  confidence_score?: number;
  ignore?: boolean;
  notes?: string;
};

type MappingTemplatePayload = {
  template_name: string;
  file_pattern?: string;
  fingerprint?: string;
  sheet_name: string;
  header_row: number;
  mappings: Array<{
    source_column: string;
    target_table: string;
    target_field: string;
    confidence_score: number;
    is_verified: boolean;
    is_natural_key: boolean;
    transformation_rule: string | null;
    notes: string | null;
  }>;
  conflict_resolution: string;
  version?: number;
  status?: string;
  shared?: boolean;
  company_id?: number;
};

export const etlService = {
  async uploadFile(file: File, entityType: string): Promise<UploadResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('entity_type', entityType);
    formData.append('auto_process', 'true');

    const response = await apiClient.post('/v1/etl/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      validateStatus: () => true,
    });

    if (response.status >= 200 && response.status < 300) {
      return response.data;
    }
    return response.data as UploadResult;
  },

  async getStaging(batchGuid: string) {
    const response = await apiClient.get(`/v1/etl/staging?batch_guid=${encodeURIComponent(batchGuid)}`);
    return response.data;
  },

  async getErrors(batchGuid: string) {
    const response = await apiClient.get(`/v1/etl/errors?batch_guid=${encodeURIComponent(batchGuid)}`);
    return response.data;
  },

  async promoteBatch(batchGuid: string, conflictResolution = 'SKIP') {
    const formData = new FormData();
    formData.append('batch_guid', batchGuid);
    formData.append('conflict_resolution', conflictResolution);
    const response = await apiClient.post('/v1/etl/promote', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  async detectTemplate(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/v1/etl/template/detect', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  async saveTemplateDraft(payload: MappingTemplatePayload) {
    const response = await apiClient.post('/admin/mapping/templates/draft', payload);
    return response.data;
  },

  async submitTemplate(templateId: number) {
    const response = await apiClient.post(`/admin/mapping/templates/${templateId}/submit`);
    return response.data;
  },

  async activateTemplate(templateId: number) {
    const response = await apiClient.post(`/admin/mapping/templates/${templateId}/activate`);
    return response.data;
  },
};
