import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { Workflow, WorkflowExecution } from '@/types/workflow';

interface WorkflowState {
  workflows: Workflow[];
  currentWorkflow: Workflow | null;
  executions: WorkflowExecution[];
  loading: boolean;
}

const initialState: WorkflowState = {
  workflows: [],
  currentWorkflow: null,
  executions: [],
  loading: false,
};

const workflowSlice = createSlice({
  name: 'workflow',
  initialState,
  reducers: {
    setWorkflows: (state, action: PayloadAction<Workflow[]>) => {
      state.workflows = action.payload;
    },
    setCurrentWorkflow: (state, action: PayloadAction<Workflow | null>) => {
      state.currentWorkflow = action.payload;
    },
    addWorkflow: (state, action: PayloadAction<Workflow>) => {
      state.workflows.push(action.payload);
    },
    updateWorkflow: (state, action: PayloadAction<Workflow>) => {
      const index = state.workflows.findIndex(w => w.id === action.payload.id);
      if (index !== -1) {
        state.workflows[index] = action.payload;
      }
      if (state.currentWorkflow?.id === action.payload.id) {
        state.currentWorkflow = action.payload;
      }
    },
    removeWorkflow: (state, action: PayloadAction<string>) => {
      state.workflows = state.workflows.filter(w => w.id !== action.payload);
      if (state.currentWorkflow?.id === action.payload) {
        state.currentWorkflow = null;
      }
    },
    setExecutions: (state, action: PayloadAction<WorkflowExecution[]>) => {
      state.executions = action.payload;
    },
    addExecution: (state, action: PayloadAction<WorkflowExecution>) => {
      state.executions.unshift(action.payload);
    },
    updateExecution: (state, action: PayloadAction<WorkflowExecution>) => {
      const index = state.executions.findIndex(e => e.id === action.payload.id);
      if (index !== -1) {
        state.executions[index] = action.payload;
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const {
  setWorkflows,
  setCurrentWorkflow,
  addWorkflow,
  updateWorkflow,
  removeWorkflow,
  setExecutions,
  addExecution,
  updateExecution,
  setLoading,
} = workflowSlice.actions;

export default workflowSlice.reducer;