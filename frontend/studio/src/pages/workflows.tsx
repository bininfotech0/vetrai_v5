import { useState } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/Table';
import { Dialog, DialogTitle, DialogDescription, DialogCloseButton } from '@/components/ui/Dialog';
import { Form, FormField, FormLabel, FormMessage } from '@/components/ui/Form';
import { Textarea } from '@/components/ui/Textarea';
import {
  PlusIcon,
  MagnifyingGlassIcon,
  PlayIcon,
  PencilIcon,
  TrashIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { formatDateTime } from '@/lib/utils';

interface Workflow {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive' | 'draft';
  lastRun?: Date;
  createdAt: Date;
}

export default function Workflows() {
  const [workflows, setWorkflows] = useState<Workflow[]>([
    {
      id: '1',
      name: 'Customer Onboarding',
      description: 'Automated customer onboarding workflow',
      status: 'active',
      lastRun: new Date(),
      createdAt: new Date(),
    },
    {
      id: '2',
      name: 'Data Processing Pipeline',
      description: 'Process and analyze customer data',
      status: 'active',
      lastRun: new Date(),
      createdAt: new Date(),
    },
    {
      id: '3',
      name: 'Report Generation',
      description: 'Generate monthly reports',
      status: 'draft',
      createdAt: new Date(),
    },
  ]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newWorkflow, setNewWorkflow] = useState({ name: '', description: '' });

  const filteredWorkflows = workflows.filter(
    (workflow) =>
      workflow.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      workflow.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCreateWorkflow = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWorkflow.name.trim()) {
      toast.error('Workflow name is required');
      return;
    }

    const workflow: Workflow = {
      id: Date.now().toString(),
      name: newWorkflow.name,
      description: newWorkflow.description,
      status: 'draft',
      createdAt: new Date(),
    };

    setWorkflows([...workflows, workflow]);
    setNewWorkflow({ name: '', description: '' });
    setIsCreateDialogOpen(false);
    toast.success('Workflow created successfully');
  };

  const handleDeleteWorkflow = (id: string) => {
    setWorkflows(workflows.filter((w) => w.id !== id));
    toast.success('Workflow deleted');
  };

  const getStatusBadge = (status: Workflow['status']) => {
    const variants = {
      active: 'success',
      inactive: 'secondary',
      draft: 'warning',
    } as const;
    return <Badge variant={variants[status]}>{status}</Badge>;
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
                <h1 className="text-3xl font-bold">Workflows</h1>
                <p className="text-muted-foreground mt-1">
                  Manage and monitor your AI workflows
                </p>
              </div>
              <Button onClick={() => setIsCreateDialogOpen(true)}>
                <PlusIcon className="h-4 w-4 mr-2" />
                Create Workflow
              </Button>
            </div>

            <Card>
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className="relative flex-1">
                    <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search workflows..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                      aria-label="Search workflows"
                    />
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Description</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Last Run</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredWorkflows.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                          {searchQuery ? 'No workflows found' : 'No workflows yet. Create your first one!'}
                        </TableCell>
                      </TableRow>
                    ) : (
                      filteredWorkflows.map((workflow) => (
                        <TableRow key={workflow.id}>
                          <TableCell className="font-medium">{workflow.name}</TableCell>
                          <TableCell>{workflow.description}</TableCell>
                          <TableCell>{getStatusBadge(workflow.status)}</TableCell>
                          <TableCell>
                            {workflow.lastRun ? formatDateTime(workflow.lastRun) : 'Never'}
                          </TableCell>
                          <TableCell>{formatDateTime(workflow.createdAt)}</TableCell>
                          <TableCell>
                            <div className="flex items-center justify-end gap-2">
                              <Button variant="ghost" size="sm" title="Run workflow">
                                <PlayIcon className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm" title="Edit workflow">
                                <PencilIcon className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDeleteWorkflow(workflow.id)}
                                title="Delete workflow"
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

      {/* Create Workflow Dialog */}
      <Dialog open={isCreateDialogOpen} onClose={() => setIsCreateDialogOpen(false)}>
        <DialogCloseButton onClose={() => setIsCreateDialogOpen(false)} />
        <DialogTitle>Create New Workflow</DialogTitle>
        <DialogDescription>
          Create a new AI workflow to automate your tasks
        </DialogDescription>

        <Form onSubmit={handleCreateWorkflow} className="mt-4">
          <FormField>
            <FormLabel htmlFor="workflowName" required>
              Workflow Name
            </FormLabel>
            <Input
              id="workflowName"
              value={newWorkflow.name}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, name: e.target.value })}
              placeholder="e.g., Customer Onboarding"
              required
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="workflowDescription">Description</FormLabel>
            <Textarea
              id="workflowDescription"
              value={newWorkflow.description}
              onChange={(e) => setNewWorkflow({ ...newWorkflow, description: e.target.value })}
              placeholder="Describe what this workflow does..."
              rows={3}
            />
          </FormField>

          <div className="flex gap-3 justify-end mt-6">
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsCreateDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit">Create Workflow</Button>
          </div>
        </Form>
      </Dialog>
    </div>
  );
}
