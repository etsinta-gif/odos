import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { biService } from '../../api/biService';

export default function ReportsList() {
  const [reports, setReports] = useState<Array<Record<string, unknown>>>([]);
  const [busyId, setBusyId] = useState<number | null>(null);

  const load = async () => {
    const data = await biService.listReports();
    setReports(data);
  };

  useEffect(() => {
    void load();
  }, []);

  const runReport = async (reportId: number) => {
    setBusyId(reportId);
    await biService.executeReport(reportId);
    setBusyId(null);
  };

  const doExport = async (reportId: number, format: 'pdf' | 'excel' | 'csv') => {
    const response = await biService.exportReport(reportId, format);
    const blobUrl = URL.createObjectURL(response.data);
    const anchor = document.createElement('a');
    anchor.href = blobUrl;
    anchor.download = `report-${reportId}.${format === 'excel' ? 'xlsx' : format}`;
    anchor.click();
    URL.revokeObjectURL(blobUrl);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-brand-ink">Reports</h2>
        <Link to="/reports/new" className="rounded bg-brand-deep px-3 py-2 text-sm text-white">New Report</Link>
      </div>

      <div className="bg-white border border-brand-deep/10 rounded-xl shadow-soft overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-brand-sand/60">
            <tr>
              <th className="text-left px-3 py-2">Name</th>
              <th className="text-left px-3 py-2">Category</th>
              <th className="text-left px-3 py-2">Format</th>
              <th className="text-left px-3 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => {
              const reportId = Number(report.report_id);
              return (
                <tr key={reportId} className="border-t border-brand-deep/10">
                  <td className="px-3 py-2">{String(report.name || '')}</td>
                  <td className="px-3 py-2">{String(report.category || '')}</td>
                  <td className="px-3 py-2">{String(report.output_format || '')}</td>
                  <td className="px-3 py-2">
                    <div className="flex flex-wrap gap-2">
                      <Link to={`/reports/${reportId}`} className="rounded border border-brand-deep/20 px-2 py-1 text-xs">Edit</Link>
                      <button onClick={() => void runReport(reportId)} className="rounded bg-brand-mint px-2 py-1 text-xs text-white">
                        {busyId === reportId ? 'Running...' : 'Run'}
                      </button>
                      <button onClick={() => void doExport(reportId, 'pdf')} className="rounded border border-brand-deep/20 px-2 py-1 text-xs">PDF</button>
                      <button onClick={() => void doExport(reportId, 'excel')} className="rounded border border-brand-deep/20 px-2 py-1 text-xs">Excel</button>
                      <button onClick={() => void doExport(reportId, 'csv')} className="rounded border border-brand-deep/20 px-2 py-1 text-xs">CSV</button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {reports.length === 0 && <p className="px-3 py-3 text-sm text-brand-deep/70">No reports created yet.</p>}
      </div>
    </div>
  );
}
