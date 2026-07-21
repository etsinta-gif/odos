import { useEffect, useState } from 'react';
import apiClient from '../../api/client';

type Stats = {
  lenders: number;
  products: number;
  customers: number;
  cases: number;
  connectors: number;
  revenue: number;
  commission: number;
};

type Activity = {
  id: number;
  type: string;
  action: string;
  description: string;
  timestamp: string | null;
};

export default function MastersDashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);

  useEffect(() => {
    Promise.all([
      apiClient.get('/masters/dashboard/stats'),
      apiClient.get('/masters/dashboard/activities'),
    ]).then(([statsRes, activityRes]) => {
      setStats(statsRes.data);
      setActivities(activityRes.data);
    });
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-brand-ink">Masters Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {[
          ['Lenders', stats?.lenders || 0],
          ['Products', stats?.products || 0],
          ['Customers', stats?.customers || 0],
          ['Cases', stats?.cases || 0],
          ['Connectors', stats?.connectors || 0],
          ['Revenue', `₹${(stats?.revenue || 0).toLocaleString()}`],
          ['Commission', `₹${(stats?.commission || 0).toLocaleString()}`],
        ].map(([label, value]) => (
          <div key={String(label)} className="rounded-xl bg-white border border-brand-deep/10 p-4 shadow-soft">
            <p className="text-xs uppercase text-brand-deep/60">{label}</p>
            <p className="text-2xl font-semibold mt-2">{value}</p>
          </div>
        ))}
      </div>

      <div className="rounded-xl bg-white border border-brand-deep/10 p-4 shadow-soft">
        <h3 className="font-semibold mb-3">Recent Activity</h3>
        <div className="space-y-2 max-h-56 overflow-auto">
          {activities.length === 0 && <p className="text-sm text-brand-deep/70">No activity yet.</p>}
          {activities.map((activity) => (
            <div key={`${activity.type}-${activity.id}-${activity.timestamp || ''}`} className="text-sm border-b border-brand-deep/10 pb-2">
              <span className="font-medium">{activity.description}</span>
              <span className="ml-2 text-brand-deep/60">{activity.timestamp ? new Date(activity.timestamp).toLocaleString() : '-'}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
