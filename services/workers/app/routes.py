"""
API routes for Workers Service
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from shared.config import get_settings
from shared.middleware import CurrentUser, get_current_user
from shared.utils import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session

from .celery_app import execute_workflow
from .models import WorkerJob
from .schemas import (JobStatusResponse, MessageResponse, MetricsResponse,
                      WorkflowExecuteRequest, WorkflowExecuteResponse)

router = APIRouter()
settings = get_settings()


@router.post(
    "/workflows/execute",
    response_model=WorkflowExecuteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def execute_workflow_endpoint(
    workflow_request: WorkflowExecuteRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Execute workflow"""
    # Create job record
    job = WorkerJob(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        job_type=workflow_request.workflow_type,
        status="pending",
        input_data=workflow_request.input_data,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Trigger Celery task
    execute_workflow.delay(
        job.id, workflow_request.workflow_type, workflow_request.input_data
    )

    return {
        "job_id": job.id,
        "status": "pending",
        "message": "Workflow execution started",
    }


@router.get("/workflows/{job_id}", response_model=JobStatusResponse)
async def get_workflow_status(
    job_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get workflow execution status"""
    job = (
        db.query(WorkerJob)
        .filter(
            WorkerJob.id == job_id,
            WorkerJob.organization_id == current_user.organization_id,
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )

    return job


@router.delete("/workflows/{job_id}", response_model=MessageResponse)
async def cancel_workflow(
    job_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel workflow execution"""
    job = (
        db.query(WorkerJob)
        .filter(
            WorkerJob.id == job_id,
            WorkerJob.organization_id == current_user.organization_id,
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )

    if job.status in ["pending", "running"]:
        job.status = "cancelled"
        db.commit()

    return {"message": "Workflow cancelled successfully"}


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get performance metrics"""
    # Query job statistics
    total_jobs = (
        db.query(func.count(WorkerJob.id))
        .filter(WorkerJob.organization_id == current_user.organization_id)
        .scalar()
    )

    pending_jobs = (
        db.query(func.count(WorkerJob.id))
        .filter(
            WorkerJob.organization_id == current_user.organization_id,
            WorkerJob.status == "pending",
        )
        .scalar()
    )

    running_jobs = (
        db.query(func.count(WorkerJob.id))
        .filter(
            WorkerJob.organization_id == current_user.organization_id,
            WorkerJob.status == "running",
        )
        .scalar()
    )

    completed_jobs = (
        db.query(func.count(WorkerJob.id))
        .filter(
            WorkerJob.organization_id == current_user.organization_id,
            WorkerJob.status == "completed",
        )
        .scalar()
    )

    failed_jobs = (
        db.query(func.count(WorkerJob.id))
        .filter(
            WorkerJob.organization_id == current_user.organization_id,
            WorkerJob.status == "failed",
        )
        .scalar()
    )

    return {
        "total_jobs": total_jobs or 0,
        "pending_jobs": pending_jobs or 0,
        "running_jobs": running_jobs or 0,
        "completed_jobs": completed_jobs or 0,
        "failed_jobs": failed_jobs or 0,
        "avg_execution_time_seconds": 0.0,  # Placeholder
    }
