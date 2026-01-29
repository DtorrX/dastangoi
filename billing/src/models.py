from pydantic import BaseModel
from typing import Optional


class Subscriber(BaseModel):
    email: str
    plan: str
    status: str
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
