import { useEffect, useMemo, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { etlService } from '../../api/etlService';
import { useAuth } from '../../context/AuthContext';

type ProposalColumn = {
  source_column: string;
  suggested_target_table?: string;
  suggested_target_field?: string;
  confidence_score?: number;
  ignore?: boolean;
  notes?: string;
};

export default function MappingApproval() {
  const { batchGuid } = useParams();
  const location = useLocation();
  const { user } = useAuth();
  const incoming = (location.state as { proposal?: any } | null)?.proposal;
  const incomingFileName = (location.state as { fileName?: string } | null)?.fileName;

  const [columns, setColumns] = useState<ProposalColumn[]>([]);
  const [templateName, setTemplateName] = useState(() => {
    const fallback = incomingFileName || batchGuid || 'Hybrid_Template';
    return `Draft_${String(fallback).replace(/[^a-zA-Z0-9_\-\.]/g, '_')}`;
  });
  const [templateId, setTemplateId] = useState<number | null>(null);
  const [message, setMessage] = useState<string>('');
  const [isBusy, setIsBusy] = useState(false);

  useEffect(() => {
    const sheetColumns = incoming?.sheets?.[0]?.columns || [];
    setColumns(sheetColumns);
  }, [incoming]);

  const highConfidence = useMemo(() => columns.filter((c) => (c.confidence_score || 0) >= 80).length, [columns]);

  const approvedCount = useMemo(
    () => columns.filter((c) => !c.ignore && !!c.suggested_target_table && !!c.suggested_target_field).length,
    [columns]
  );

  const setField = (index: number, key: keyof ProposalColumn, value: string | boolean) => {
    setColumns((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], [key]: value };
      return next;
    });
  };

  const approveHighConfidence = () => {
    setColumns((prev) =>
      prev.map((col) => ({
        ...col,
        ignore: (col.confidence_score || 0) >= 80 ? false : col.ignore,
      }))
    );
  };

  const buildTemplatePayload = () => {
    const sheet = incoming?.sheets?.[0] || {};
    const preparedMappings = columns
      .filter((c) => !c.ignore && c.suggested_target_table && c.suggested_target_field)
      .map((c) => ({
        source_column: c.source_column,
        target_table: c.suggested_target_table || '',
        target_field: c.suggested_target_field || '',
        confidence_score: c.confidence_score || 0,
        is_verified: true,
        is_natural_key: false,
        transformation_rule: null,
        notes: c.notes || null,
      }));

    return {
      template_name: templateName,
      file_pattern: incomingFileName || batchGuid || templateName,
      fingerprint: sheet.fingerprint || incoming?.workbook_fingerprint || null,
      sheet_name: sheet.sheet_name || 'Sheet1',
      header_row: sheet.header_row || 1,
      mappings: preparedMappings,
      conflict_resolution: 'SKIP',
      status: 'Draft',
    };
  };

  const onSaveDraft = async () => {
    setIsBusy(true);
    setMessage('');
    try {
      const payload = buildTemplatePayload();
      if (!payload.mappings.length) {
        setMessage('Add at least one valid mapping before saving draft.');
        return;
      }
      const saved = await etlService.saveTemplateDraft(payload);
      setTemplateId(saved.template_id);
      setMessage(`Draft saved (Template ID: ${saved.template_id}).`);
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'Failed to save draft.');
    } finally {
      setIsBusy(false);
    }
  };

  const onSubmitForApproval = async () => {
    if (!templateId) {
      setMessage('Save draft first, then submit for approval.');
      return;
    }
    setIsBusy(true);
    setMessage('');
    try {
      await etlService.submitTemplate(templateId);
      setMessage('Template submitted for approval (status: Approved).');
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'Failed to submit template.');
    } finally {
      setIsBusy(false);
    }
  };

  const onActivateTemplate = async () => {
    if (!templateId) {
      setMessage('Save draft first to get a template ID.');
      return;
    }
    setIsBusy(true);
    setMessage('');
    try {
      await etlService.activateTemplate(templateId);
      setMessage('Template activated (status: Active).');
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'Activation failed.');
    } finally {
      setIsBusy(false);
    }
  };

  return (
    <div className="space-y-4 max-w-6xl">
      <h2 className="text-2xl font-bold text-brand-ink">Mapping Approval</h2>
      <p className="text-sm text-brand-deep/70">Batch: {batchGuid}</p>
      <p className="text-sm text-brand-deep/70">High confidence suggestions: {highConfidence}</p>
      <p className="text-sm text-brand-deep/70">Approved mappings ready: {approvedCount}</p>

      <div className="rounded-xl border border-brand-deep/10 bg-white p-4 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="md:col-span-2">
          <label className="block text-xs uppercase tracking-wide text-brand-deep/70">Template Name</label>
          <input
            value={templateName}
            onChange={(e) => setTemplateName(e.target.value)}
            className="mt-1 w-full rounded border border-brand-deep/20 px-3 py-2"
          />
        </div>
        <div>
          <label className="block text-xs uppercase tracking-wide text-brand-deep/70">Status</label>
          <div className="mt-1 rounded border border-brand-deep/20 px-3 py-2 bg-brand-sand text-sm">
            {templateId ? `Draft Saved (ID ${templateId})` : 'Unsaved Draft'}
          </div>
        </div>
      </div>

      <div className="overflow-auto rounded-xl border border-brand-deep/10 bg-white">
        <table className="min-w-full text-sm">
          <thead className="bg-brand-sand">
            <tr>
              <th className="text-left p-3">Source</th>
              <th className="text-left p-3">Target Table</th>
              <th className="text-left p-3">Target Field</th>
              <th className="text-left p-3">Confidence</th>
              <th className="text-left p-3">Ignore</th>
            </tr>
          </thead>
          <tbody>
            {columns.map((col, idx) => (
              <tr key={`${col.source_column}-${idx}`} className="border-t border-brand-deep/10">
                <td className="p-3">{col.source_column}</td>
                <td className="p-3">
                  <input
                    value={col.suggested_target_table || ''}
                    onChange={(e) => setField(idx, 'suggested_target_table', e.target.value)}
                    className="w-full rounded border border-brand-deep/20 px-2 py-1"
                  />
                </td>
                <td className="p-3">
                  <input
                    value={col.suggested_target_field || ''}
                    onChange={(e) => setField(idx, 'suggested_target_field', e.target.value)}
                    className="w-full rounded border border-brand-deep/20 px-2 py-1"
                  />
                </td>
                <td className="p-3">{col.confidence_score || 0}%</td>
                <td className="p-3">
                  <input
                    type="checkbox"
                    checked={!!col.ignore}
                    onChange={(e) => setField(idx, 'ignore', e.target.checked)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          onClick={approveHighConfidence}
          disabled={isBusy}
          className="rounded bg-brand-sand border border-brand-deep/20 px-3 py-2 text-sm"
        >
          Approve All High Confidence
        </button>
        <button
          onClick={onSaveDraft}
          disabled={isBusy}
          className="rounded bg-brand-deep px-3 py-2 text-sm text-white disabled:opacity-50"
        >
          Save as Draft
        </button>
        <button
          onClick={onSubmitForApproval}
          disabled={isBusy || !templateId}
          className="rounded bg-brand-mint px-3 py-2 text-sm text-white disabled:opacity-50"
        >
          Submit for Approval
        </button>
        {user?.roles?.includes('ADMIN') && (
          <button
            onClick={onActivateTemplate}
            disabled={isBusy || !templateId}
            className="rounded bg-emerald-700 px-3 py-2 text-sm text-white disabled:opacity-50"
          >
            Activate Template
          </button>
        )}
      </div>

      <div className="rounded-xl border border-brand-deep/10 bg-white p-4 text-sm text-brand-deep/70">
        {message || 'Review mappings, save draft, submit for approval, and activate (admin only).'}
      </div>
    </div>
  );
}
