import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/Button';
import {
  HomeIcon,
  CogIcon,
  PlayIcon,
  DocumentIcon,
  KeyIcon,
  UserGroupIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from '@heroicons/react/24/outline';
import { cn } from '@/lib/utils';
import Link from 'next/link';
import { useRouter } from 'next/router';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Workflows', href: '/workflows', icon: PlayIcon },
  { name: 'Templates', href: '/templates', icon: DocumentIcon },
  { name: 'API Keys', href: '/keys', icon: KeyIcon },
  { name: 'Team', href: '/team', icon: UserGroupIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const { user } = useAuth();
  const router = useRouter();

  return (
    <div className={cn(
      'bg-card border-r border-border flex flex-col transition-all duration-300',
      collapsed ? 'w-16' : 'w-64'
    )}>
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <h1 className="text-xl font-bold text-primary">VetrAI</h1>
          )}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCollapsed(!collapsed)}
            className="h-8 w-8"
          >
            {collapsed ? (
              <ChevronRightIcon className="h-4 w-4" />
            ) : (
              <ChevronLeftIcon className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item) => {
          const isActive = router.pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
                collapsed && 'justify-center'
              )}
            >
              <item.icon className={cn('h-5 w-5', !collapsed && 'mr-3')} />
              {!collapsed && item.name}
            </Link>
          );
        })}
      </nav>

      {/* User Info */}
      {!collapsed && user && (
        <div className="p-4 border-t border-border">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-medium">
                {user.firstName.charAt(0)}{user.lastName.charAt(0)}
              </div>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium">{user.firstName} {user.lastName}</p>
              <p className="text-xs text-muted-foreground">{user.role.replace('_', ' ')}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}