import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  HomeIcon,
  ArrowUpTrayIcon,
  ExclamationTriangleIcon,
  BuildingOfficeIcon,
  AdjustmentsHorizontalIcon,
  ChartBarIcon,
  PresentationChartLineIcon,
  RectangleGroupIcon,
  BellAlertIcon,
  BellIcon,
  ClipboardDocumentListIcon,
  ChevronDoubleLeftIcon,
  ChevronDoubleRightIcon,
} from '@heroicons/react/24/outline';

type MenuItem = { name: string; href: string; icon: React.ComponentType<React.SVGProps<SVGSVGElement>> };

const menuByRole: Record<string, MenuItem[]> = {
  ADMIN: [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'ETL Upload', href: '/masters/etl/upload', icon: ArrowUpTrayIcon },
    { name: 'Red Flags', href: '/dashboard/redflags', icon: ExclamationTriangleIcon },
    { name: 'Party Defaults', href: '/dashboard/party-defaults', icon: AdjustmentsHorizontalIcon },
    { name: 'Reports', href: '/reports', icon: ChartBarIcon },
    { name: 'Dashboards', href: '/dashboards', icon: RectangleGroupIcon },
    { name: 'Trends', href: '/trends', icon: PresentationChartLineIcon },
    { name: 'Alert Rules', href: '/alerts/rules', icon: BellAlertIcon },
    { name: 'Notifications', href: '/alerts/notifications', icon: BellIcon },
    { name: 'Alert Audit', href: '/alerts/audit', icon: ClipboardDocumentListIcon },
  ],
  OPS: [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'ETL Upload', href: '/masters/etl/upload', icon: ArrowUpTrayIcon },
    { name: 'Red Flags', href: '/dashboard/redflags', icon: ExclamationTriangleIcon },
    { name: 'Party Defaults', href: '/dashboard/party-defaults', icon: AdjustmentsHorizontalIcon },
    { name: 'Reports', href: '/reports', icon: ChartBarIcon },
    { name: 'Alert Rules', href: '/alerts/rules', icon: BellAlertIcon },
    { name: 'Notifications', href: '/alerts/notifications', icon: BellIcon },
    { name: 'Alert Audit', href: '/alerts/audit', icon: ClipboardDocumentListIcon },
  ],
  FINANCE: [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Red Flags', href: '/dashboard/redflags', icon: ExclamationTriangleIcon },
    { name: 'Reports', href: '/reports', icon: ChartBarIcon },
    { name: 'Dashboards', href: '/dashboards', icon: RectangleGroupIcon },
    { name: 'Trends', href: '/trends', icon: PresentationChartLineIcon },
    { name: 'Notifications', href: '/alerts/notifications', icon: BellIcon },
    { name: 'Alert Audit', href: '/alerts/audit', icon: ClipboardDocumentListIcon },
  ],
  AUDITOR: [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Red Flags', href: '/dashboard/redflags', icon: ExclamationTriangleIcon },
    { name: 'Reports', href: '/reports', icon: ChartBarIcon },
    { name: 'Trends', href: '/trends', icon: PresentationChartLineIcon },
    { name: 'Notifications', href: '/alerts/notifications', icon: BellIcon },
    { name: 'Alert Audit', href: '/alerts/audit', icon: ClipboardDocumentListIcon },
  ],
};

type SidebarProps = {
  collapsed: boolean;
  onToggle: () => void;
};

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const { user } = useAuth();
  const role = user?.roles?.[0] || 'OPS';
  const items = menuByRole[role] || menuByRole.OPS;

  return (
    <aside className={`${collapsed ? 'w-20' : 'w-72'} min-h-screen bg-brand-deep text-white transition-all duration-200`}>
      <div className="p-4 border-b border-white/20">
        <div className="flex items-center justify-between gap-2">
          <div className="text-2xl font-bold tracking-wide">{collapsed ? 'OD' : 'ODOS'}</div>
          <button
            type="button"
            onClick={onToggle}
            className="rounded border border-white/30 p-1 text-white/90 hover:bg-white/10"
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {collapsed ? <ChevronDoubleRightIcon className="w-4 h-4" /> : <ChevronDoubleLeftIcon className="w-4 h-4" />}
          </button>
        </div>
        <div className={`mt-1 text-xs text-white/70 ${collapsed ? 'hidden' : 'flex'} items-center gap-2`}>
          <BuildingOfficeIcon className="w-4 h-4" />
          Finance Ops Platform
        </div>
      </div>
      <nav className="p-4 space-y-2">
        {items.map((item) => (
          <NavLink
            key={item.href}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center ${collapsed ? 'justify-center' : 'gap-3'} rounded-lg px-3 py-2 text-sm ${
                isActive ? 'bg-brand-mint text-white' : 'text-white/80 hover:bg-white/10 hover:text-white'
              }`
            }
            title={item.name}
          >
            <item.icon className="w-5 h-5" />
            {!collapsed && item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
