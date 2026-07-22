import { useEffect, useState } from 'react';

import { alertsService, type AlertNotification } from '../../api/alertsService';

export default function NotificationCenter() {
  const [notifications, setNotifications] = useState<AlertNotification[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const load = async () => {
    setIsLoading(true);
    try {
      setNotifications(await alertsService.listNotifications({ limit: 100 }));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const typeClass = (type: AlertNotification['type']) => {
    if (type === 'EMAIL') return 'bg-blue-100 text-blue-800';
    if (type === 'WEBHOOK') return 'bg-amber-100 text-amber-800';
    return 'bg-emerald-100 text-emerald-800';
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-brand-ink">Notification Center</h2>
        <button className="rounded bg-brand-deep px-3 py-2 text-sm text-white" onClick={() => void load()}>Refresh</button>
      </div>

      <div className="space-y-3">
        {isLoading && <p className="text-sm text-brand-deep/70">Loading notifications...</p>}
        {!isLoading && notifications.length === 0 && <p className="text-sm text-brand-deep/70">No notifications available.</p>}

        {notifications.map((notification) => (
          <div key={notification.notification_id} className={`bg-white border rounded-xl p-4 shadow-soft ${notification.read ? 'border-brand-deep/10' : 'border-brand-mint/40'}`}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <p className="font-semibold text-brand-ink">{notification.subject}</p>
                  <span className={`px-2 py-0.5 rounded text-xs ${typeClass(notification.type)}`}>{notification.type}</span>
                  {!notification.delivered && <span className="px-2 py-0.5 rounded text-xs bg-red-100 text-red-700">Delivery Failed</span>}
                </div>
                <p className="text-sm text-brand-deep/80 mt-1 whitespace-pre-wrap">{notification.content}</p>
                <p className="text-xs text-brand-deep/60 mt-2">{notification.sent_at ? new Date(notification.sent_at).toLocaleString() : '-'}</p>
                {!notification.delivered && notification.error_message && (
                  <p className="text-xs text-red-700 mt-1">{notification.error_message}</p>
                )}
              </div>
              {!notification.read && (
                <button
                  className="rounded border border-brand-deep/20 px-2 py-1 text-xs"
                  onClick={async () => {
                    await alertsService.markNotificationRead(notification.notification_id);
                    await load();
                  }}
                >
                  Mark Read
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
