"""
API routes for Workers Service
"""
import sys
from pathlib import Path
from typing import List
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user, require_org_admin
from shared.config import get_settings

from .models import Job, WorkflowTemplate, JobStatus
from .schemas import (
    JobCreate,
    JobResponse,
    WorkflowTemplateCreate,
    WorkflowTemplateUpdate,
    WorkflowTemplateResponse,
    MessageResponse,
)

router = APIRouter()
settings = get_settings()


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create and queue a new job"""
    
    job = Job(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        job_type=job_data.job_type,
        input_data=job_data.input_data
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # TODO: Queue job to Celery
    # celery_task = execute_job.delay(job.id)
    # job.celery_task_id = celery_task.id
    # db.commit()
    
    return job


@router.get("/jobs", response_model=List[JobResponse])
async def list_jobs(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100
):
    """List jobs for current user's organization"""
    
    query = db.query(Job).filter(
        Job.organization_id == current_user.organization_id
    )
    
    if status_filter:
        query = query.filter(Job.status == status_filter)
    
    jobs = query.offset(skip).limit(limit).all()
    return jobs


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get job by ID"""
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.organization_id == current_user.organization_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job


@router.post("/jobs/{job_id}/cancel", response_model=MessageResponse)
async def cancel_job(
    job_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a running job"""
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.organization_id == current_user.organization_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.status not in [JobStatus.PENDING, JobStatus.RUNNING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job cannot be canceled in current state"
        )
    
    job.status = JobStatus.CANCELED
    job.completed_at = datetime.utcnow()
    
    # TODO: Cancel Celery task
    # if job.celery_task_id:
    #     celery_app.control.revoke(job.celery_task_id, terminate=True)
    
    db.commit()
    
    return {"message": "Job canceled successfully"}


@router.post("/templates", response_model=WorkflowTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: WorkflowTemplateCreate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Create a workflow template"""
    
    template = WorkflowTemplate(
        organization_id=current_user.organization_id,
        name=template_data.name,
        description=template_data.description,
        workflow_definition=template_data.workflow_definition
    )
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return template


@router.get("/templates", response_model=List[WorkflowTemplateResponse])
async def list_templates(
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """List workflow templates"""
    
    templates = db.query(WorkflowTemplate).filter(
        (WorkflowTemplate.organization_id == current_user.organization_id) |
        (WorkflowTemplate.organization_id.is_(None))
    ).all()
    
    return templates


@router.get("/templates/{template_id}", response_model=WorkflowTemplateResponse)
async def get_template(
    template_id: int,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Get template by ID"""
    
    template = db.query(WorkflowTemplate).filter(
        WorkflowTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check access
    if template.organization_id and template.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return template


@router.put("/templates/{template_id}", response_model=WorkflowTemplateResponse)
async def update_template(
    template_id: int,
    template_update: WorkflowTemplateUpdate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Update workflow template"""
    
    template = db.query(WorkflowTemplate).filter(
        WorkflowTemplate.id == template_id,
        WorkflowTemplate.organization_id == current_user.organization_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Update fields
    if template_update.name is not None:
        template.name = template_update.name
    if template_update.description is not None:
        template.description = template_update.description
    if template_update.workflow_definition is not None:
        template.workflow_definition = template_update.workflow_definition
    if template_update.is_active is not None:
        template.is_active = 1 if template_update.is_active else 0
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/templates/{template_id}", response_model=MessageResponse)
async def delete_template(
    template_id: int,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Delete workflow template"""
    
    template = db.query(WorkflowTemplate).filter(
        WorkflowTemplate.id == template_id,
        WorkflowTemplate.organization_id == current_user.organization_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    db.delete(template)
    db.commit()
    
    return {"message": "Template deleted successfully"}
