import React from 'react';

export function StatsCards() {
  const stats = [
    { name: 'Total Users', value: '12,345', change: '+12%', trend: 'up' },
    { name: 'Active Organizations', value: '1,234', change: '+5%', trend: 'up' },
    { name: 'Monthly Revenue', value: '$45,678', change: '+18%', trend: 'up' },
    { name: 'Support Tickets', value: '23', change: '-8%', trend: 'down' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div key={stat.name} className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{stat.name}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
            <div className={`text-sm font-medium ${
              stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
            }`}>
              {stat.change}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}