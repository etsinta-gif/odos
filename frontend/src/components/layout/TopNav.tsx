import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useTenant } from '../../context/TenantContext';

export function TopNav() {
  const { user, logout } = useAuth();
  const { companies, currentCompany, setCurrentCompany } = useTenant();
  const navigate = useNavigate();

  const onLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="bg-white/80 backdrop-blur border-b border-brand-deep/10 px-6 py-4 flex items-center justify-between">
      <div>
        <p className="text-xs uppercase tracking-widest text-brand-deep/60">Hybrid ETL</p>
        <h1 className="text-lg font-semibold text-brand-ink">Operations Console</h1>
      </div>

      <div className="flex items-center gap-4">
        {companies.length > 0 && (
          <select
            className="rounded border border-brand-deep/20 px-2 py-1 text-sm"
            value={currentCompany?.company_id || ''}
            onChange={(e) => {
              const selected = companies.find((c) => c.company_id === Number(e.target.value));
              if (selected) {
                setCurrentCompany(selected);
              }
            }}
          >
            {companies.map((company) => (
              <option key={company.company_id} value={company.company_id}>
                {company.company_name}
              </option>
            ))}
          </select>
        )}

        <div className="text-right">
          <p className="text-sm font-semibold text-brand-ink">{user?.full_name || user?.username}</p>
          <p className="text-xs text-brand-deep/70">{user?.roles?.join(', ') || 'User'}</p>
        </div>
        <button onClick={onLogout} className="rounded bg-brand-deep px-3 py-1.5 text-sm text-white hover:bg-brand-mint">
          Logout
        </button>
      </div>
    </header>
  );
}
