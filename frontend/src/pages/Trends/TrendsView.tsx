import { useEffect, useState } from 'react';

import { biService } from '../../api/biService';
import { BarChart, LineChart, PieChart } from '../../components/charts/SimpleCharts';

export default function TrendsView() {
  const [summary, setSummary] = useState<Record<string, { data: Array<{ date: string; count: number }> }> | null>(null);

  useEffect(() => {
    const load = async () => {
      setSummary(await biService.getTrendSummary());
    };
    void load();
  }, []);

  if (!summary) {
    return <div className="py-10 text-center text-brand-deep/70">Loading trends...</div>;
  }

  const gst = summary.gst_mismatches?.data || [];
  const tds = summary.tds_mismatches?.data || [];
  const com = summary.commission_exceeds?.data || [];
  const red = summary.red_flags?.data || [];

  const toPoints = (rows: Array<{ date: string; count: number }>) => rows.map((row) => ({ label: row.date, value: row.count }));

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-brand-ink">Trends</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft"><LineChart title="GST Mismatches" points={toPoints(gst)} /></div>
        <div className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft"><LineChart title="TDS Mismatches" points={toPoints(tds)} /></div>
        <div className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft"><BarChart title="Commission Exceeds" points={toPoints(com)} /></div>
        <div className="bg-white border border-brand-deep/10 rounded-xl p-4 shadow-soft"><PieChart title="Red Flag Distribution" points={toPoints(red)} /></div>
      </div>
    </div>
  );
}
