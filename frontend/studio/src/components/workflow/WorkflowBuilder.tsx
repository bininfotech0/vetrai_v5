import React, { useCallback, useEffect, useState } from 'react';
import ReactFlow, {
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  Connection,
  EdgeChange,
  NodeChange,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { PlayIcon, StopIcon, DocumentArrowDownIcon } from '@heroicons/react/24/outline';
import type { WorkflowNode, WorkflowEdge } from '@/types/workflow';

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'input',
    position: { x: 250, y: 25 },
    data: { label: 'Input Node' },
  },
  {
    id: '2',
    position: { x: 100, y: 125 },
    data: { label: 'Processing Node' },
  },
  {
    id: '3',
    type: 'output',
    position: { x: 250, y: 250 },
    data: { label: 'Output Node' },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2' },
  { id: 'e2-3', source: '2', target: '3' },
];

export function WorkflowBuilder() {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [isExecuting, setIsExecuting] = useState(false);

  const onNodesChange = useCallback(
    (changes: NodeChange[]) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes]
  );

  const onEdgesChange = useCallback(
    (changes: EdgeChange[]) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [setEdges]
  );

  const onConnect = useCallback(
    (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges]
  );

  const handleExecute = async () => {
    setIsExecuting(true);
    try {
      // TODO: Implement workflow execution via Workers API
      console.log('Executing workflow...', { nodes, edges });
      
      // Simulate execution
      await new Promise(resolve => setTimeout(resolve, 2000));
    } catch (error) {
      console.error('Workflow execution failed:', error);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleSave = async () => {
    try {
      // TODO: Implement workflow save via API
      console.log('Saving workflow...', { nodes, edges });
    } catch (error) {
      console.error('Workflow save failed:', error);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Toolbar */}
      <Card className="flex items-center justify-between p-4 m-4 mb-2">
        <div className="flex items-center space-x-2">
          <h2 className="text-lg font-semibold">Workflow Builder</h2>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            onClick={handleSave}
            variant="outline"
            size="sm"
          >
            <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
            Save
          </Button>
          
          <Button
            onClick={handleExecute}
            disabled={isExecuting}
            size="sm"
          >
            {isExecuting ? (
              <>
                <StopIcon className="h-4 w-4 mr-2" />
                Executing...
              </>
            ) : (
              <>
                <PlayIcon className="h-4 w-4 mr-2" />
                Execute
              </>
            )}
          </Button>
        </div>
      </Card>

      {/* React Flow Canvas */}
      <div className="flex-1 mx-4 mb-4 border rounded-lg overflow-hidden">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          attributionPosition="top-right"
        >
          <Controls />
          <MiniMap />
          <Background variant={'dots' as any} gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
}