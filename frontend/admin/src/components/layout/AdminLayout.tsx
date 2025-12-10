import React from 'react';

interface AdminLayoutProps {
  children: React.ReactNode;
}

export function AdminLayout({ children }: AdminLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-2xl font-bold text-gray-900">VetrAI Admin</h1>
            <nav className="space-x-8">
              <a href="/" className="text-gray-600 hover:text-gray-900">Dashboard</a>
              <a href="/users" className="text-gray-600 hover:text-gray-900">Users</a>
              <a href="/organizations" className="text-gray-600 hover:text-gray-900">Organizations</a>
              <a href="/billing" className="text-gray-600 hover:text-gray-900">Billing</a>
              <a href="/support" className="text-gray-600 hover:text-gray-900">Support</a>
              <a href="/settings" className="text-gray-600 hover:text-gray-900">Settings</a>
            </nav>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}