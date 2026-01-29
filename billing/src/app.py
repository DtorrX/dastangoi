from datetime import datetime
import os
import stripe
from fastapi import FastAPI, Depends

from .stripe_webhooks import router as webhook_router
from .auth import require_admin

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

app = FastAPI(title="Disinfo Billing")
app.include_router(webhook_router, prefix="/webhooks")


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/checkout")
def create_checkout_session(plan: str, _: bool = Depends(require_admin)):
    price_map = {
        "free": os.environ.get("STRIPE_PRICE_FREE", ""),
        "paid": os.environ.get("STRIPE_PRICE_PAID", ""),
        "pro": os.environ.get("STRIPE_PRICE_PRO", ""),
    }
    price_id = price_map.get(plan)
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return {"url": session.url}
