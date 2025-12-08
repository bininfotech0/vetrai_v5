"""
Pydantic schemas for Workers Service
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class WorkflowExecuteRequest(BaseModel):
    """Schema for workflow execution request"""

    workflow_type: str = Field(..., description="Type of workflow to execute")
    input_data: Dict[str, Any] = Field(..., description="Input data for workflow")
    priority: Optional[int] = Field(default=1, ge=1, le=10)


class WorkflowExecuteResponse(BaseModel):
    """Schema for workflow execution response"""

    job_id: int
    status: str
    message: str


class JobStatusResponse(BaseModel):
    """Schema for job status response"""

    id: int
    organization_id: int
    user_id: int
    job_type: str
    status: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    retries: int
    created_at: datetime

    class Config:
        from_attributes = True


class MetricsResponse(BaseModel):
    """Schema for performance metrics"""

    total_jobs: int
    pending_jobs: int
    running_jobs: int
    completed_jobs: int
    failed_jobs: int
    avg_execution_time_seconds: float


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str
