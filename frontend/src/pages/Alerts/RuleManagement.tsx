import { useEffect, useMemo, useState } from 'react';

import { alertsService, type AlertRule, type EscalationPolicy } from '../../api/alertsService';

type RuleDraft = {
  name: string;
  description: string;
  category: string;
  field: string;
  operator: string;
  value: string;
  priority: number;
  escalation_policy_id?: number;
  actionType: 'in_app' | 'email' | 'webhook' | 'auto_resolve' | 'auto_assign';
  recipients: string;
  webhookUrl: string;
};

const CATEGORY_OPTIONS = ['GST_MISMATCH', 'TDS_MISMATCH', 'COMMISSION_EXCEED', 'DUPLICATE', 'MISSING_DATA', 'ALL'];
const OPERATOR_OPTIONS = ['eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'in', 'like', 'is_null', 'is_not_null'];

function parseValue(raw: string): unknown {
  const trimmed = raw.trim();
  if (trimmed === 'true') return true;
  if (trimmed === 'false') return false;
  if (trimmed === 'null') return null;
  if (/^-?\d+(\.\d+)?$/.test(trimmed)) return Number(trimmed);
  if (trimmed.includes(',')) return trimmed.split(',').map((v) => v.trim()).filter(Boolean);
  return trimmed;
}

export default function RuleManagement() {
  const [rules, setRules] = useState<AlertRule[]>([]);
  const [policies, setPolicies] = useState<EscalationPolicy[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [draft, setDraft] = useState<RuleDraft>({
    name: '',
    description: '',
    category: 'GST_MISMATCH',
    field: 'severity',
    operator: 'eq',
    value: 'WARNING',
    priority: 2,
    actionType: 'in_app',
    recipients: '',
    webhookUrl: '',
  });

  const load = async () => {
    setIsLoading(true);
    try {
      const [rulesPayload, policiesPayload] = await Promise.all([
        alertsService.listRules(),
        alertsService.listEscalationPolicies(),
      ]);
      setRules(rulesPayload);
      setPolicies(policiesPayload);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const createRule = async () => {
    const actions: Array<Record<string, unknown>> = [];
    if (draft.actionType === 'in_app') {
      const userIds = draft.recipients
        .split(',')
        .map((x) => x.trim())
        .filter(Boolean)
        .map((x) => Number(x))
        .filter((x) => Number.isFinite(x));
      actions.push({ type: 'in_app', config: { user_ids: userIds } });
    }
    if (draft.actionType === 'email') {
      const recipients = draft.recipients.split(',').map((x) => x.trim()).filter(Boolean);
      actions.push({ type: 'email', config: { subject: draft.name, recipients } });
    }
    if (draft.actionType === 'webhook') {
      actions.push({ type: 'webhook', config: { url: draft.webhookUrl } });
    }
    if (draft.actionType === 'auto_resolve') {
      actions.push({ type: 'auto_resolve', config: {} });
    }
    if (draft.actionType === 'auto_assign') {
      actions.push({ type: 'auto_assign', config: {} });
    }

    await alertsService.createRule({
      name: draft.name,
      description: draft.description,
      category: draft.category,
      conditions: {
        field: draft.field,
        operator: draft.operator,
        value: parseValue(draft.value),
      },
      actions,
      escalation_policy_id: draft.escalation_policy_id,
      priority: draft.priority,
    });

    setShowCreate(false);
    setDraft({
      name: '',
      description: '',
      category: 'GST_MISMATCH',
      field: 'severity',
      operator: 'eq',
      value: 'WARNING',
      priority: 2,
      actionType: 'in_app',
      recipients: '',
      webhookUrl: '',
    });
    await load();
  };

  const activeCount = useMemo(() => rules.filter((r) => r.is_active).length, [rules]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold text-brand-ink">Alert Rules</h2>
          <p className="text-sm text-brand-deep/70">{activeCount} active of {rules.length} total</p>
        </div>
        <button className="rounded bg-brand-deep px-3 py-2 text-sm text-white" onClick={() => setShowCreate(true)}>
          Create Rule
        </button>
      </div>

      <div className="bg-white border border-brand-deep/10 rounded-xl shadow-soft overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-brand-sand/60">
            <tr>
              <th className="text-left px-3 py-2">Name</th>
              <th className="text-left px-3 py-2">Category</th>
              <th className="text-left px-3 py-2">Priority</th>
              <th className="text-left px-3 py-2">Status</th>
              <th className="text-left px-3 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {rules.map((rule) => (
              <tr key={rule.rule_id} className="border-t border-brand-deep/10">
                <td className="px-3 py-2">
                  <p className="font-semibold text-brand-ink">{rule.name}</p>
                  <p className="text-xs text-brand-deep/70">{rule.description || '-'}</p>
                </td>
                <td className="px-3 py-2">{rule.category}</td>
                <td className="px-3 py-2">{rule.priority}</td>
                <td className="px-3 py-2">{rule.is_active ? 'Active' : 'Inactive'}</td>
                <td className="px-3 py-2">
                  <div className="flex gap-2">
                    <button
                      className="rounded border border-brand-deep/20 px-2 py-1 text-xs"
                      onClick={async () => {
                        await alertsService.updateRule(rule.rule_id, { is_active: !rule.is_active });
                        await load();
                      }}
                    >
                      {rule.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                    <button
                      className="rounded border border-red-300 px-2 py-1 text-xs text-red-700"
                      onClick={async () => {
                        await alertsService.deleteRule(rule.rule_id);
                        await load();
                      }}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!isLoading && rules.length === 0 && <p className="px-3 py-3 text-sm text-brand-deep/70">No rules configured yet.</p>}
        {isLoading && <p className="px-3 py-3 text-sm text-brand-deep/70">Loading rules...</p>}
      </div>

      {showCreate && (
        <div className="fixed inset-0 bg-brand-ink/60 flex items-center justify-center p-4">
          <div className="w-full max-w-3xl bg-white rounded-xl shadow-soft p-4 space-y-3">
            <h3 className="text-xl font-semibold text-brand-ink">Create Alert Rule</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <input className="rounded border border-brand-deep/20 px-3 py-2 text-sm" placeholder="Rule Name" value={draft.name} onChange={(e) => setDraft({ ...draft, name: e.target.value })} />
              <select className="rounded border border-brand-deep/20 px-3 py-2 text-sm" value={draft.category} onChange={(e) => setDraft({ ...draft, category: e.target.value })}>
                {CATEGORY_OPTIONS.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
              <input className="rounded border border-brand-deep/20 px-3 py-2 text-sm" placeholder="Condition field" value={draft.field} onChange={(e) => setDraft({ ...draft, field: e.target.value })} />
              <select className="rounded border border-brand-deep/20 px-3 py-2 text-sm" value={draft.operator} onChange={(e) => setDraft({ ...draft, operator: e.target.value })}>
                {OPERATOR_OPTIONS.map((op) => <option key={op} value={op}>{op}</option>)}
              </select>
              <input className="rounded border border-brand-deep/20 px-3 py-2 text-sm" placeholder="Condition value" value={draft.value} onChange={(e) => setDraft({ ...draft, value: e.target.value })} />
              <input className="rounded border border-brand-deep/20 px-3 py-2 text-sm" placeholder="Priority (1-4)" type="number" min={1} max={4} value={draft.priority} onChange={(e) => setDraft({ ...draft, priority: Number(e.target.value) })} />
              <select className="rounded border border-brand-deep/20 px-3 py-2 text-sm" value={draft.actionType} onChange={(e) => setDraft({ ...draft, actionType: e.target.value as RuleDraft['actionType'] })}>
                <option value="in_app">In-App</option>
                <option value="email">Email</option>
                <option value="webhook">Webhook</option>
                <option value="auto_resolve">Auto Resolve</option>
                <option value="auto_assign">Auto Assign</option>
              </select>
              <select
                className="rounded border border-brand-deep/20 px-3 py-2 text-sm"
                value={draft.escalation_policy_id || ''}
                onChange={(e) => setDraft({ ...draft, escalation_policy_id: e.target.value ? Number(e.target.value) : undefined })}
              >
                <option value="">No Escalation Policy</option>
                {policies.map((policy) => <option key={policy.policy_id} value={policy.policy_id}>{policy.name}</option>)}
              </select>
            </div>

            <textarea className="w-full rounded border border-brand-deep/20 px-3 py-2 text-sm" rows={2} placeholder="Description" value={draft.description} onChange={(e) => setDraft({ ...draft, description: e.target.value })} />

            {(draft.actionType === 'in_app' || draft.actionType === 'email') && (
              <input
                className="w-full rounded border border-brand-deep/20 px-3 py-2 text-sm"
                placeholder={draft.actionType === 'in_app' ? 'Recipient user IDs (comma separated)' : 'Recipient emails (comma separated)'}
                value={draft.recipients}
                onChange={(e) => setDraft({ ...draft, recipients: e.target.value })}
              />
            )}

            {draft.actionType === 'webhook' && (
              <input className="w-full rounded border border-brand-deep/20 px-3 py-2 text-sm" placeholder="Webhook URL" value={draft.webhookUrl} onChange={(e) => setDraft({ ...draft, webhookUrl: e.target.value })} />
            )}

            <div className="flex justify-end gap-2">
              <button className="rounded border border-brand-deep/20 px-3 py-2 text-sm" onClick={() => setShowCreate(false)}>Cancel</button>
              <button
                className="rounded bg-brand-deep px-3 py-2 text-sm text-white disabled:opacity-60"
                disabled={!draft.name.trim()}
                onClick={() => void createRule()}
              >
                Create Rule
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
