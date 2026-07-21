import { useEffect, useMemo, useState } from 'react';
import apiClient from '../../api/client';

type Flag = {
  id: number;
  severity: 'critical' | 'warning' | 'info';
  category: string;
  title: string;
  description: string;
  source: string;
  source_id: number;
  created_at: string;
  status: 'open' | 'in_progress' | 'resolved';
  actions: Array<{ label: string; action: string; batch_guid?: string }>;
};

export default function RedFlags() {
  const [flags, setFlags] = useState<Flag[]>([]);
  const [filter, setFilter] = useState<'all' | 'critical' | 'warning' | 'info'>('all');

  useEffect(() => {
    apiClient.get('/admin/redflags').then((res) => setFlags(res.data));
  }, []);

  const filtered = useMemo(() => flags.filter((f) => filter === 'all' || f.severity === filter), [flags, filter]);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-brand-ink">Red-Flag Dashboard</h2>
      <div className="flex gap-2">
        {(['all', 'critical', 'warning', 'info'] as const).map((item) => (
          <button
            key={item}
            onClick={() => setFilter(item)}
            className={`px-3 py-1 rounded text-sm ${filter === item ? 'bg-brand-deep text-white' : 'bg-white border border-brand-deep/20'}`}
          >
            {item}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {filtered.map((flag) => (
          <div key={flag.id} className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="font-semibold">{flag.title}</p>
                <p className="text-sm text-brand-deep/70">{flag.description}</p>
                <p className="text-xs text-brand-deep/60 mt-1">{flag.category} • {flag.source}#{flag.source_id}</p>
              </div>
              <span className="text-xs px-2 py-1 rounded bg-brand-sand border border-brand-deep/20">{flag.severity}</span>
            </div>
          </div>
        ))}
        {filtered.length === 0 && <p className="text-sm text-brand-deep/70">No flags for this filter.</p>}
      </div>
    </div>
  );
}
