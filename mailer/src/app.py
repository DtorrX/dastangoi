from datetime import datetime
import os
from fastapi import FastAPI, HTTPException

from .ses import send_email
from .queue import batch_recipients, load_recipients
from .unsubscribe import build_unsubscribe_token, verify_unsubscribe_token
from .bounce import router as bounce_router

app = FastAPI(title="Disinfo Mailer")
app.include_router(bounce_router, prefix="/webhooks")


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/send")
def send_report(payload: dict):
    subject = payload.get("subject", "Daily Signals Report")
    html = payload.get("html", "")
    text = payload.get("text", "")

    if not html or not text:
        raise HTTPException(status_code=400, detail="Missing report body")

    recipients = load_recipients()
    results = []

    for batch in batch_recipients(recipients.keys()):
        for email in batch:
            token = build_unsubscribe_token(email)
            unsubscribe_url = f"{os.environ.get('APP_BASE_URL', '')}/unsubscribe?token={token}"
            html_with_link = f"{html}<p>Unsubscribe: {unsubscribe_url}</p>"
            text_with_link = f"{text}\nUnsubscribe: {unsubscribe_url}"

            result = send_email(email, subject, html_with_link, text_with_link)
            results.append({"email": email, **result})

    return {"sent": len(results), "results": results}


@app.get("/unsubscribe")
def unsubscribe(token: str):
    try:
        email = verify_unsubscribe_token(token)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Placeholder: write email to a suppression list or database.
    return {"unsubscribed": True, "email": email}
