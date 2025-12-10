import { useState } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/Table';
import { Dialog, DialogTitle, DialogDescription, DialogCloseButton } from '@/components/ui/Dialog';
import { Form, FormField, FormLabel, FormDescription } from '@/components/ui/Form';
import { Select } from '@/components/ui/Select';
import { Alert, AlertDescription } from '@/components/ui/Alert';
import { PlusIcon, TrashIcon, EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { formatDateTime } from '@/lib/utils';

interface ApiKey {
  id: string;
  name: string;
  key: string;
  scope: 'read' | 'write' | 'admin';
  lastUsed?: Date;
  createdAt: Date;
}

export default function ApiKeys() {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([
    {
      id: '1',
      name: 'Production API Key',
      key: 'sk_live_xxxxxxxxxxxxx',
      scope: 'write',
      lastUsed: new Date(),
      createdAt: new Date(),
    },
  ]);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [newKeyScope, setNewKeyScope] = useState<'read' | 'write' | 'admin'>('read');
  const [visibleKeys, setVisibleKeys] = useState<Set<string>>(new Set());
  const [createdKey, setCreatedKey] = useState<string | null>(null);

  const handleCreateKey = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName.trim()) {
      toast.error('Key name is required');
      return;
    }

    const generatedKey = `sk_${newKeyScope}_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
    const apiKey: ApiKey = {
      id: Date.now().toString(),
      name: newKeyName,
      key: generatedKey,
      scope: newKeyScope,
      createdAt: new Date(),
    };

    setApiKeys([...apiKeys, apiKey]);
    setCreatedKey(generatedKey);
    setNewKeyName('');
    setNewKeyScope('read');
    toast.success('API key created successfully');
  };

  const handleDeleteKey = (id: string) => {
    setApiKeys(apiKeys.filter((k) => k.id !== id));
    toast.success('API key deleted');
  };

  const toggleKeyVisibility = (id: string) => {
    const newVisible = new Set(visibleKeys);
    if (newVisible.has(id)) {
      newVisible.delete(id);
    } else {
      newVisible.add(id);
    }
    setVisibleKeys(newVisible);
  };

  const maskKey = (key: string) => {
    return `${key.substring(0, 8)}${'•'.repeat(20)}`;
  };

  const getScopeBadge = (scope: ApiKey['scope']) => {
    const variants = {
      read: 'info',
      write: 'warning',
      admin: 'destructive',
    } as const;
    return <Badge variant={variants[scope]}>{scope}</Badge>;
  };

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-3xl font-bold">API Keys</h1>
                <p className="text-muted-foreground mt-1">
                  Manage your API keys for programmatic access
                </p>
              </div>
              <Button onClick={() => setIsCreateDialogOpen(true)}>
                <PlusIcon className="h-4 w-4 mr-2" />
                Create API Key
              </Button>
            </div>

            <Alert variant="info" className="mb-6">
              <AlertDescription>
                Keep your API keys secure and never share them publicly. Each key provides access to
                your account based on its scope.
              </AlertDescription>
            </Alert>

            <Card>
              <CardHeader>
                <CardTitle>Your API Keys</CardTitle>
                <CardDescription>
                  {apiKeys.length} active {apiKeys.length === 1 ? 'key' : 'keys'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Key</TableHead>
                      <TableHead>Scope</TableHead>
                      <TableHead>Last Used</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {apiKeys.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                          No API keys yet. Create your first one!
                        </TableCell>
                      </TableRow>
                    ) : (
                      apiKeys.map((apiKey) => (
                        <TableRow key={apiKey.id}>
                          <TableCell className="font-medium">{apiKey.name}</TableCell>
                          <TableCell>
                            <code className="text-sm font-mono">
                              {visibleKeys.has(apiKey.id) ? apiKey.key : maskKey(apiKey.key)}
                            </code>
                          </TableCell>
                          <TableCell>{getScopeBadge(apiKey.scope)}</TableCell>
                          <TableCell>
                            {apiKey.lastUsed ? formatDateTime(apiKey.lastUsed) : 'Never'}
                          </TableCell>
                          <TableCell>{formatDateTime(apiKey.createdAt)}</TableCell>
                          <TableCell>
                            <div className="flex items-center justify-end gap-2">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => toggleKeyVisibility(apiKey.id)}
                                title={visibleKeys.has(apiKey.id) ? 'Hide key' : 'Show key'}
                              >
                                {visibleKeys.has(apiKey.id) ? (
                                  <EyeSlashIcon className="h-4 w-4" />
                                ) : (
                                  <EyeIcon className="h-4 w-4" />
                                )}
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDeleteKey(apiKey.id)}
                                title="Delete key"
                              >
                                <TrashIcon className="h-4 w-4 text-destructive" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>

      {/* Create API Key Dialog */}
      <Dialog
        open={isCreateDialogOpen}
        onClose={() => {
          setIsCreateDialogOpen(false);
          setCreatedKey(null);
        }}
      >
        <DialogCloseButton
          onClose={() => {
            setIsCreateDialogOpen(false);
            setCreatedKey(null);
          }}
        />
        
        {createdKey ? (
          <>
            <DialogTitle>API Key Created</DialogTitle>
            <DialogDescription>
              Make sure to copy your API key now. You won&apos;t be able to see it again!
            </DialogDescription>

            <div className="mt-4 space-y-4">
              <Alert variant="warning">
                <AlertDescription>
                  Store this key securely. Anyone with this key can access your account.
                </AlertDescription>
              </Alert>

              <div className="p-4 bg-muted rounded-md">
                <code className="text-sm font-mono break-all">{createdKey}</code>
              </div>

              <div className="flex gap-3 justify-end">
                <Button
                  onClick={() => {
                    navigator.clipboard.writeText(createdKey);
                    toast.success('API key copied to clipboard');
                  }}
                >
                  Copy to Clipboard
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setIsCreateDialogOpen(false);
                    setCreatedKey(null);
                  }}
                >
                  Done
                </Button>
              </div>
            </div>
          </>
        ) : (
          <>
            <DialogTitle>Create New API Key</DialogTitle>
            <DialogDescription>
              Create a new API key for programmatic access to your account
            </DialogDescription>

            <Form onSubmit={handleCreateKey} className="mt-4">
              <FormField>
                <FormLabel htmlFor="keyName" required>
                  Key Name
                </FormLabel>
                <Input
                  id="keyName"
                  value={newKeyName}
                  onChange={(e) => setNewKeyName(e.target.value)}
                  placeholder="e.g., Production API Key"
                  required
                />
                <FormDescription>
                  A descriptive name to help you identify this key
                </FormDescription>
              </FormField>

              <FormField>
                <FormLabel htmlFor="keyScope" required>
                  Scope
                </FormLabel>
                <Select
                  id="keyScope"
                  value={newKeyScope}
                  onChange={(e) => setNewKeyScope(e.target.value as 'read' | 'write' | 'admin')}
                  options={[
                    { value: 'read', label: 'Read - View data only' },
                    { value: 'write', label: 'Write - Create and modify data' },
                    { value: 'admin', label: 'Admin - Full access' },
                  ]}
                />
                <FormDescription>
                  Choose the level of access for this API key
                </FormDescription>
              </FormField>

              <div className="flex gap-3 justify-end mt-6">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsCreateDialogOpen(false)}
                >
                  Cancel
                </Button>
                <Button type="submit">Create Key</Button>
              </div>
            </Form>
          </>
        )}
      </Dialog>
    </div>
  );
}
