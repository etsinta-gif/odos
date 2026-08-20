import { useEffect, useState } from 'react';
import { BarChart, PieChart } from '../charts/SimpleCharts';
import apiClient from '../../api/client';
import { phase1DashboardService, type Phase1Filters, type Phase1Payload } from '../../api/phase1DashboardService';

type DashboardKind = 'pnl' | 'working-capital' | 'portfolio-health';

type Props = {
  title: string;
  description: string;
  kind: DashboardKind;
  loader: (filters: Phase1Filters) => Promise<Phase1Payload>;
};

function formatMetric(value: unknown): string {
  if (value === null || value === undefined) return '-';
  if (typeof value === 'number') return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 2 }).format(value);
  return String(value);
}

function metricEntries(kind: DashboardKind, payload: Phase1Payload): Array<[string, unknown]> {
  if (kind === 'pnl') return [['Revenue', payload.revenue], ['Variable Expenses', payload.variable_expenses], ['Contribution Margin', payload.contribution_margin], ['Fixed Costs', payload.fixed_costs], ['EBITDA', payload.ebitda], ['EBITDA Margin %', payload.ebitda_margin], ['Revenue Growth %', payload.revenue_growth]];
  if (kind === 'working-capital') return [['Total Revenue', payload.total_revenue], ['Total Expenses', payload.total_expenses], ['Gross Working Capital', payload.gross_working_capital], ['DSO', payload.dso], ['DPO', payload.dpo], ['CCC', payload.ccc], ['Receivables', payload.outstanding_receivables], ['Payables', payload.outstanding_payables], ['Net Working Capital', Number(payload.outstanding_receivables || 0) - Number(payload.outstanding_payables || 0)]];
  return [['Revenue Total', payload.revenue_total], ['Overall Weighted Rating / 20', payload.weighted_average_risk_score], ['Associated Rating', payload.associated_rating], ['Risk Band', payload.risk_band], ['Rating Coverage %', payload.rating_coverage_pct], ['Unrated Revenue', payload.unrated_revenue], ['Concentration Rows', Array.isArray(payload.concentration) ? payload.concentration.length : 0]];
}

