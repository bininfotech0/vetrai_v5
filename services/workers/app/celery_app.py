"""
Celery application configuration
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from celery import Celery
from shared.config import get_settings

settings = get_settings()

# Create Celery app
celery_app = Celery(
    "vetrai_workers",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=settings.celery_task_track_started,
    task_time_limit=settings.celery_task_time_limit,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)


@celery_app.task(name="execute_workflow")
def execute_workflow(job_id: int, workflow_type: str, input_data: dict):
    """Execute workflow task"""
    # Placeholder for workflow execution
    import time

    time.sleep(2)  # Simulate work
    return {"status": "completed", "result": "Workflow executed successfully"}
