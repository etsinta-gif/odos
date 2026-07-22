import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { biService } from '../../api/biService';

export default function DashboardList() {
  const [dashboards, setDashboards] = useState<Array<Record<string, unknown>>>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const load = async () => {
    setDashboards(await biService.listDashboards());
  };

  useEffect(() => {
    void load();
  }, []);

  const create = async () => {
    if (!name.trim()) {
      return;
    }
    await biService.createDashboard({ name, description, layout: { cols: 12 } });
    setName('');
    setDescription('');
    await load();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-brand-ink">Dashboards</h2>

      <div className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft grid grid-cols-1 md:grid-cols-3 gap-2">
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Dashboard name" className="rounded border border-brand-deep/20 px-3 py-2 text-sm" />
        <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" className="rounded border border-brand-deep/20 px-3 py-2 text-sm" />
        <button onClick={() => void create()} className="rounded bg-brand-deep px-3 py-2 text-sm text-white">Create</button>
      </div>

      <div className="bg-white border border-brand-deep/10 rounded-xl shadow-soft overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-brand-sand/60">
            <tr>
              <th className="text-left px-3 py-2">Name</th>
              <th className="text-left px-3 py-2">Description</th>
              <th className="text-left px-3 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {dashboards.map((dash) => {
              const id = Number(dash.dashboard_id);
              return (
                <tr key={id} className="border-t border-brand-deep/10">
                  <td className="px-3 py-2">{String(dash.name || '')}</td>
                  <td className="px-3 py-2">{String(dash.description || '')}</td>
                  <td className="px-3 py-2">
                    <div className="flex gap-2">
                      <Link to={`/dashboards/${id}`} className="rounded border border-brand-deep/20 px-2 py-1 text-xs">Open</Link>
                      <button
                        onClick={async () => {
                          await biService.deleteDashboard(id);
                          await load();
                        }}
                        className="rounded border border-red-300 px-2 py-1 text-xs text-red-700"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {dashboards.length === 0 && <p className="px-3 py-3 text-sm text-brand-deep/70">No dashboards yet.</p>}
      </div>
    </div>
  );
}
