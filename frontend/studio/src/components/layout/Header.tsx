import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/Button';
import {
  BellIcon,
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/react/24/outline';
import { Menu, Transition } from '@headlessui/react';
import { Fragment } from 'react';
import { cn } from '@/lib/utils';
import { useRouter } from 'next/router';
import toast from 'react-hot-toast';

export function Header() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [notifications] = useState(0); // TODO: Implement notifications

  const handleLogout = async () => {
    try {
      await logout();
      toast.success('Logged out successfully');
      if (router.pathname !== '/login') {
        router.replace('/login');
      }
    } catch (error) {
      toast.error('Error logging out');
    }
  };

  return (
    <header className="bg-card border-b border-border px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <h1 className="text-2xl font-semibold text-foreground">Studio</h1>
        </div>

        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <Button variant="ghost" size="icon" className="relative">
            <BellIcon className="h-5 w-5" />
            {notifications > 0 && (
              <span className="absolute -top-1 -right-1 h-5 w-5 rounded-full bg-destructive text-destructive-foreground text-xs flex items-center justify-center">
                {notifications}
              </span>
            )}
          </Button>

          {/* User Menu */}
          <Menu as="div" className="relative">
            <Menu.Button as={Button} variant="ghost" size="icon">
              <UserIcon className="h-5 w-5" />
            </Menu.Button>

            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 mt-2 w-56 origin-top-right divide-y divide-border rounded-md bg-card border border-border shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <div className="px-4 py-3">
                  <p className="text-sm">Signed in as</p>
                  <p className="text-sm font-medium text-foreground truncate">
                    {user?.email}
                  </p>
                </div>

                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <button
                        className={cn(
                          'flex w-full items-center px-4 py-2 text-sm',
                          active ? 'bg-accent text-accent-foreground' : 'text-foreground'
                        )}
                        onClick={() => router.push('/profile')}
                      >
                        <UserIcon className="mr-3 h-4 w-4" />
                        Your Profile
                      </button>
                    )}
                  </Menu.Item>

                  <Menu.Item>
                    {({ active }) => (
                      <button
                        className={cn(
                          'flex w-full items-center px-4 py-2 text-sm',
                          active ? 'bg-accent text-accent-foreground' : 'text-foreground'
                        )}
                        onClick={() => router.push('/settings')}
                      >
                        <Cog6ToothIcon className="mr-3 h-4 w-4" />
                        Settings
                      </button>
                    )}
                  </Menu.Item>
                </div>

                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <button
                        className={cn(
                          'flex w-full items-center px-4 py-2 text-sm',
                          active ? 'bg-accent text-accent-foreground' : 'text-foreground'
                        )}
                        onClick={handleLogout}
                      >
                        <ArrowRightOnRectangleIcon className="mr-3 h-4 w-4" />
                        Sign out
                      </button>
                    )}
                  </Menu.Item>
                </div>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
    </header>
  );
}