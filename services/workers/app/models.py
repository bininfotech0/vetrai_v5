"""
Database models for Workers Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from shared.models import BaseModel


class WorkerJob(BaseModel):
    """Worker job model"""
    
    __tablename__ = "worker_jobs"
    
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    job_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="pending", index=True)
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    retries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    def __repr__(self):
        return f"<WorkerJob(id={self.id}, job_type='{self.job_type}', status='{self.status}')>"
