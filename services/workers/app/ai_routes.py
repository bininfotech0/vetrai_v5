"""
API routes for AI Integrations (LangFlow, LangGraph, LLaMA)
"""
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user, require_org_admin
from shared.config import get_settings

from integrations import langflow_integration, langgraph_integration, llama_integration

router = APIRouter(prefix="/ai", tags=["AI Integrations"])
settings = get_settings()

# Pydantic Models
class FlowCreateRequest(BaseModel):
    name: str
    description: str = ""
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

class FlowExecuteRequest(BaseModel):
    inputs: Dict[str, Any]

class WorkflowCreateRequest(BaseModel):
    name: str
    description: str = ""
    entry_point: str = "start"
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]

class WorkflowExecuteRequest(BaseModel):
    inputs: Dict[str, Any]

class LLaMAModelRequest(BaseModel):
    name: str
    type: str = "ollama"  # ollama, transformers, llama_cpp
    model_path: str = ""
    context_length: int = 2048
    temperature: float = 0.7

class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7

class ChatRequest(BaseModel):
    message: str

# LangFlow Routes
@router.post("/langflow/flows", status_code=status.HTTP_201_CREATED)
async def create_langflow_flow(
    request: FlowCreateRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Create a new LangFlow workflow"""
    try:
        flow_id = await langflow_integration.create_flow({
            "name": request.name,
            "description": request.description,
            "nodes": request.nodes,
            "edges": request.edges
        })
        
        return {
            "message": "LangFlow workflow created successfully",
            "flow_id": flow_id,
            "name": request.name
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating LangFlow workflow: {str(e)}"
        )

@router.get("/langflow/flows")
async def list_langflow_flows(
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all LangFlow workflows"""
    try:
        flows = await langflow_integration.list_flows()
        return {"flows": flows}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing LangFlow workflows: {str(e)}"
        )

@router.post("/langflow/flows/{flow_id}/execute")
async def execute_langflow_flow(
    flow_id: str,
    request: FlowExecuteRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Execute a LangFlow workflow"""
    try:
        result = await langflow_integration.run_flow(flow_id, request.inputs)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing LangFlow workflow: {str(e)}"
        )

@router.get("/langflow/flows/{flow_id}")
async def get_langflow_flow(
    flow_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get LangFlow workflow details"""
    try:
        flow = await langflow_integration.get_flow(flow_id)
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LangFlow workflow not found"
            )
        return flow
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting LangFlow workflow: {str(e)}"
        )

# LangGraph Routes
@router.post("/langgraph/workflows", status_code=status.HTTP_201_CREATED)
async def create_langgraph_workflow(
    request: WorkflowCreateRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Create a new LangGraph workflow"""
    try:
        workflow_id = await langgraph_integration.create_workflow({
            "name": request.name,
            "description": request.description,
            "entry_point": request.entry_point,
            "nodes": request.nodes,
            "edges": request.edges
        })
        
        return {
            "message": "LangGraph workflow created successfully",
            "workflow_id": workflow_id,
            "name": request.name
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating LangGraph workflow: {str(e)}"
        )

@router.get("/langgraph/workflows")
async def list_langgraph_workflows(
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all LangGraph workflows"""
    try:
        workflows = await langgraph_integration.list_workflows()
        return {"workflows": workflows}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing LangGraph workflows: {str(e)}"
        )

@router.post("/langgraph/workflows/{workflow_id}/execute")
async def execute_langgraph_workflow(
    workflow_id: str,
    request: WorkflowExecuteRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Execute a LangGraph workflow"""
    try:
        result = await langgraph_integration.execute_workflow(workflow_id, request.inputs)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing LangGraph workflow: {str(e)}"
        )

@router.get("/langgraph/workflows/{workflow_id}")
async def get_langgraph_workflow(
    workflow_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get LangGraph workflow details"""
    try:
        workflow = await langgraph_integration.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LangGraph workflow not found"
            )
        return workflow
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting LangGraph workflow: {str(e)}"
        )

# LLaMA Routes
@router.post("/llama/models", status_code=status.HTTP_201_CREATED)
async def initialize_llama_model(
    request: LLaMAModelRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Initialize a LLaMA model"""
    try:
        model_id = await llama_integration.initialize_model({
            "name": request.name,
            "type": request.type,
            "model_path": request.model_path,
            "context_length": request.context_length,
            "temperature": request.temperature
        })
        
        return {
            "message": "LLaMA model initialized successfully",
            "model_id": model_id,
            "name": request.name
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing LLaMA model: {str(e)}"
        )

@router.get("/llama/models")
async def list_llama_models(
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all LLaMA models"""
    try:
        models = await llama_integration.list_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing LLaMA models: {str(e)}"
        )

@router.post("/llama/models/{model_id}/generate")
async def generate_text_llama(
    model_id: str,
    request: TextGenerationRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Generate text using a LLaMA model"""
    try:
        result = await llama_integration.generate_text(
            model_id, 
            request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating text: {str(e)}"
        )

@router.post("/llama/models/{model_id}/chat/start")
async def start_llama_chat(
    model_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Start a new chat session with a LLaMA model"""
    try:
        session_id = await llama_integration.start_chat_session(model_id)
        return {
            "message": "Chat session started successfully",
            "session_id": session_id,
            "model_id": model_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting chat session: {str(e)}"
        )

@router.post("/llama/chat/{session_id}")
async def chat_llama(
    session_id: str,
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Continue a chat session with a LLaMA model"""
    try:
        result = await llama_integration.chat(session_id, request.message)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in chat: {str(e)}"
        )

@router.get("/llama/chat/{session_id}")
async def get_llama_chat_session(
    session_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get chat session details"""
    try:
        session = await llama_integration.get_chat_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting chat session: {str(e)}"
        )

# General AI Status Route
@router.get("/status")
async def get_ai_status(
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get status of all AI integrations"""
    try:
        langflow_flows = await langflow_integration.list_flows()
        langgraph_workflows = await langgraph_integration.list_workflows()
        llama_models = await llama_integration.list_models()
        
        return {
            "status": "healthy",
            "integrations": {
                "langflow": {
                    "available": True,
                    "flows_count": len(langflow_flows)
                },
                "langgraph": {
                    "available": True,
                    "workflows_count": len(langgraph_workflows)
                },
                "llama": {
                    "available": True,
                    "models_count": len(llama_models)
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }