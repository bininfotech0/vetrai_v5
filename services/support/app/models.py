"""
Database models for Support Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Text, Boolean, Enum as SQLEnum
from shared.models import BaseModel
import enum


class TicketPriority(enum.Enum):
    """Ticket priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketStatus(enum.Enum):
    """Ticket status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_ON_CUSTOMER = "waiting_on_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Ticket(BaseModel):
    """Support ticket model"""
    
    __tablename__ = "support_tickets"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    assigned_to = Column(Integer, nullable=True, index=True)
    
    priority = Column(SQLEnum(TicketPriority), nullable=False, default=TicketPriority.MEDIUM)
    status = Column(SQLEnum(TicketStatus), nullable=False, default=TicketStatus.OPEN)
    
    ticket_number = Column(String(50), nullable=False, unique=True, index=True)
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, number='{self.ticket_number}', status='{self.status.value}')>"


class TicketComment(BaseModel):
    """Ticket comment model"""
    
    __tablename__ = "support_ticket_comments"
    
    ticket_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    comment = Column(Text, nullable=False)
    is_internal = Column(Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"<TicketComment(id={self.id}, ticket_id={self.ticket_id})>"


class TicketAttachment(BaseModel):
    """Ticket attachment model"""
    
    __tablename__ = "support_ticket_attachments"
    
    ticket_id = Column(Integer, nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<TicketAttachment(id={self.id}, filename='{self.filename}')>"