export default function Phase1DashboardShell({ title, description, kind, loader }: Props) {
  const [filters, setFilters] = useState<Phase1Filters>(() => {
    const today = new Date();
    const to = today.toISOString().slice(0, 10);
    const from = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().slice(0, 10);
    return { period_from: from, period_to: to };
  });
  const [payload, setPayload] = useState<Phase1Payload | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const load = async (requestedFilters: Phase1Filters = filters) => {
    setLoading(true);
    setError('');
    try {
      setPayload(await loader(requestedFilters));
    } catch (requestError: any) {
      setPayload(null);
      setError(String(requestError?.response?.data?.detail || 'Dashboard data could not be loaded.'));
    } finally {
      setLoading(false);
    }
  };

  const exportDashboard = async (format: 'csv' | 'excel' | 'pdf') => {
    try {
      const apiKind = kind === 'pnl' ? 'pnl-performance' : kind;
      const response = await phase1DashboardService.export(apiKind, filters, format);
      const url = URL.createObjectURL(response.data);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = `${kind}.${format === 'excel' ? 'xlsx' : format}`;
      anchor.click();
      URL.revokeObjectURL(url);
    } catch (requestError: any) {
      setError(String(requestError?.response?.data?.detail || `Failed to export ${format.toUpperCase()}.`));
    }
  };

  useEffect(() => {
    void (async () => {
      try {
        const response = await apiClient.get('/admin/pnl/policy/date-limits');
        const limits = response.data || {};
        const from = limits.max_month_from || limits.full_data_from;
        const to = limits.max_month_to || limits.full_data_to;
        if (from && to) {
          const datasetFilters = { period_from: String(from), period_to: String(to) };
          setFilters(datasetFilters);
          setPayload(await loader(datasetFilters));
          return;
        }
      } catch {
        // Fall back to the local month when legacy P&L limits are unavailable.
      }
      await load();
    })();
  }, [kind]);

  const ratingPoints = Array.isArray(payload?.revenue_by_credit_rating)
    ? payload.revenue_by_credit_rating.map((row: any) => ({ label: String(row.rating), value: Number(row.revenue || 0) }))
    : [];
  const concentrationPoints = Array.isArray(payload?.concentration)
    ? payload.concentration.map((row: any) => ({ label: String(row.dimension), value: Number(row.revenue || 0) }))
    : [];
  const contributionPoints = Array.isArray(payload?.profit_loss_counts?.contribution)
    ? payload.profit_loss_counts.contribution.map((row: any) => ({ label: String(row.label), value: Number(row.count || 0) }))
    : [];
  const ebitdaPoints = Array.isArray(payload?.profit_loss_counts?.ebitda)
    ? payload.profit_loss_counts.ebitda.map((row: any) => ({ label: String(row.label), value: Number(row.count || 0) }))
    : [];
  const variableExpenseCountPoints = Array.isArray(payload?.variable_expense_distribution)
    ? payload.variable_expense_distribution.map((row: any) => ({ label: String(row.label), value: Number(row.unit_count || 0) }))
    : [];
  const variableExpenseRevenuePoints = Array.isArray(payload?.variable_expense_distribution)
    ? payload.variable_expense_distribution.map((row: any) => ({ label: String(row.label), value: Number(row.revenue_amount || 0) }))
    : [];
  const dsoProductPoints = Array.isArray(payload?.dso_by_product)
    ? payload.dso_by_product.map((row: any) => ({ label: String(row.product), value: Number(row.dso_days || 0) }))
    : [];
  const dpoTypePoints = Array.isArray(payload?.dpo_by_payable_type)
    ? payload.dpo_by_payable_type.map((row: any) => ({ label: String(row.payable_type), value: Number(row.dpo_days || 0) }))
    : [];
  const agingPoints = Array.isArray(payload?.receivables_aging)
    ? payload.receivables_aging.map((row: any) => ({ label: String(row.bucket), value: Number(row.amount || 0) }))
    : [];
  const payableAgingPoints = Array.isArray(payload?.payables_aging)
    ? payload.payables_aging.map((row: any) => ({ label: String(row.bucket), value: Number(row.amount || 0) }))
    : [];
  const monthlyCashFlow = Array.isArray(payload?.monthly_cash_flow) ? payload.monthly_cash_flow : [];

  return (
    <div className="space-y-5">
      <header>
        <h1 className="text-2xl font-bold text-brand-ink">{title}</h1>
        <p className="mt-1 text-sm text-brand-deep/70">{description}</p>
      </header>
      <section className="flex flex-wrap items-end gap-3 rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft">
        <label className="text-xs font-semibold text-brand-deep">From<input aria-label="Period From" type="date" value={filters.period_from} onChange={(event) => setFilters({ ...filters, period_from: event.target.value })} className="mt-1 block rounded border px-2 py-1 text-sm" /></label>
        <label className="text-xs font-semibold text-brand-deep">To<input aria-label="Period To" type="date" value={filters.period_to} onChange={(event) => setFilters({ ...filters, period_to: event.target.value })} className="mt-1 block rounded border px-2 py-1 text-sm" /></label>
        <button type="button" onClick={() => void load()} className="rounded bg-brand-deep px-3 py-2 text-sm font-semibold text-white">Refresh</button>
        <button type="button" disabled={!payload} onClick={() => void exportDashboard('csv')} className="rounded border border-brand-deep/20 px-3 py-2 text-sm font-semibold disabled:opacity-40">Export CSV</button>
        <button type="button" disabled={!payload} onClick={() => void exportDashboard('excel')} className="rounded border border-brand-deep/20 px-3 py-2 text-sm font-semibold disabled:opacity-40">Export Excel</button>
        <button type="button" disabled={!payload} onClick={() => void exportDashboard('pdf')} className="rounded border border-brand-deep/20 px-3 py-2 text-sm font-semibold disabled:opacity-40">Export PDF</button>
      </section>
      {error ? <div className="rounded border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-800">{error}</div> : null}
      {loading ? <p className="text-sm text-brand-deep/70">Loading dashboard data...</p> : null}
      {payload ? <>
        <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {metricEntries(kind, payload).map(([label, value]) => <div key={label} className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><div className="text-xs text-brand-deep/65">{label}</div><div className="mt-1 text-xl font-bold text-brand-ink">{formatMetric(value)}</div></div>)}
        </section>
        {kind !== 'working-capital' ? <section className="grid gap-4 lg:grid-cols-2">
          {kind === 'portfolio-health' ? <><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><BarChart title="Revenue by Credit Rating" points={ratingPoints} /></div><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><PieChart title="Portfolio Distribution" points={ratingPoints} /></div><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><BarChart title="Revenue Concentration" points={concentrationPoints} /></div><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft lg:col-span-2"><h2 className="font-semibold text-brand-ink">Unrated Customers & Revenue</h2><p className="mt-1 text-xs text-brand-deep/70">Customers without a rating and the revenue attributed to them in the selected period.</p><div className="mt-3 overflow-x-auto"><table className="min-w-full text-xs"><thead><tr className="border-b text-left"><th className="px-2 py-2">Customer</th><th className="px-2 py-2">Revenue</th><th className="px-2 py-2">Share %</th></tr></thead><tbody>{Array.isArray(payload?.unrated_customers) && payload.unrated_customers.length ? payload.unrated_customers.map((row: any) => <tr key={String(row.customer)} className="border-b"><td className="px-2 py-2 font-medium">{row.customer}</td><td className="px-2 py-2">{formatMetric(row.revenue)}</td><td className="px-2 py-2">{formatMetric(row.share_pct)}</td></tr>) : <tr><td colSpan={3} className="px-2 py-3 text-brand-deep/70">No unrated customers in the selected window.</td></tr>}</tbody></table></div></div></> : <><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><BarChart title="Contribution Level: Profit vs Loss Units" points={contributionPoints} /><p className="mt-3 text-xs text-brand-deep/70">Profit means Contribution Margin is zero or positive. Loss means Contribution Margin is negative. Contribution = Revenue minus Variable Expenses.</p></div><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><BarChart title="EBITDA Level: Profit vs Loss Units" points={ebitdaPoints} /><p className="mt-3 text-xs text-brand-deep/70">Profit means EBITDA is zero or positive. Loss means EBITDA is negative. EBITDA = Contribution Margin minus Fixed Costs.</p></div></>}
        </section> : null}
        {kind === 'pnl' ? (
          <section className="grid gap-4 lg:grid-cols-2">
            <div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft">
              <h2 className="font-semibold text-brand-ink">Variable Expenses %: Unit Count</h2>
              <p className="mt-1 text-xs text-brand-deep/70">Each P&L unit is grouped by Variable Expenses divided by Revenue. Labels stay attached to the corresponding percentage bar.</p>
              <BarChart title="Units by Variable Expense Band" points={variableExpenseCountPoints} compactLabels />
            </div>
            <div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft">
              <h2 className="font-semibold text-brand-ink">Variable Expenses %: Revenue Amount</h2>
              <p className="mt-1 text-xs text-brand-deep/70">Each point shows the total Revenue generated by units in that Variable Expense percentage band.</p>
              <BarChart title="Revenue by Variable Expense Band" points={variableExpenseRevenuePoints} compactLabels />
            </div>
          </section>
        ) : null}
        {kind === 'working-capital' ? (
          <>
            <section className="grid gap-4 lg:grid-cols-2">
              <div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><h2 className="font-semibold text-brand-ink">DSO by Product</h2><p className="mt-1 text-xs text-brand-deep/70">Weighted DSO days by product; labels show the product and bars show days.</p><BarChart title="DSO Days" points={dsoProductPoints} compactLabels /></div>
              <div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><h2 className="font-semibold text-brand-ink">DPO by Payable Type</h2><p className="mt-1 text-xs text-brand-deep/70">Average payable days and invoice amounts by expense stream.</p><BarChart title="DPO Days" points={dpoTypePoints} compactLabels /></div>
            </section>
            <section className="grid gap-4 lg:grid-cols-2"><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><h2 className="font-semibold text-brand-ink">Receivables Aging</h2><PieChart title="Outstanding Receivables" points={agingPoints} /></div><div className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><h2 className="font-semibold text-brand-ink">Payables Aging</h2><PieChart title="Outstanding Payables" points={payableAgingPoints} /></div></section>
            <section className="rounded-xl border border-brand-deep/10 bg-white p-4 shadow-soft"><h2 className="font-semibold text-brand-ink">Monthly Cash Flow</h2><div className="mt-3 overflow-x-auto"><table className="min-w-full text-xs"><thead><tr className="border-b text-left"><th className="px-2 py-2">Month</th><th className="px-2 py-2">Amount Received</th><th className="px-2 py-2">Amount Paid</th><th className="px-2 py-2">Shortfall / Excess</th><th className="px-2 py-2">Cumulative Received</th><th className="px-2 py-2">Cumulative Paid</th><th className="px-2 py-2">Cumulative Shortfall / Excess</th></tr></thead><tbody>{monthlyCashFlow.map((row: any) => <tr key={String(row.month)} className="border-b"><td className="px-2 py-2 font-medium">{row.month}</td><td className="px-2 py-2">{formatMetric(row.amount_received)}</td><td className="px-2 py-2">{formatMetric(row.amount_paid)}</td><td className={`px-2 py-2 font-semibold ${Number(row.shortfall_excess) < 0 ? 'text-rose-700' : 'text-emerald-700'}`}>{formatMetric(row.shortfall_excess)}</td><td className="px-2 py-2">{formatMetric(row.cumulative_amount_received)}</td><td className="px-2 py-2">{formatMetric(row.cumulative_amount_paid)}</td><td className={`px-2 py-2 font-semibold ${Number(row.cumulative_shortfall_excess) < 0 ? 'text-rose-700' : 'text-emerald-700'}`}>{formatMetric(row.cumulative_shortfall_excess)}</td></tr>)}</tbody></table>{monthlyCashFlow.length === 0 ? <p className="mt-3 text-xs text-brand-deep/70">No months in the selected period.</p> : null}</div></section>
          </>
        ) : null}
      </> : null}
    </div>
  );
}

export { phase1DashboardService };
