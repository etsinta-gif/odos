import { useEffect, useMemo, useState } from 'react';
import { alertsService, type AlertRecord, type AlertSummary } from '../../api/alertsService';

type StatusFilter = 'ALL' | 'OPEN' | 'RESOLVED' | 'IGNORED';
type SeverityFilter = 'ALL' | 'CRITICAL' | 'WARNING' | 'INFO';

export default function RedFlags() {
  const [flags, setFlags] = useState<AlertRecord[]>([]);
  const [summary, setSummary] = useState<AlertSummary | null>(null);
  const [severity, setSeverity] = useState<SeverityFilter>('ALL');
  const [status, setStatus] = useState<StatusFilter>('ALL');
  const [noteById, setNoteById] = useState<Record<number, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const load = async () => {
    setIsLoading(true);
    try {
      const [listPayload, summaryPayload] = await Promise.all([
        alertsService.list({
          severity: severity === 'ALL' ? undefined : severity,
          status: status === 'ALL' ? undefined : status,
          limit: 300,
        }),
        alertsService.summary(),
      ]);
      setFlags(listPayload.records);
      setSummary(summaryPayload);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, [severity, status]);

  const filtered = useMemo(() => flags, [flags]);

  const setNote = (id: number, value: string) => {
    setNoteById((prev) => ({ ...prev, [id]: value }));
  };

  const onResolve = async (id: number) => {
    await alertsService.resolve(id, noteById[id]);
    await load();
  };

  const onIgnore = async (id: number) => {
    await alertsService.ignore(id, noteById[id]);
    await load();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-brand-ink">Red-Flag Dashboard</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-white border border-brand-deep/10 rounded-xl p-3 shadow-soft">
          <p className="text-xs text-brand-deep/60">Total</p>
          <p className="text-2xl font-bold text-brand-ink">{summary?.total ?? 0}</p>
        </div>
        <div className="bg-white border border-brand-deep/10 rounded-xl p-3 shadow-soft">
          <p className="text-xs text-brand-deep/60">Open</p>
          <p className="text-2xl font-bold text-brand-ink">{summary?.by_status?.OPEN ?? 0}</p>
        </div>
        <div className="bg-white border border-brand-deep/10 rounded-xl p-3 shadow-soft">
          <p className="text-xs text-brand-deep/60">Critical</p>
          <p className="text-2xl font-bold text-brand-ink">{summary?.by_severity?.CRITICAL ?? 0}</p>
        </div>
        <div className="bg-white border border-brand-deep/10 rounded-xl p-3 shadow-soft">
          <p className="text-xs text-brand-deep/60">Warnings</p>
          <p className="text-2xl font-bold text-brand-ink">{summary?.by_severity?.WARNING ?? 0}</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {(['ALL', 'CRITICAL', 'WARNING', 'INFO'] as const).map((item) => (
          <button
            key={item}
            onClick={() => setSeverity(item)}
            className={`px-3 py-1 rounded text-sm ${severity === item ? 'bg-brand-deep text-white' : 'bg-white border border-brand-deep/20'}`}
          >
            {item}
          </button>
        ))}
        {(['ALL', 'OPEN', 'RESOLVED', 'IGNORED'] as const).map((item) => (
          <button
            key={item}
            onClick={() => setStatus(item)}
            className={`px-3 py-1 rounded text-sm ${status === item ? 'bg-brand-mint text-white' : 'bg-white border border-brand-deep/20'}`}
          >
            {item}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {isLoading && <p className="text-sm text-brand-deep/70">Loading...</p>}
        {filtered.map((flag) => (
          <div key={flag.red_flag_id} className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="font-semibold">{flag.record_type} #{flag.record_id}</p>
                <p className="text-sm text-brand-deep/70">{flag.message}</p>
                <p className="text-xs text-brand-deep/60 mt-1">{flag.category} • {flag.status}</p>
                <p className="text-xs text-brand-deep/50 mt-1">Reported: {flag.reported_value ?? '-'} | Expected: {flag.expected_value ?? '-'}</p>
              </div>
              <span className="text-xs px-2 py-1 rounded bg-brand-sand border border-brand-deep/20">{flag.severity}</span>
            </div>
            {flag.status === 'OPEN' && (
              <div className="mt-3 flex flex-col gap-2 md:flex-row">
                <input
                  className="flex-1 rounded border border-brand-deep/20 px-3 py-2 text-sm"
                  placeholder="Resolution note"
                  value={noteById[flag.red_flag_id] || ''}
                  onChange={(e) => setNote(flag.red_flag_id, e.target.value)}
                />
                <button
                  onClick={() => void onResolve(flag.red_flag_id)}
                  className="rounded bg-brand-mint px-3 py-2 text-sm text-white"
                >
                  Resolve
                </button>
                <button
                  onClick={() => void onIgnore(flag.red_flag_id)}
                  className="rounded border border-brand-deep/30 px-3 py-2 text-sm"
                >
                  Ignore
                </button>
              </div>
            )}
            {flag.status !== 'OPEN' && flag.resolution_notes && (
              <p className="mt-2 text-xs text-brand-deep/70">Note: {flag.resolution_notes}</p>
            )}
          </div>
        ))}
        {!isLoading && filtered.length === 0 && <p className="text-sm text-brand-deep/70">No flags for current filters.</p>}
      </div>
    </div>
  );
}
