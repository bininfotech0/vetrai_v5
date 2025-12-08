"""
API routes for Billing Service
"""

import sys
from pathlib import Path
from typing import List, Optional

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, Header, Request, status
from shared.config import get_settings
from shared.middleware import CurrentUser, get_current_user, require_org_admin
from shared.utils import get_db
from sqlalchemy.orm import Session

from .models import Invoice, Subscription
from .schemas import (CheckoutSessionCreate, CheckoutSessionResponse,
                      InvoiceResponse, MessageResponse, SubscriptionCreate,
                      SubscriptionResponse)

router = APIRouter()
settings = get_settings()


@router.post("/customers", response_model=MessageResponse)
async def create_customer(
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db),
):
    """Create Stripe customer for organization"""
    # Placeholder - Stripe integration
    return {"message": "Customer created successfully"}


@router.post(
    "/subscriptions",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db),
):
    """Create subscription"""
    subscription = Subscription(
        organization_id=current_user.organization_id,
        plan=subscription_data.plan,
        status="active",
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


@router.get("/subscriptions", response_model=List[SubscriptionResponse])
async def list_subscriptions(
    current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    """List organization subscriptions"""
    subscriptions = (
        db.query(Subscription)
        .filter(Subscription.organization_id == current_user.organization_id)
        .all()
    )

    return subscriptions


@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    checkout_data: CheckoutSessionCreate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db),
):
    """Create Stripe checkout session"""
    # Placeholder - Stripe integration
    return {
        "session_id": "cs_test_123",
        "url": "https://checkout.stripe.com/pay/cs_test_123",
    }


@router.post("/webhooks/stripe")
async def handle_stripe_webhook(
    request: Request, stripe_signature: Optional[str] = Header(None)
):
    """Handle Stripe webhooks"""
    # Placeholder - Stripe webhook verification and processing
    return {"received": True}


@router.get("/invoices", response_model=List[InvoiceResponse])
async def list_invoices(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List organization invoices"""
    invoices = (
        db.query(Invoice)
        .filter(Invoice.organization_id == current_user.organization_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return invoices


@router.post("/usage", response_model=MessageResponse)
async def record_usage(
    current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Record usage event for billing"""
    # Placeholder - Usage tracking
    return {"message": "Usage recorded successfully"}
