"""
API routes for Support Service
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import List
import secrets

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user
from shared.config import get_settings

from .models import Ticket, TicketComment, TicketAttachment, TicketStatus
from .schemas import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    CommentCreate,
    CommentResponse,
    AttachmentResponse,
    MessageResponse,
)

router = APIRouter()
settings = get_settings()


def generate_ticket_number() -> str:
    """Generate a unique ticket number"""
    return f"TKT-{secrets.token_hex(4).upper()}"


@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new support ticket"""
    
    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        priority=ticket_data.priority,
        ticket_number=generate_ticket_number()
    )
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    return ticket


@router.get("/tickets", response_model=List[TicketResponse])
async def list_tickets(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100
):
    """List tickets for current user's organization"""
    
    query = db.query(Ticket).filter(
        Ticket.organization_id == current_user.organization_id
    )
    
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    
    tickets = query.offset(skip).limit(limit).all()
    return tickets


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ticket by ID"""
    
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.organization_id == current_user.organization_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    return ticket


@router.put("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update ticket"""
    
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.organization_id == current_user.organization_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Update fields
    if ticket_update.title is not None:
        ticket.title = ticket_update.title
    if ticket_update.description is not None:
        ticket.description = ticket_update.description
    if ticket_update.priority is not None:
        ticket.priority = ticket_update.priority
    if ticket_update.status is not None:
        ticket.status = ticket_update.status
    if ticket_update.assigned_to is not None:
        ticket.assigned_to = ticket_update.assigned_to
    
    db.commit()
    db.refresh(ticket)
    
    return ticket


@router.post("/tickets/{ticket_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    ticket_id: int,
    comment_data: CommentCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a ticket"""
    
    # Verify ticket exists and belongs to organization
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.organization_id == current_user.organization_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    comment = TicketComment(
        ticket_id=ticket_id,
        user_id=current_user.user_id,
        comment=comment_data.comment,
        is_internal=comment_data.is_internal
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment


@router.get("/tickets/{ticket_id}/comments", response_model=List[CommentResponse])
async def list_comments(
    ticket_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List comments for a ticket"""
    
    # Verify ticket exists and belongs to organization
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.organization_id == current_user.organization_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    comments = db.query(TicketComment).filter(
        TicketComment.ticket_id == ticket_id
    ).all()
    
    return comments


@router.post("/tickets/{ticket_id}/attachments", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    ticket_id: int,
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an attachment to a ticket"""
    
    # Verify ticket exists and belongs to organization
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.organization_id == current_user.organization_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # TODO: Upload file to MinIO
    file_path = f"tickets/{ticket_id}/{file.filename}"
    file_size = 0  # TODO: Get actual file size
    
    attachment = TicketAttachment(
        ticket_id=ticket_id,
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        content_type=file.content_type
    )
    
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    
    return attachment


@router.get("/tickets/{ticket_id}/attachments", response_model=List[AttachmentResponse])
async def list_attachments(
    ticket_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List attachments for a ticket"""
    
    # Verify ticket exists and belongs to organization
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.organization_id == current_user.organization_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    attachments = db.query(TicketAttachment).filter(
        TicketAttachment.ticket_id == ticket_id
    ).all()
    
    return attachments
