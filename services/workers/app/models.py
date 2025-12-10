"""
Database models for Workers Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Text, Boolean, Enum as SQLEnum, JSON, DateTime
from shared.models import BaseModel
import enum


class JobStatus(enum.Enum):
    """Job status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class Job(BaseModel):
    """Job model for workflow execution"""
    
    __tablename__ = "worker_jobs"
    
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    job_type = Column(String(100), nullable=False, index=True)
    status = Column(SQLEnum(JobStatus), nullable=False, default=JobStatus.PENDING, index=True)
    
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    celery_task_id = Column(String(255), nullable=True, unique=True, index=True)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Job(id={self.id}, type='{self.job_type}', status='{self.status.value}')>"


class WorkflowTemplate(BaseModel):
    """Workflow template model"""
    
    __tablename__ = "workflow_templates"
    
    organization_id = Column(Integer, nullable=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    workflow_definition = Column(JSON, nullable=False)
    
    is_active = Column(Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f"<WorkflowTemplate(id={self.id}, name='{self.name}')>"
