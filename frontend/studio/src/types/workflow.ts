export interface WorkflowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: {
    label: string;
    config: Record<string, unknown>;
  };
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  type?: string;
  data?: Record<string, unknown>;
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
  inputs: Record<string, unknown>;
  outputs?: Record<string, unknown>;
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
  defaultInputs: Record<string, unknown>;
  isPublic: boolean;
  organizationId: string;
  createdAt: string;
  updatedAt: string;
}