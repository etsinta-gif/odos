import { Link, useLocation } from 'react-router-dom';

const LABELS: Record<string, string> = {
  dashboard: 'Dashboard',
  redflags: 'Red Flags',
  masters: 'Masters',
  etl: 'ETL',
  upload: 'Upload',
  mapping: 'Mapping Approval',
};

function segmentLabel(segment: string): string {
  if (LABELS[segment]) {
    return LABELS[segment];
  }
  return segment
    .split('-')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

export function Breadcrumbs() {
  const location = useLocation();
  const parts = location.pathname.split('/').filter(Boolean);

  if (parts.length === 0) {
    return null;
  }

  return (
    <nav aria-label="Breadcrumb" className="px-6 py-3 text-sm text-brand-deep/70 border-b border-brand-deep/10 bg-white/70">
      <ol className="flex flex-wrap items-center gap-2">
        <li>
          <Link to="/dashboard" className="hover:text-brand-deep hover:underline">
            Home
          </Link>
        </li>
        {parts.map((part, index) => {
          const path = `/${parts.slice(0, index + 1).join('/')}`;
          const isLast = index === parts.length - 1;
          return (
            <li key={path} className="flex items-center gap-2">
              <span>/</span>
              {isLast ? (
                <span className="font-medium text-brand-ink">{segmentLabel(part)}</span>
              ) : (
                <Link to={path} className="hover:text-brand-deep hover:underline">
                  {segmentLabel(part)}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
