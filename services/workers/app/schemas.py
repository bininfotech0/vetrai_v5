"""
Pydantic schemas for Workers Service
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    """Schema for creating a job"""
    job_type: str = Field(..., min_length=1, max_length=100)
    input_data: Optional[Dict[str, Any]] = None


class JobResponse(BaseModel):
    """Schema for job response"""
    id: int
    organization_id: int
    user_id: int
    job_type: str
    status: str
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    celery_task_id: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowTemplateCreate(BaseModel):
    """Schema for creating a workflow template"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    workflow_definition: Dict[str, Any] = Field(...)


class WorkflowTemplateUpdate(BaseModel):
    """Schema for updating a workflow template"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    workflow_definition: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class WorkflowTemplateResponse(BaseModel):
    """Schema for workflow template response"""
    id: int
    organization_id: Optional[int]
    name: str
    description: Optional[str]
    workflow_definition: Dict[str, Any]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
