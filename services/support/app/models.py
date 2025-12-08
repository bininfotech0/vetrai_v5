"""
Database models for Support Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from shared.models import BaseModel


class Ticket(BaseModel):
    """Support ticket model"""
    
    __tablename__ = "tickets"
    
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    assigned_to = Column(Integer, nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="open", index=True)
    priority = Column(String(50), nullable=False, default="medium", index=True)
    category = Column(String(100), nullable=True)
    sla_due_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, title='{self.title}', status='{self.status}')>"


class TicketComment(BaseModel):
    """Ticket comment model"""
    
    __tablename__ = "ticket_comments"
    
    ticket_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    comment = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<TicketComment(id={self.id}, ticket_id={self.ticket_id})>"
