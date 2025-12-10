# VetrAI Studio UI Components Documentation

## Overview

This document provides comprehensive documentation for all UI components in the VetrAI Studio application. All components are built with accessibility, responsiveness, and theming in mind.

## Core UI Components

### Button

A versatile button component with multiple variants and sizes.

**Props:**
- `variant`: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
- `size`: 'default' | 'sm' | 'lg' | 'icon'

**Example:**
```tsx
import { Button } from '@/components/ui/Button';

<Button variant="primary" size="lg">Click me</Button>
<Button variant="outline" size="sm">Secondary action</Button>
<Button variant="ghost" size="icon"><Icon /></Button>
```

**Accessibility:**
- Full keyboard navigation support
- Proper ARIA attributes
- Focus visible states

---

### Input

Text input component with consistent styling and validation support.

**Props:**
- All standard HTML input attributes
- `className`: Additional CSS classes

**Example:**
```tsx
import { Input } from '@/components/ui/Input';

<Input
  type="email"
  placeholder="Enter your email"
  required
  aria-label="Email address"
/>
```

**Accessibility:**
- Proper label associations
- ARIA attributes for validation states
- Focus management

---

### Card

Container component for grouping related content.

**Components:**
- `Card`: Main container
- `CardHeader`: Header section
- `CardTitle`: Title text
- `CardDescription`: Description text
- `CardContent`: Main content area
- `CardFooter`: Footer section

**Example:**
```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Content */}
  </CardContent>
</Card>
```

---

### Dialog (Modal)

Accessible modal dialog component using Headless UI.

**Components:**
- `Dialog`: Main dialog wrapper
- `DialogTitle`: Dialog title
- `DialogDescription`: Dialog description
- `DialogCloseButton`: Close button

**Example:**
```tsx
import { Dialog, DialogTitle, DialogDescription, DialogCloseButton } from '@/components/ui/Dialog';

<Dialog open={isOpen} onClose={() => setIsOpen(false)}>
  <DialogCloseButton onClose={() => setIsOpen(false)} />
  <DialogTitle>Confirm Action</DialogTitle>
  <DialogDescription>
    Are you sure you want to proceed?
  </DialogDescription>
  {/* Dialog content */}
</Dialog>
```

**Accessibility:**
- Keyboard trap when open
- ESC key to close
- Proper focus management
- ARIA roles and attributes

---

### Table

Semantic table component for displaying tabular data.

**Components:**
- `Table`: Main table wrapper
- `TableHeader`: Table header section
- `TableBody`: Table body section
- `TableRow`: Table row
- `TableHead`: Header cell
- `TableCell`: Body cell
- `TableCaption`: Table caption

**Example:**
```tsx
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/Table';

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Item 1</TableCell>
      <TableCell>Active</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

---

### Tabs

Tabbed interface component using Headless UI.

**Components:**
- `Tabs`: Main tabs wrapper
- `TabsList`: Tab list container
- `TabsTrigger`: Individual tab button
- `TabsContent`: Tab panel content

**Example:**
```tsx
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs';

<Tabs defaultIndex={0}>
  <TabsList>
    <TabsTrigger>Tab 1</TabsTrigger>
    <TabsTrigger>Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent>Content 1</TabsContent>
  <TabsContent>Content 2</TabsContent>
</Tabs>
```

**Accessibility:**
- Keyboard navigation (arrow keys)
- Proper ARIA roles
- Focus management

---

### Form Components

#### Form

Form wrapper with consistent spacing.

**Components:**
- `Form`: Form wrapper
- `FormField`: Field container
- `FormLabel`: Field label
- `FormMessage`: Validation message
- `FormDescription`: Helper text

**Example:**
```tsx
import { Form, FormField, FormLabel, FormMessage } from '@/components/ui/Form';
import { Input } from '@/components/ui/Input';

<Form onSubmit={handleSubmit}>
  <FormField>
    <FormLabel htmlFor="email" required>Email</FormLabel>
    <Input id="email" type="email" />
    <FormMessage error>Email is required</FormMessage>
  </FormField>
</Form>
```

#### Select

Dropdown select component with custom styling.

**Example:**
```tsx
import { Select } from '@/components/ui/Select';

<Select
  options={[
    { value: '1', label: 'Option 1' },
    { value: '2', label: 'Option 2' },
  ]}
