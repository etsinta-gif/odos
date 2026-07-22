import { useEffect, useMemo, useState } from 'react';
import { partyService, type PartyDefaultsRecord } from '../../api/partyService';

type EditableRow = PartyDefaultsRecord & {
  dirty?: boolean;
};

function toRows(data: Array<Record<string, unknown>>, type: 'LENDER' | 'CONNECTOR'): EditableRow[] {
  if (type === 'LENDER') {
    return data.map((item) => ({
      id: Number(item.lender_id),
      type,
      name: String(item.lender_name || ''),
      default_gst_rate: Number(item.default_gst_rate ?? 0),
      default_tds_rate: Number(item.default_tds_rate ?? 0),
      max_commission: item.max_commission == null ? null : Number(item.max_commission),
    }));
  }

  return data.map((item) => ({
    id: Number(item.connector_id),
    type,
    name: String(item.full_name || ''),
    default_gst_rate: Number(item.default_gst_rate ?? 0),
    default_tds_rate: Number(item.default_tds_rate ?? 0),
    max_commission: item.max_commission == null ? null : Number(item.max_commission),
  }));
}

export default function PartyDefaultsPage() {
  const [rows, setRows] = useState<EditableRow[]>([]);
  const [scope, setScope] = useState<'ALL' | 'LENDER' | 'CONNECTOR'>('ALL');
  const [savingId, setSavingId] = useState<number | null>(null);

  const load = async () => {
    const [lenders, connectors] = await Promise.all([partyService.getLenders(), partyService.getConnectors()]);
    setRows([...toRows(lenders, 'LENDER'), ...toRows(connectors, 'CONNECTOR')]);
  };

  useEffect(() => {
    void load();
  }, []);

  const filtered = useMemo(() => {
    if (scope === 'ALL') {
      return rows;
    }
    return rows.filter((r) => r.type === scope);
  }, [rows, scope]);

  const updateCell = (id: number, key: keyof EditableRow, value: string) => {
    setRows((prev) =>
      prev.map((row) => {
        if (row.id !== id) {
          return row;
        }
        if (key === 'max_commission') {
          return { ...row, max_commission: value === '' ? null : Number(value), dirty: true };
        }
        return { ...row, [key]: Number(value), dirty: true };
      })
    );
  };

  const onSave = async (row: EditableRow) => {
    setSavingId(row.id);
    const payload = {
      default_gst_rate: row.default_gst_rate,
      default_tds_rate: row.default_tds_rate,
      max_commission: row.max_commission,
    };

    if (row.type === 'LENDER') {
      await partyService.updateLender(row.id, payload);
    } else {
      await partyService.updateConnector(row.id, payload);
    }

    setRows((prev) => prev.map((x) => (x.id === row.id && x.type === row.type ? { ...x, dirty: false } : x)));
    setSavingId(null);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-2xl font-bold text-brand-ink">Party Defaults</h2>
        <div className="flex gap-2">
          {(['ALL', 'LENDER', 'CONNECTOR'] as const).map((item) => (
            <button
              key={item}
              onClick={() => setScope(item)}
              className={`px-3 py-1 rounded text-sm ${scope === item ? 'bg-brand-deep text-white' : 'bg-white border border-brand-deep/20'}`}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-white border border-brand-deep/10 rounded-xl shadow-soft overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-brand-sand/60">
            <tr>
              <th className="text-left px-3 py-2">Type</th>
              <th className="text-left px-3 py-2">Name</th>
              <th className="text-left px-3 py-2">Default GST %</th>
              <th className="text-left px-3 py-2">Default TDS %</th>
              <th className="text-left px-3 py-2">Max Commission</th>
              <th className="text-left px-3 py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => (
              <tr key={`${row.type}-${row.id}`} className="border-t border-brand-deep/10">
                <td className="px-3 py-2">{row.type}</td>
                <td className="px-3 py-2">{row.name}</td>
                <td className="px-3 py-2">
                  <input
                    type="number"
                    step="0.01"
                    className="w-28 rounded border border-brand-deep/20 px-2 py-1"
                    value={row.default_gst_rate}
                    onChange={(e) => updateCell(row.id, 'default_gst_rate', e.target.value)}
                  />
                </td>
                <td className="px-3 py-2">
                  <input
                    type="number"
                    step="0.01"
                    className="w-28 rounded border border-brand-deep/20 px-2 py-1"
                    value={row.default_tds_rate}
                    onChange={(e) => updateCell(row.id, 'default_tds_rate', e.target.value)}
                  />
                </td>
                <td className="px-3 py-2">
                  <input
                    type="number"
                    step="0.01"
                    className="w-36 rounded border border-brand-deep/20 px-2 py-1"
                    value={row.max_commission ?? ''}
                    onChange={(e) => updateCell(row.id, 'max_commission', e.target.value)}
                  />
                </td>
                <td className="px-3 py-2">
                  <button
                    disabled={!row.dirty || savingId === row.id}
                    onClick={() => void onSave(row)}
                    className="rounded bg-brand-mint px-3 py-1.5 text-white disabled:opacity-50"
                  >
                    {savingId === row.id ? 'Saving...' : 'Save'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <p className="px-3 py-3 text-sm text-brand-deep/70">No party records found.</p>}
      </div>
    </div>
  );
}
