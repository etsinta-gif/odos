import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { biService, type ReportDefinition } from '../../api/biService';

const SOURCES = ['TRN_Revenue', 'TRN_Commission', 'TRN_Payment', 'ETL_RedFlag', 'MST_Party'];
const AGGREGATIONS = ['sum', 'avg', 'count', 'min', 'max'];
const OPERATORS = ['eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'in', 'like', 'is_null', 'is_not_null'];

export default function ReportBuilder() {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const [preview, setPreview] = useState<{ columns: string[]; data: Array<Record<string, unknown>> } | null>(null);
  const [report, setReport] = useState<ReportDefinition>({
    name: '',
    description: '',
    category: 'Custom',
    output_format: 'HTML',
    definition: {
      source: 'TRN_Revenue',
      dimensions: [],
      metrics: [],
      filters: [],
      order_by: [],
      limit: 100,
    },
    is_scheduled: false,
    schedule_config: { frequency: 'daily', time: '09:00', recipients: [] },
    is_public: false,
  });

  useEffect(() => {
    const load = async () => {
      if (!reportId || reportId === 'new') {
        return;
      }
      const data = await biService.getReport(Number(reportId));
      setReport({ ...(data as unknown as ReportDefinition) });
    };
    void load();
  }, [reportId]);

  const save = async () => {
    if (reportId && reportId !== 'new') {
      await biService.updateReport(Number(reportId), report);
    } else {
      await biService.createReport(report);
    }
    navigate('/reports');
  };

  const execute = async () => {
    if (!reportId || reportId === 'new') {
      return;
    }
    const data = await biService.executeReport(Number(reportId));
    setPreview(data);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-2xl font-bold text-brand-ink">{reportId && reportId !== 'new' ? 'Edit Report' : 'Create Report'}</h2>
        <div className="flex gap-2">
          {reportId && reportId !== 'new' && (
            <button onClick={() => void execute()} className="rounded bg-brand-mint px-3 py-2 text-sm text-white">Run</button>
          )}
          <button onClick={() => void save()} className="rounded bg-brand-deep px-3 py-2 text-sm text-white">Save</button>
        </div>
      </div>

      <div className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-brand-deep/70">Report Name</label>
            <input value={report.name} onChange={(e) => setReport({ ...report, name: e.target.value })} className="mt-1 w-full rounded border border-brand-deep/20 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="text-xs text-brand-deep/70">Category</label>
            <select value={report.category} onChange={(e) => setReport({ ...report, category: e.target.value })} className="mt-1 w-full rounded border border-brand-deep/20 px-3 py-2 text-sm">
              {['Financial', 'Compliance', 'Operational', 'Custom'].map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label className="text-xs text-brand-deep/70">Description</label>
          <textarea value={report.description || ''} onChange={(e) => setReport({ ...report, description: e.target.value })} className="mt-1 w-full rounded border border-brand-deep/20 px-3 py-2 text-sm" rows={2} />
        </div>

        <div>
          <label className="text-xs text-brand-deep/70">Source</label>
          <select
            value={report.definition.source}
            onChange={(e) => setReport({ ...report, definition: { ...report.definition, source: e.target.value } })}
            className="mt-1 w-full rounded border border-brand-deep/20 px-3 py-2 text-sm"
          >
            {SOURCES.map((source) => <option key={source} value={source}>{source}</option>)}
          </select>
        </div>

        <div>
          <label className="text-xs text-brand-deep/70">Dimensions (comma separated)</label>
          <input
            value={report.definition.dimensions.join(', ')}
            onChange={(e) => setReport({
              ...report,
              definition: { ...report.definition, dimensions: e.target.value.split(',').map((x) => x.trim()).filter(Boolean) },
            })}
            className="mt-1 w-full rounded border border-brand-deep/20 px-3 py-2 text-sm"
            placeholder="party_id, data.lender_name"
          />
        </div>

        <div>
          <label className="text-xs text-brand-deep/70">Metrics</label>
          <div className="space-y-2 mt-2">
            {report.definition.metrics.map((metric, idx) => (
              <div key={idx} className="grid grid-cols-12 gap-2">
                <input
                  value={metric.field}
                  onChange={(e) => {
                    const next = [...report.definition.metrics];
                    next[idx].field = e.target.value;
                    setReport({ ...report, definition: { ...report.definition, metrics: next } });
                  }}
                  placeholder="field"
                  className="col-span-5 rounded border border-brand-deep/20 px-2 py-1 text-sm"
                />
                <select
                  value={metric.aggregation}
                  onChange={(e) => {
                    const next = [...report.definition.metrics];
                    next[idx].aggregation = e.target.value;
                    setReport({ ...report, definition: { ...report.definition, metrics: next } });
                  }}
                  className="col-span-3 rounded border border-brand-deep/20 px-2 py-1 text-sm"
                >
                  {AGGREGATIONS.map((agg) => <option key={agg} value={agg}>{agg}</option>)}
                </select>
                <input
                  value={metric.alias}
                  onChange={(e) => {
                    const next = [...report.definition.metrics];
                    next[idx].alias = e.target.value;
                    setReport({ ...report, definition: { ...report.definition, metrics: next } });
                  }}
                  placeholder="alias"
                  className="col-span-3 rounded border border-brand-deep/20 px-2 py-1 text-sm"
                />
                <button
                  onClick={() => setReport({
                    ...report,
                    definition: { ...report.definition, metrics: report.definition.metrics.filter((_, i) => i !== idx) },
                  })}
                  className="col-span-1 rounded border border-red-300 text-red-600 text-sm"
                >x</button>
              </div>
            ))}
            <button
              onClick={() => setReport({
                ...report,
                definition: { ...report.definition, metrics: [...report.definition.metrics, { field: '', aggregation: 'sum', alias: '' }] },
              })}
              className="rounded border border-brand-deep/20 px-3 py-1 text-sm"
            >
              Add Metric
            </button>
          </div>
        </div>

        <div>
          <label className="text-xs text-brand-deep/70">Filters</label>
          <div className="space-y-2 mt-2">
            {report.definition.filters.map((f, idx) => (
              <div key={idx} className="grid grid-cols-12 gap-2">
                <input
                  value={String(f.field || '')}
                  onChange={(e) => {
                    const next = [...report.definition.filters];
                    next[idx].field = e.target.value;
                    setReport({ ...report, definition: { ...report.definition, filters: next } });
                  }}
                  placeholder="field"
                  className="col-span-4 rounded border border-brand-deep/20 px-2 py-1 text-sm"
                />
                <select
                  value={String(f.operator || 'eq')}
                  onChange={(e) => {
                    const next = [...report.definition.filters];
                    next[idx].operator = e.target.value;
                    setReport({ ...report, definition: { ...report.definition, filters: next } });
                  }}
                  className="col-span-3 rounded border border-brand-deep/20 px-2 py-1 text-sm"
                >
                  {OPERATORS.map((op) => <option key={op} value={op}>{op}</option>)}
                </select>
                <input
                  value={String(f.value ?? '')}
                  onChange={(e) => {
                    const next = [...report.definition.filters];
                    next[idx].value = e.target.value;
                    setReport({ ...report, definition: { ...report.definition, filters: next } });
                  }}
                  placeholder="value"
                  className="col-span-4 rounded border border-brand-deep/20 px-2 py-1 text-sm"
                />
                <button
                  onClick={() => setReport({
                    ...report,
                    definition: { ...report.definition, filters: report.definition.filters.filter((_, i) => i !== idx) },
                  })}
                  className="col-span-1 rounded border border-red-300 text-red-600 text-sm"
                >x</button>
              </div>
            ))}
            <button
              onClick={() => setReport({
                ...report,
                definition: { ...report.definition, filters: [...report.definition.filters, { field: '', operator: 'eq', value: '' }] },
              })}
              className="rounded border border-brand-deep/20 px-3 py-1 text-sm"
            >
              Add Filter
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <label className="text-xs text-brand-deep/70">Output Format</label>
            <select
              value={report.output_format}
              onChange={(e) => setReport({ ...report, output_format: e.target.value })}
              className="mt-1 w-full rounded border border-brand-deep/20 px-3 py-2 text-sm"
            >
              {['HTML', 'PDF', 'Excel', 'CSV'].map((f) => <option key={f} value={f}>{f}</option>)}
            </select>
          </div>
          <label className="flex items-center gap-2 text-sm mt-6">
            <input type="checkbox" checked={Boolean(report.is_public)} onChange={(e) => setReport({ ...report, is_public: e.target.checked })} />
            Public report
          </label>
          <label className="flex items-center gap-2 text-sm mt-6">
            <input type="checkbox" checked={Boolean(report.is_scheduled)} onChange={(e) => setReport({ ...report, is_scheduled: e.target.checked })} />
            Scheduled
          </label>
        </div>
      </div>

      {preview && (
        <div className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft">
          <h3 className="font-semibold mb-2">Preview</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead><tr>{preview.columns.map((c) => <th key={c} className="text-left px-2 py-1 border-b">{c}</th>)}</tr></thead>
              <tbody>
                {preview.data.map((row, idx) => (
                  <tr key={idx}>{preview.columns.map((c) => <td key={c} className="px-2 py-1 border-b">{String(row[c] ?? '')}</td>)}</tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