/>
```

#### Textarea

Multi-line text input component.

**Example:**
```tsx
import { Textarea } from '@/components/ui/Textarea';

<Textarea
  placeholder="Enter description..."
  rows={4}
/>
```

#### Checkbox

Checkbox input with label support.

**Example:**
```tsx
import { Checkbox } from '@/components/ui/Checkbox';

<Checkbox label="I agree to the terms" />
```

---

### Badge

Small label component for status and categories.

**Props:**
- `variant`: 'default' | 'secondary' | 'destructive' | 'outline' | 'success' | 'warning' | 'info'

**Example:**
```tsx
import { Badge } from '@/components/ui/Badge';

<Badge variant="success">Active</Badge>
<Badge variant="warning">Pending</Badge>
<Badge variant="destructive">Error</Badge>
```

---

### Alert

Alert message component for important information.

**Components:**
- `Alert`: Main alert container
- `AlertTitle`: Alert title
- `AlertDescription`: Alert content

**Props:**
- `variant`: 'default' | 'destructive' | 'warning' | 'success' | 'info'
- `showIcon`: boolean (default: true)

**Example:**
```tsx
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/Alert';

<Alert variant="warning">
  <AlertTitle>Warning</AlertTitle>
  <AlertDescription>
    This action cannot be undone.
  </AlertDescription>
</Alert>
```

---

### Tooltip

Hover tooltip component.

**Props:**
- `content`: React.ReactNode - Tooltip content
- `position`: 'top' | 'bottom' | 'left' | 'right'

**Example:**
```tsx
import { Tooltip } from '@/components/ui/Tooltip';

<Tooltip content="This is a tooltip" position="top">
  <Button>Hover me</Button>
</Tooltip>
```

---

### LoadingSpinner

Loading indicator component.

**Props:**
- `size`: 'sm' | 'md' | 'lg'

**Example:**
```tsx
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

<LoadingSpinner size="lg" />
```

---

### ThemeToggle

Dark/light mode toggle button.

**Example:**
```tsx
import { ThemeToggle } from '@/components/ui/ThemeToggle';

<ThemeToggle />
```

**Features:**
- Persists preference to localStorage
- Respects system preference on first load
- Smooth transitions between themes

---

## Layout Components

### Sidebar

Responsive navigation sidebar.

**Features:**
- Collapsible on desktop
- Slide-out drawer on mobile
- Active route highlighting
- User profile display

**Usage:**
```tsx
import { Sidebar } from '@/components/layout/Sidebar';

<Sidebar />
```

---

### Header

Application header with navigation and user menu.

**Features:**
- Theme toggle
- Notifications
- User menu with profile and logout
- Responsive design

**Usage:**
```tsx
import { Header } from '@/components/layout/Header';

<Header />
```

---

## Utility Components

### ErrorBoundary

Error boundary component for catching React errors.

**Example:**
```tsx
import { ErrorBoundary } from '@/components/ErrorBoundary';

<ErrorBoundary fallback={<div>Something went wrong</div>}>
  <YourComponent />
</ErrorBoundary>
```

---

## Theming

All components support theming through CSS variables. The theme can be customized by modifying the values in `globals.css`.

**CSS Variables:**
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  /* ... more variables */
}
```

**Dark Mode:**
Dark mode is automatically applied when the `.dark` class is added to the root element.

---

## Accessibility Guidelines

All components follow WCAG 2.1 Level AA standards:

1. **Keyboard Navigation**: All interactive elements are keyboard accessible
2. **Focus Management**: Proper focus indicators and logical tab order
3. **ARIA Attributes**: Appropriate ARIA roles and attributes
4. **Color Contrast**: Sufficient contrast ratios for text and UI elements
5. **Screen Readers**: Semantic HTML and ARIA labels for screen reader support

---

## Best Practices

1. **Always use semantic HTML**: Use proper HTML elements for their intended purpose
2. **Provide labels**: Always associate labels with form inputs
3. **Handle errors**: Display clear error messages and validation states
4. **Loading states**: Show loading indicators for async operations
5. **Responsive design**: Test on multiple screen sizes
6. **Accessibility**: Test with keyboard navigation and screen readers

---

## Contributing

When creating new components:

1. Follow existing component patterns
2. Include proper TypeScript types
3. Add accessibility features
4. Support theming
5. Make components responsive
6. Document usage with examples
7. Test across browsers and devices
