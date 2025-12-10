"""
LangGraph Integration for VetrAI Platform
Provides state-based workflow execution and agent orchestration
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, TypedDict, Annotated
from datetime import datetime
import uuid

try:
    from langgraph.graph import StateGraph, END
    from langgraph.prebuilt import ToolExecutor
    from langchain.schema import BaseMessage, HumanMessage, AIMessage
    from langchain.tools import tool
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

logger = logging.getLogger(__name__)

class WorkflowState(TypedDict):
    """State structure for LangGraph workflows"""
    messages: List[BaseMessage]
    user_input: str
    current_step: str
    context: Dict[str, Any]
    result: Optional[str]

class LangGraphIntegration:
    """LangGraph integration for state-based AI workflows"""
    
    def __init__(self):
        self.workflows = {}
        self.executions = {}
        
    async def create_workflow(self, workflow_config: Dict[str, Any]) -> str:
        """Create a new LangGraph workflow"""
        if not LANGGRAPH_AVAILABLE:
            raise RuntimeError("LangGraph is not available. Install langgraph package.")
        
        try:
            workflow_id = str(uuid.uuid4())
            
            # Create the workflow graph
            workflow = StateGraph(WorkflowState)
            
            # Add nodes based on configuration
            nodes = workflow_config.get("nodes", [])
            for node in nodes:
                workflow.add_node(node["name"], self._create_node_function(node))
            
            # Add edges based on configuration
            edges = workflow_config.get("edges", [])
            for edge in edges:
                if edge.get("condition"):
                    workflow.add_conditional_edges(
                        edge["from"],
                        self._create_condition_function(edge["condition"]),
                        edge.get("mapping", {})
                    )
                else:
                    workflow.add_edge(edge["from"], edge["to"])
            
            # Set entry point
            entry_point = workflow_config.get("entry_point", "start")
            workflow.set_entry_point(entry_point)
            
            # Compile the workflow
            compiled_workflow = workflow.compile()
            
            # Store the workflow
            workflow_data = {
                "id": workflow_id,
                "name": workflow_config.get("name", f"VetrAI Workflow {workflow_id[:8]}"),
                "description": workflow_config.get("description", ""),
                "config": workflow_config,
                "workflow": compiled_workflow,
                "created_at": datetime.utcnow().isoformat()
            }
            
            self.workflows[workflow_id] = workflow_data
            
            logger.info(f"Created LangGraph workflow: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            logger.error(f"Error creating LangGraph workflow: {e}")
            raise
    
    def _create_node_function(self, node_config: Dict[str, Any]):
        """Create a node function based on configuration"""
        node_type = node_config.get("type", "simple")
        
        if node_type == "llm":
            return self._llm_node
        elif node_type == "tool":
            return self._tool_node
        elif node_type == "decision":
            return self._decision_node
        else:
            return self._simple_node
    
    def _create_condition_function(self, condition_config: Dict[str, Any]):
        """Create a condition function for conditional edges"""
        def condition_func(state: WorkflowState):
            # Simple condition evaluation (can be enhanced)
            field = condition_config.get("field", "current_step")
            value = condition_config.get("value", "")
            return state.get(field) == value
        
        return condition_func
    
    async def _llm_node(self, state: WorkflowState) -> WorkflowState:
        """LLM processing node"""
        try:
            # Simulate LLM processing
            user_input = state.get("user_input", "")
            
            # Create response (in real implementation, use actual LLM)
            response = f"AI Response to: {user_input}"
            
            state["messages"].append(AIMessage(content=response))
            state["result"] = response
            state["current_step"] = "llm_complete"
            
            return state
            
        except Exception as e:
            logger.error(f"Error in LLM node: {e}")
            state["current_step"] = "error"
            return state
    
    async def _tool_node(self, state: WorkflowState) -> WorkflowState:
        """Tool execution node"""
        try:
            # Simulate tool execution
            context = state.get("context", {})
            
            # Execute tool (placeholder)
            tool_result = f"Tool executed with context: {context}"
            
            state["context"]["tool_result"] = tool_result
            state["current_step"] = "tool_complete"
            
            return state
            
        except Exception as e:
            logger.error(f"Error in tool node: {e}")
            state["current_step"] = "error"
            return state
    
    async def _decision_node(self, state: WorkflowState) -> WorkflowState:
        """Decision making node"""
        try:
            # Simple decision logic
            user_input = state.get("user_input", "").lower()
            
            if "question" in user_input:
                state["current_step"] = "question_path"
            elif "task" in user_input:
                state["current_step"] = "task_path"
            else:
                state["current_step"] = "default_path"
            
            return state
            
        except Exception as e:
            logger.error(f"Error in decision node: {e}")
            state["current_step"] = "error"
            return state
    
    async def _simple_node(self, state: WorkflowState) -> WorkflowState:
        """Simple processing node"""
        try:
            state["current_step"] = "processed"
            return state
        except Exception as e:
            logger.error(f"Error in simple node: {e}")
            state["current_step"] = "error"
            return state
    
    async def execute_workflow(self, workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a LangGraph workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        try:
            workflow_data = self.workflows[workflow_id]
            workflow = workflow_data["workflow"]
            execution_id = str(uuid.uuid4())
            
            # Create initial state
            initial_state: WorkflowState = {
                "messages": [HumanMessage(content=inputs.get("input", ""))],
                "user_input": inputs.get("input", ""),
                "current_step": "start",
                "context": inputs.get("context", {}),
                "result": None
            }
            
            # Execute workflow
            final_state = await workflow.ainvoke(initial_state)
            
            # Store execution result
            execution_result = {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "status": "completed" if final_state.get("current_step") != "error" else "error",
                "inputs": inputs,
                "final_state": final_state,
                "result": final_state.get("result"),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.executions[execution_id] = execution_result
            
            logger.info(f"Executed LangGraph workflow: {workflow_id}")
            return execution_result
            
        except Exception as e:
            logger.error(f"Error executing LangGraph workflow: {e}")
            raise
    
    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow configuration"""
        workflow_data = self.workflows.get(workflow_id)
        if workflow_data:
            # Return serializable data (exclude compiled workflow)
            return {
                "id": workflow_data["id"],
                "name": workflow_data["name"],
                "description": workflow_data["description"],
                "config": workflow_data["config"],
                "created_at": workflow_data["created_at"]
            }
        return None
    
    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflows"""
        return [await self.get_workflow(wid) for wid in self.workflows.keys()]
    
    async def get_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get execution result"""
        return self.executions.get(execution_id)
    
    def create_sample_workflows(self):
        """Create sample LangGraph workflows"""
        
        # Simple Chat Workflow
        chat_workflow = {
            "name": "Simple Chat Workflow",
            "description": "Basic chat interaction with LLM",
            "entry_point": "start",
            "nodes": [
                {"name": "start", "type": "simple"},
                {"name": "llm", "type": "llm"},
                {"name": "end", "type": "simple"}
            ],
            "edges": [
                {"from": "start", "to": "llm"},
                {"from": "llm", "to": "end"}
            ]
        }
        
        # Multi-Agent Workflow
        agent_workflow = {
            "name": "Multi-Agent Workflow",
            "description": "Workflow with decision making and tool usage",
            "entry_point": "start",
            "nodes": [
                {"name": "start", "type": "simple"},
                {"name": "decision", "type": "decision"},
                {"name": "llm", "type": "llm"},
                {"name": "tool", "type": "tool"},
                {"name": "end", "type": "simple"}
            ],
            "edges": [
                {"from": "start", "to": "decision"},
                {
                    "from": "decision",
                    "condition": {"field": "current_step", "value": "question_path"},
                    "mapping": {
                        "question_path": "llm",
                        "task_path": "tool",
                        "default_path": "llm"
                    }
                },
                {"from": "llm", "to": "end"},
                {"from": "tool", "to": "end"}
            ]
        }
        
        return [chat_workflow, agent_workflow]

# Global instance
langgraph_integration = LangGraphIntegration()

# Initialize sample workflows
try:
    if LANGGRAPH_AVAILABLE:
        sample_workflows = langgraph_integration.create_sample_workflows()
        for workflow in sample_workflows:
            asyncio.run(langgraph_integration.create_workflow(workflow))
except Exception as e:
    logger.warning(f"Could not create sample workflows: {e}")