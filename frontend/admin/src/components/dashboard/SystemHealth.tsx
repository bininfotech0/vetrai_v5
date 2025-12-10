import React from 'react';

export function SystemHealth() {
  const services = [
    { name: 'Auth Service', status: 'healthy', uptime: '99.9%' },
    { name: 'Tenancy Service', status: 'healthy', uptime: '99.8%' },
    { name: 'Workers Service', status: 'healthy', uptime: '99.7%' },
    { name: 'Database', status: 'healthy', uptime: '99.9%' },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 bg-green-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'error':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow border">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">System Health</h2>
      <div className="space-y-3">
        {services.map((service, index) => (
          <div key={index} className="flex items-center justify-between">
            <div className="flex items-center">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                {service.status}
              </span>
              <span className="ml-3 text-sm text-gray-900">{service.name}</span>
            </div>
            <span className="text-sm text-gray-500">{service.uptime}</span>
          </div>
        ))}
      </div>
    </div>
  );
}