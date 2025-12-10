import { useState } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { MagnifyingGlassIcon, RocketLaunchIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  usageCount: number;
}

export default function Templates() {
  const [templates] = useState<Template[]>([
    {
      id: '1',
      name: 'Customer Service Bot',
      description: 'Automated customer support chatbot with natural language processing',
      category: 'Customer Service',
      difficulty: 'beginner',
      usageCount: 1234,
    },
    {
      id: '2',
      name: 'Data Analysis Pipeline',
      description: 'Extract insights from large datasets using AI-powered analysis',
      category: 'Analytics',
      difficulty: 'intermediate',
      usageCount: 856,
    },
    {
      id: '3',
      name: 'Content Generation',
      description: 'Generate high-quality content for blogs, social media, and marketing',
      category: 'Content',
      difficulty: 'beginner',
      usageCount: 2103,
    },
    {
      id: '4',
      name: 'Document Processing',
      description: 'Extract and process information from documents and forms',
      category: 'Document Processing',
      difficulty: 'intermediate',
      usageCount: 674,
    },
    {
      id: '5',
      name: 'Sentiment Analysis',
      description: 'Analyze customer feedback and social media sentiment',
      category: 'Analytics',
      difficulty: 'advanced',
      usageCount: 445,
    },
    {
      id: '6',
      name: 'Email Classification',
      description: 'Automatically categorize and route incoming emails',
      category: 'Automation',
      difficulty: 'beginner',
      usageCount: 932,
    },
  ]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const categories = ['all', ...Array.from(new Set(templates.map((t) => t.category)))];

  const filteredTemplates = templates.filter((template) => {
    const matchesSearch =
      template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getDifficultyBadge = (difficulty: Template['difficulty']) => {
    const variants = {
      beginner: 'success',
      intermediate: 'warning',
      advanced: 'destructive',
    } as const;
    return <Badge variant={variants[difficulty]}>{difficulty}</Badge>;
  };

  const handleUseTemplate = (template: Template) => {
    toast.success(`Using template: ${template.name}`);
    // TODO: Navigate to workflow builder with template
  };

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto">
            <div className="mb-6">
              <h1 className="text-3xl font-bold">Workflow Templates</h1>
              <p className="text-muted-foreground mt-1">
                Pre-built AI workflows to help you get started quickly
              </p>
            </div>

            <div className="mb-6 flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search templates..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                  aria-label="Search templates"
                />
              </div>
              <div className="flex gap-2 flex-wrap">
                {categories.map((category) => (
                  <Button
                    key={category}
                    variant={selectedCategory === category ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedCategory(category)}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </Button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredTemplates.length === 0 ? (
                <div className="col-span-full text-center py-12 text-muted-foreground">
                  No templates found
                </div>
              ) : (
                filteredTemplates.map((template) => (
                  <Card key={template.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between mb-2">
                        <CardTitle className="text-lg">{template.name}</CardTitle>
                        {getDifficultyBadge(template.difficulty)}
                      </div>
                      <CardDescription>{template.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between">
                        <div className="space-y-1">
                          <p className="text-sm text-muted-foreground">
                            <Badge variant="outline">{template.category}</Badge>
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {template.usageCount.toLocaleString()} uses
                          </p>
                        </div>
                        <Button size="sm" onClick={() => handleUseTemplate(template)}>
                          <RocketLaunchIcon className="h-4 w-4 mr-1" />
                          Use Template
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
