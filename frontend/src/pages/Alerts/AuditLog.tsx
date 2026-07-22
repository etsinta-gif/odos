import { useEffect, useState } from 'react';

import { alertsService, type AlertAuditLog } from '../../api/alertsService';

const ACTIONS = ['ALL', 'TRIGGERED', 'RESOLVED', 'IGNORED', 'ESCALATED', 'AUTO_RESOLVED', 'AUTO_ASSIGNED'];

export default function AuditLog() {
  const [logs, setLogs] = useState<AlertAuditLog[]>([]);
  const [action, setAction] = useState('ALL');
  const [isLoading, setIsLoading] = useState(false);

  const load = async (selectedAction = action) => {
    setIsLoading(true);
    try {
      const payload = await alertsService.listAuditLogs({
        limit: 200,
        action: selectedAction === 'ALL' ? undefined : selectedAction,
      });
      setLogs(payload);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-2xl font-bold text-brand-ink">Alert Audit Log</h2>
        <div className="flex gap-2">
          <select
            className="rounded border border-brand-deep/20 px-3 py-2 text-sm"
            value={action}
            onChange={(e) => {
              setAction(e.target.value);
              void load(e.target.value);
            }}
          >
            {ACTIONS.map((item) => <option key={item} value={item}>{item}</option>)}
          </select>
          <button className="rounded bg-brand-deep px-3 py-2 text-sm text-white" onClick={() => void load()}>
            Refresh
          </button>
        </div>
      </div>

      <div className="bg-white border border-brand-deep/10 rounded-xl shadow-soft overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-brand-sand/60">
            <tr>
              <th className="text-left px-3 py-2">Action</th>
              <th className="text-left px-3 py-2">Details</th>
              <th className="text-left px-3 py-2">Performed At</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.log_id} className="border-t border-brand-deep/10 align-top">
                <td className="px-3 py-2">{log.action}</td>
                <td className="px-3 py-2">
                  <pre className="text-xs whitespace-pre-wrap text-brand-deep/80">{log.details ? JSON.stringify(log.details, null, 2) : '-'}</pre>
                </td>
                <td className="px-3 py-2 text-xs text-brand-deep/70">{log.performed_at ? new Date(log.performed_at).toLocaleString() : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {isLoading && <p className="px-3 py-3 text-sm text-brand-deep/70">Loading audit logs...</p>}
        {!isLoading && logs.length === 0 && <p className="px-3 py-3 text-sm text-brand-deep/70">No audit events found.</p>}
      </div>
    </div>
  );
}
