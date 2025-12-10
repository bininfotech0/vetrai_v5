"""
Database models for Billing Service
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text, Enum as SQLEnum
from shared.models import BaseModel
import enum


class SubscriptionStatus(enum.Enum):
    """Subscription status enumeration"""
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"


class InvoiceStatus(enum.Enum):
    """Invoice status enumeration"""
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    VOID = "void"
    UNCOLLECTIBLE = "uncollectible"


class Subscription(BaseModel):
    """Subscription model"""
    
    __tablename__ = "subscriptions"
    
    organization_id = Column(Integer, nullable=False, index=True)
    stripe_subscription_id = Column(String(255), nullable=True, unique=True, index=True)
    stripe_customer_id = Column(String(255), nullable=True, index=True)
    
    plan_name = Column(String(100), nullable=False)
    status = Column(SQLEnum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.ACTIVE)
    
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    trial_end = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, org_id={self.organization_id}, status='{self.status.value}')>"


class Invoice(BaseModel):
    """Invoice model"""
    
    __tablename__ = "invoices"
    
    subscription_id = Column(Integer, nullable=False, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    stripe_invoice_id = Column(String(255), nullable=True, unique=True, index=True)
    
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    status = Column(SQLEnum(InvoiceStatus), nullable=False, default=InvoiceStatus.DRAFT)
    
    invoice_number = Column(String(50), nullable=True)
    invoice_pdf = Column(Text, nullable=True)
    
    due_date = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, invoice_number='{self.invoice_number}', status='{self.status.value}')>"


class Payment(BaseModel):
    """Payment model"""
    
    __tablename__ = "payments"
    
    invoice_id = Column(Integer, nullable=False, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    stripe_payment_id = Column(String(255), nullable=True, unique=True, index=True)
    
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    
    payment_method = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False)
    
    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status='{self.status}')>"
