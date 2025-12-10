import * as React from 'react';
import { Tab } from '@headlessui/react';
import { cn } from '@/lib/utils';

interface TabsProps {
  children: React.ReactNode;
  defaultIndex?: number;
  onChange?: (index: number) => void;
  className?: string;
}

export function Tabs({ children, defaultIndex = 0, onChange, className }: TabsProps) {
  return (
    <Tab.Group defaultIndex={defaultIndex} onChange={onChange}>
      <div className={cn('w-full', className)}>{children}</div>
    </Tab.Group>
  );
}

interface TabsListProps {
  children: React.ReactNode;
  className?: string;
}

export function TabsList({ children, className }: TabsListProps) {
  return (
    <Tab.List
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground',
        className
      )}
    >
      {children}
    </Tab.List>
  );
}

interface TabsTriggerProps {
  children: React.ReactNode;
  className?: string;
}

export function TabsTrigger({ children, className }: TabsTriggerProps) {
  return (
    <Tab
      className={({ selected }) =>
        cn(
          'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
          selected
            ? 'bg-background text-foreground shadow-sm'
            : 'text-muted-foreground hover:bg-background/50',
          className
        )
      }
    >
      {children}
    </Tab>
  );
}

interface TabsContentProps {
  children: React.ReactNode;
  className?: string;
}

export function TabsContent({ children, className }: TabsContentProps) {
  return (
    <Tab.Panel
      className={cn(
        'mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        className
      )}
    >
      {children}
    </Tab.Panel>
  );
}
