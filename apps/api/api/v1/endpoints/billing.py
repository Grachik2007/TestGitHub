from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class SubscriptionPlan(BaseModel):
    name: str
    price: float
    features: List[str]
    tokens_per_month: int


class Subscription(BaseModel):
    plan: str
    status: str
    tokens_used: int
    tokens_limit: int
    renewal_date: str
    cancel_at_period_end: bool = False


class Invoice(BaseModel):
    invoice_id: str
    amount: float
    date: str
    status: str


@router.get("/plans", response_model=List[SubscriptionPlan])
async def get_plans():
    """Get available subscription plans."""
    # TODO: Implement plans retrieval
    return [
        {
            "name": "Starter",
            "price": 29.0,
            "features": ["5 agents", "1000 tokens/month"],
            "tokens_per_month": 1000,
        },
        {
            "name": "Pro",
            "price": 99.0,
            "features": ["10 agents", "10000 tokens/month"],
            "tokens_per_month": 10000,
        },
    ]


@router.get("/subscription", response_model=Subscription)
async def get_subscription():
    """Get user subscription."""
    # TODO: Implement subscription retrieval
    return {
        "plan": "Pro",
        "status": "active",
        "tokens_used": 5000,
        "tokens_limit": 10000,
        "renewal_date": "2024-02-23",
    }


@router.post("/subscribe")
async def subscribe(plan: str):
    """Subscribe to a plan."""
    # TODO: Implement subscription creation
    return {"message": f"Subscribed to {plan} plan"}


@router.post("/cancel")
async def cancel_subscription():
    """Cancel subscription."""
    # TODO: Implement subscription cancellation
    return {"message": "Subscription cancelled"}


@router.get("/invoices", response_model=List[Invoice])
async def get_invoices():
    """Get invoices."""
    # TODO: Implement invoices retrieval
    return [
        {
            "invoice_id": "inv-001",
            "amount": 99.0,
            "date": "2024-01-23",
            "status": "paid",
        }
    ]
