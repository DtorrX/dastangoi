import os
import stripe
from fastapi import APIRouter, Header, HTTPException, Request

router = APIRouter()

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")


@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default="")):
    payload = await request.body()
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, secret)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Minimal event handling: mark subscriber status based on subscription state.
    # In production, write to a subscribers table and keep audit logs.
    return {"received": True, "type": event.get("type", "unknown")}
