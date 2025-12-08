"""
Pydantic schemas for Billing Service
"""
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class SubscriptionCreate(BaseModel):
    """Schema for creating a subscription"""
    plan_name: str = Field(..., min_length=1, max_length=100)
    trial_days: Optional[int] = Field(None, ge=0)


class SubscriptionResponse(BaseModel):
    """Schema for subscription response"""
    id: int
    organization_id: int
    stripe_subscription_id: Optional[str]
    stripe_customer_id: Optional[str]
    plan_name: str
    status: str
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    trial_end: Optional[datetime]
    canceled_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    """Schema for invoice response"""
    id: int
    subscription_id: int
    organization_id: int
    stripe_invoice_id: Optional[str]
    amount: Decimal
    currency: str
    status: str
    invoice_number: Optional[str]
    invoice_pdf: Optional[str]
    due_date: Optional[datetime]
    paid_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaymentResponse(BaseModel):
    """Schema for payment response"""
    id: int
    invoice_id: int
    organization_id: int
    stripe_payment_id: Optional[str]
    amount: Decimal
    currency: str
    payment_method: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class WebhookEvent(BaseModel):
    """Schema for Stripe webhook event"""
    type: str
    data: dict


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
