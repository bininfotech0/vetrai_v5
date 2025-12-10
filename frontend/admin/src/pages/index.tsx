import { useState } from 'react';
import { AdminLayout } from '@/components/layout/AdminLayout';
import { StatsCards } from '@/components/dashboard/StatsCards';
import { RecentActivity } from '@/components/dashboard/RecentActivity';
import { SystemHealth } from '@/components/dashboard/SystemHealth';
import { UserGrowthChart } from '@/components/dashboard/UserGrowthChart';

export default function Dashboard() {
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome to the VetrAI Admin Dashboard
          </p>
        </div>

        {/* Stats Cards */}
        <StatsCards />

        {/* Charts and Data */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <UserGrowthChart />
          </div>
          <div>
            <SystemHealth />
          </div>
        </div>

        {/* Recent Activity */}
        <RecentActivity />
      </div>
    </AdminLayout>
  );
}