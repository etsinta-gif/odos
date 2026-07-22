import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';

import { biService } from '../../api/biService';
import { BarChart, LineChart, PieChart } from '../../components/charts/SimpleCharts';

type DashboardPayload = {
  dashboard_id: number;
  name: string;
  description?: string;
  widgets: Array<{
    widget_id: number;
    title: string;
    type: string;
    chart_type?: string;
    report_id?: number;
    width: number;
    height: number;
  }>;
};

function normalize(points: Array<Record<string, unknown>>) {
  if (points.length === 0) {
    return [];
  }
  const keys = Object.keys(points[0]);
  if (keys.length < 2) {
    return [];
  }
  const labelKey = keys[0];
  const valueKey = keys[1];
  return points.map((item) => ({
    label: String(item[labelKey] ?? ''),
    value: Number(item[valueKey] ?? 0),
  }));
}

export default function DashboardView() {
  const { dashboardId } = useParams();
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [widgetData, setWidgetData] = useState<Record<number, { columns: string[]; data: Array<Record<string, unknown>> }>>({});

  useEffect(() => {
    const load = async () => {
      if (!dashboardId) {
        return;
      }
      const payload = (await biService.getDashboard(Number(dashboardId))) as unknown as DashboardPayload;
      setDashboard(payload);
      for (const widget of payload.widgets || []) {
        const data = await biService.executeWidget(payload.dashboard_id, widget.widget_id);
        setWidgetData((prev) => ({ ...prev, [widget.widget_id]: data }));
      }
    };
    void load();
  }, [dashboardId]);

  const addWidget = async () => {
    if (!dashboard) {
      return;
    }
    await biService.addWidget(dashboard.dashboard_id, {
      title: 'New KPI',
      type: 'KPI',
      chart_type: 'TABLE',
      width: 4,
      height: 3,
      query_definition: {
        source: 'ETL_RedFlag',
        dimensions: ['severity'],
        metrics: [{ field: 'red_flag_id', aggregation: 'count', alias: 'count' }],
        filters: [],
      },
    });
    const payload = (await biService.getDashboard(dashboard.dashboard_id)) as unknown as DashboardPayload;
    setDashboard(payload);
  };

  const cards = useMemo(() => dashboard?.widgets || [], [dashboard]);

  if (!dashboard) {
    return <div className="py-10 text-center text-brand-deep/70">Loading dashboard...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-brand-ink">{dashboard.name}</h2>
          <p className="text-sm text-brand-deep/70">{dashboard.description}</p>
        </div>
        <button onClick={() => void addWidget()} className="rounded bg-brand-deep px-3 py-2 text-sm text-white">Add Widget</button>
      </div>

      <div className="grid grid-cols-12 gap-3">
        {cards.map((widget) => {
          const data = widgetData[widget.widget_id];
          const points = normalize(data?.data || []);

          return (
            <div key={widget.widget_id} className="col-span-12 md:col-span-6 bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft">
              <h3 className="font-semibold mb-2">{widget.title}</h3>
              {!data && <p className="text-sm text-brand-deep/70">Loading widget...</p>}
              {data && widget.chart_type === 'BAR' && <BarChart title={widget.title} points={points} />}
              {data && widget.chart_type === 'LINE' && <LineChart title={widget.title} points={points} />}
              {data && widget.chart_type === 'PIE' && <PieChart title={widget.title} points={points} />}
              {data && (!widget.chart_type || widget.chart_type === 'TABLE' || widget.type === 'KPI') && (
                <div className="overflow-x-auto">
                  <table className="min-w-full text-xs">
                    <thead><tr>{data.columns.map((c) => <th key={c} className="text-left px-2 py-1 border-b">{c}</th>)}</tr></thead>
                    <tbody>
                      {data.data.map((row, idx) => (
                        <tr key={idx}>{data.columns.map((c) => <td key={c} className="px-2 py-1 border-b">{String(row[c] ?? '')}</td>)}</tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
