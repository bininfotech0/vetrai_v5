"""
Database models for Billing Service
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.models import BaseModel
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String


class Subscription(BaseModel):
    """Subscription model"""

    __tablename__ = "subscriptions"

    organization_id = Column(Integer, nullable=False, index=True)
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    plan = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    cancelled_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, default=dict)

    def __repr__(self):
        return (
            f"<Subscription(id={self.id}, "
            f"organization_id={self.organization_id}, plan='{self.plan}')>"
        )


class Invoice(BaseModel):
    """Invoice model"""

    __tablename__ = "invoices"

    organization_id = Column(Integer, nullable=False, index=True)
    subscription_id = Column(Integer, nullable=True, index=True)
    stripe_invoice_id = Column(String(255), unique=True, nullable=True)
    amount_due = Column(Integer, nullable=False)
    amount_paid = Column(Integer, nullable=False)
    currency = Column(String(10), nullable=False, default="usd")
    status = Column(String(50), nullable=False)
    invoice_pdf = Column(String(500), nullable=True)
    hosted_invoice_url = Column(String(500), nullable=True)
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<Invoice(id={self.id}, organization_id={self.organization_id}, "
            f"status='{self.status}')>"
        )
