"""
API routes for Billing Service
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user, require_org_admin
from shared.config import get_settings

from models import Subscription, Invoice, Payment, SubscriptionStatus
from schemas import (
    SubscriptionCreate,
    SubscriptionResponse,
    InvoiceResponse,
    PaymentResponse,
    WebhookEvent,
    MessageResponse,
)

router = APIRouter()
settings = get_settings()


@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Create a new subscription"""
    
    # Check if organization already has an active subscription
    existing = db.query(Subscription).filter(
        Subscription.organization_id == current_user.organization_id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization already has an active subscription"
        )
    
    # Create subscription
    subscription = Subscription(
        organization_id=current_user.organization_id,
        plan_name=subscription_data.plan_name,
        status=SubscriptionStatus.TRIALING if subscription_data.trial_days else SubscriptionStatus.ACTIVE
    )
    
    # TODO: Integrate with Stripe API
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return subscription


@router.get("/subscriptions", response_model=List[SubscriptionResponse])
async def list_subscriptions(
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """List subscriptions for current organization"""
    
    subscriptions = db.query(Subscription).filter(
        Subscription.organization_id == current_user.organization_id
    ).all()
    
    return subscriptions


@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: int,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Get subscription by ID"""
    
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.organization_id == current_user.organization_id
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    return subscription


@router.post("/subscriptions/{subscription_id}/cancel", response_model=MessageResponse)
async def cancel_subscription(
    subscription_id: int,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Cancel a subscription"""
    
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.organization_id == current_user.organization_id
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.status = SubscriptionStatus.CANCELED
    subscription.canceled_at = datetime.utcnow()
    
    # TODO: Cancel in Stripe
    
    db.commit()
    
    return {"message": "Subscription canceled successfully"}


@router.get("/invoices", response_model=List[InvoiceResponse])
async def list_invoices(
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List invoices for current organization"""
    
    invoices = db.query(Invoice).filter(
        Invoice.organization_id == current_user.organization_id
    ).offset(skip).limit(limit).all()
    
    return invoices


@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Get invoice by ID"""
    
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.organization_id == current_user.organization_id
    ).first()
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    return invoice


@router.get("/payments", response_model=List[PaymentResponse])
async def list_payments(
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List payments for current organization"""
    
    payments = db.query(Payment).filter(
        Payment.organization_id == current_user.organization_id
    ).offset(skip).limit(limit).all()
    
    return payments


@router.post("/webhooks/stripe", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    """Handle Stripe webhooks"""
    
    # TODO: Verify webhook signature
    # TODO: Process webhook events
    
    payload = await request.json()
    event_type = payload.get("type")
    
    # Handle different event types
    if event_type == "invoice.paid":
        # Update invoice status
        pass
    elif event_type == "invoice.payment_failed":
        # Handle failed payment
        pass
    elif event_type == "customer.subscription.deleted":
        # Cancel subscription
        pass
    
    return {"status": "success"}
