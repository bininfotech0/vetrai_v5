"""
Pydantic schemas for Billing Service
"""
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field


class SubscriptionCreate(BaseModel):
    """Schema for creating a subscription"""
    plan: str = Field(..., description="Plan name (free, pro, enterprise)")
    payment_method_id: Optional[str] = None


class SubscriptionResponse(BaseModel):
    """Schema for subscription response"""
    id: int
    organization_id: int
    stripe_subscription_id: Optional[str]
    plan: str
    status: str
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    cancel_at_period_end: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CheckoutSessionCreate(BaseModel):
    """Schema for creating a checkout session"""
    plan: str
    success_url: str
    cancel_url: str


class CheckoutSessionResponse(BaseModel):
    """Schema for checkout session response"""
    session_id: str
    url: str


class InvoiceResponse(BaseModel):
    """Schema for invoice response"""
    id: int
    organization_id: int
    subscription_id: Optional[int]
    stripe_invoice_id: Optional[str]
    amount_due: int
    amount_paid: int
    currency: str
    status: str
    invoice_pdf: Optional[str]
    hosted_invoice_url: Optional[str]
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class WebhookEvent(BaseModel):
    """Schema for Stripe webhook events"""
    type: str
    data: Dict


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
