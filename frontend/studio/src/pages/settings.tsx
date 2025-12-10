import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs';
import { Form, FormField, FormLabel, FormMessage } from '@/components/ui/Form';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Label } from '@/components/ui/Label';
import { ThemeToggle } from '@/components/ui/ThemeToggle';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import toast from 'react-hot-toast';

export default function Settings() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
  });

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // TODO: Implement profile update API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      toast.success('Profile updated successfully');
    } catch (error) {
      toast.error('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // TODO: Implement password change API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      toast.success('Password changed successfully');
    } catch (error) {
      toast.error('Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-2">Settings</h1>
            <p className="text-muted-foreground mb-6">Manage your account settings and preferences</p>

            <Tabs defaultIndex={0}>
              <TabsList className="mb-6">
                <TabsTrigger>Profile</TabsTrigger>
                <TabsTrigger>Security</TabsTrigger>
                <TabsTrigger>Appearance</TabsTrigger>
                <TabsTrigger>Notifications</TabsTrigger>
              </TabsList>

              {/* Profile Tab */}
              <TabsContent>
                <Card>
                  <CardHeader>
                    <CardTitle>Profile Information</CardTitle>
                    <CardDescription>Update your personal information</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Form onSubmit={handleProfileUpdate}>
                      <FormField>
                        <FormLabel htmlFor="firstName">First Name</FormLabel>
                        <Input
                          id="firstName"
                          value={profileData.firstName}
                          onChange={(e) =>
                            setProfileData({ ...profileData, firstName: e.target.value })
                          }
                        />
                      </FormField>

                      <FormField>
                        <FormLabel htmlFor="lastName">Last Name</FormLabel>
                        <Input
                          id="lastName"
                          value={profileData.lastName}
                          onChange={(e) =>
                            setProfileData({ ...profileData, lastName: e.target.value })
                          }
                        />
                      </FormField>

                      <FormField>
                        <FormLabel htmlFor="email">Email</FormLabel>
                        <Input
                          id="email"
                          type="email"
                          value={profileData.email}
                          onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                        />
                      </FormField>

                      <Button type="submit" disabled={loading}>
                        {loading ? <LoadingSpinner size="sm" className="mr-2" /> : null}
                        Save Changes
                      </Button>
                    </Form>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Security Tab */}
              <TabsContent>
                <Card>
                  <CardHeader>
                    <CardTitle>Change Password</CardTitle>
                    <CardDescription>Update your password to keep your account secure</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Form onSubmit={handlePasswordChange}>
                      <FormField>
                        <FormLabel htmlFor="currentPassword">Current Password</FormLabel>
                        <Input id="currentPassword" type="password" />
                      </FormField>

                      <FormField>
                        <FormLabel htmlFor="newPassword">New Password</FormLabel>
                        <Input id="newPassword" type="password" />
                      </FormField>

                      <FormField>
                        <FormLabel htmlFor="confirmPassword">Confirm New Password</FormLabel>
                        <Input id="confirmPassword" type="password" />
                      </FormField>

                      <Button type="submit" disabled={loading}>
                        {loading ? <LoadingSpinner size="sm" className="mr-2" /> : null}
                        Change Password
                      </Button>
                    </Form>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Appearance Tab */}
              <TabsContent>
                <Card>
                  <CardHeader>
                    <CardTitle>Appearance</CardTitle>
                    <CardDescription>Customize how VetrAI Studio looks</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <Label>Theme</Label>
                          <p className="text-sm text-muted-foreground">
                            Choose between light and dark mode
                          </p>
                        </div>
                        <ThemeToggle />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Notifications Tab */}
              <TabsContent>
                <Card>
                  <CardHeader>
                    <CardTitle>Notification Preferences</CardTitle>
                    <CardDescription>Manage how you receive notifications</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      Notification settings coming soon...
                    </p>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  );
}
