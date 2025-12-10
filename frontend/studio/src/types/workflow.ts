export interface WorkflowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: {
    label: string;
    config: Record<string, any>;
  };
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  type?: string;
  data?: Record<string, any>;
}

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  organizationId: string;
  createdBy: string;
  isTemplate: boolean;
  isPublic: boolean;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface WorkflowExecution {
  id: string;
  workflowId: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  inputs: Record<string, any>;
  outputs?: Record<string, any>;
  error?: string;
  startedAt: string;
  completedAt?: string;
  createdBy: string;
}

export interface JobTemplate {
  id: string;
  name: string;
  description?: string;
  workflow: Workflow;
  defaultInputs: Record<string, any>;
  isPublic: boolean;
  organizationId: string;
  createdAt: string;
  updatedAt: string;
}