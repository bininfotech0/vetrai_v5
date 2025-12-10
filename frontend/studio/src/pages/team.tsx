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
import { PlusIcon, TrashIcon, PencilIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { formatDateTime } from '@/lib/utils';

interface TeamMember {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  role: 'org_admin' | 'user' | 'support_agent' | 'billing_admin';
  status: 'active' | 'pending' | 'inactive';
  lastActive?: Date;
  createdAt: Date;
}

export default function Team() {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([
    {
      id: '1',
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@example.com',
      role: 'org_admin',
      status: 'active',
      lastActive: new Date(),
      createdAt: new Date(),
    },
    {
      id: '2',
      firstName: 'Jane',
      lastName: 'Smith',
      email: 'jane@example.com',
      role: 'user',
      status: 'active',
      lastActive: new Date(),
      createdAt: new Date(),
    },
  ]);
  const [isInviteDialogOpen, setIsInviteDialogOpen] = useState(false);
  const [inviteData, setInviteData] = useState({
    email: '',
    role: 'user' as TeamMember['role'],
  });

  const handleInviteMember = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteData.email.trim() || !/\S+@\S+\.\S+/.test(inviteData.email)) {
      toast.error('Valid email is required');
      return;
    }

    const member: TeamMember = {
      id: Date.now().toString(),
      firstName: 'Pending',
      lastName: 'User',
      email: inviteData.email,
      role: inviteData.role,
      status: 'pending',
      createdAt: new Date(),
    };

    setTeamMembers([...teamMembers, member]);
    setInviteData({ email: '', role: 'user' });
    setIsInviteDialogOpen(false);
    toast.success('Team member invited successfully');
  };

  const handleRemoveMember = (id: string) => {
    setTeamMembers(teamMembers.filter((m) => m.id !== id));
    toast.success('Team member removed');
  };

  const getRoleBadge = (role: TeamMember['role']) => {
    const labels = {
      org_admin: 'Org Admin',
      user: 'User',
      support_agent: 'Support',
      billing_admin: 'Billing',
    };
    return <Badge variant="outline">{labels[role]}</Badge>;
  };

  const getStatusBadge = (status: TeamMember['status']) => {
    const variants = {
      active: 'success',
      pending: 'warning',
      inactive: 'secondary',
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
                <h1 className="text-3xl font-bold">Team</h1>
                <p className="text-muted-foreground mt-1">
                  Manage your team members and their roles
                </p>
              </div>
              <Button onClick={() => setIsInviteDialogOpen(true)}>
                <PlusIcon className="h-4 w-4 mr-2" />
                Invite Member
              </Button>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Team Members</CardTitle>
                <CardDescription>
                  {teamMembers.length} {teamMembers.length === 1 ? 'member' : 'members'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Role</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Last Active</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {teamMembers.map((member) => (
                      <TableRow key={member.id}>
                        <TableCell className="font-medium">
                          {member.firstName} {member.lastName}
                        </TableCell>
                        <TableCell>{member.email}</TableCell>
                        <TableCell>{getRoleBadge(member.role)}</TableCell>
                        <TableCell>{getStatusBadge(member.status)}</TableCell>
                        <TableCell>
                          {member.lastActive ? formatDateTime(member.lastActive) : 'Never'}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center justify-end gap-2">
                            <Button variant="ghost" size="sm" title="Edit member">
                              <PencilIcon className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleRemoveMember(member.id)}
                              title="Remove member"
                            >
                              <TrashIcon className="h-4 w-4 text-destructive" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>

      {/* Invite Member Dialog */}
      <Dialog open={isInviteDialogOpen} onClose={() => setIsInviteDialogOpen(false)}>
        <DialogCloseButton onClose={() => setIsInviteDialogOpen(false)} />
        <DialogTitle>Invite Team Member</DialogTitle>
        <DialogDescription>
          Send an invitation to join your organization
        </DialogDescription>

        <Form onSubmit={handleInviteMember} className="mt-4">
          <FormField>
            <FormLabel htmlFor="memberEmail" required>
              Email Address
            </FormLabel>
            <Input
              id="memberEmail"
              type="email"
              value={inviteData.email}
              onChange={(e) => setInviteData({ ...inviteData, email: e.target.value })}
              placeholder="colleague@example.com"
              required
            />
            <FormDescription>
              They will receive an email invitation to join your team
            </FormDescription>
          </FormField>

          <FormField>
            <FormLabel htmlFor="memberRole" required>
              Role
            </FormLabel>
            <Select
              id="memberRole"
              value={inviteData.role}
              onChange={(e) => setInviteData({ ...inviteData, role: e.target.value as TeamMember['role'] })}
              options={[
                { value: 'user', label: 'User - Standard access' },
                { value: 'org_admin', label: 'Org Admin - Full organization access' },
                { value: 'support_agent', label: 'Support Agent - Support access' },
                { value: 'billing_admin', label: 'Billing Admin - Billing access' },
              ]}
            />
            <FormDescription>
              Choose the level of access for this team member
            </FormDescription>
          </FormField>

          <Alert variant="info" className="mt-4">
            <AlertDescription>
              Team members can be managed and their roles changed at any time
            </AlertDescription>
          </Alert>

          <div className="flex gap-3 justify-end mt-6">
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsInviteDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit">Send Invitation</Button>
          </div>
        </Form>
      </Dialog>
    </div>
  );
}
