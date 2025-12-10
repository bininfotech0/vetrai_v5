import React from 'react';

export function RecentActivity() {
  const activities = [
    { id: 1, user: 'John Doe', action: 'Created new workflow', time: '2 minutes ago' },
    { id: 2, user: 'Jane Smith', action: 'Updated organization settings', time: '15 minutes ago' },
    { id: 3, user: 'Bob Johnson', action: 'Generated API key', time: '1 hour ago' },
    { id: 4, user: 'Alice Wilson', action: 'Submitted support ticket', time: '2 hours ago' },
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow border">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
      <div className="space-y-4">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
            <div>
              <p className="text-sm font-medium text-gray-900">{activity.user}</p>
              <p className="text-sm text-gray-600">{activity.action}</p>
            </div>
            <span className="text-xs text-gray-500">{activity.time}</span>
          </div>
        ))}
      </div>
    </div>
  );
}