import base64
import hashlib
import hmac
import os


def _secret() -> bytes:
    return os.environ.get("UNSUBSCRIBE_SECRET", "change-me").encode("utf-8")


def build_unsubscribe_token(email: str) -> str:
    signature = hmac.new(_secret(), email.encode("utf-8"), hashlib.sha256).digest()
    payload = f"{email}:{base64.urlsafe_b64encode(signature).decode('utf-8')}"
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8")


def verify_unsubscribe_token(token: str) -> str:
    decoded = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
    email, signature = decoded.split(":", 1)
    expected = build_unsubscribe_token(email).encode("utf-8")
    if not hmac.compare_digest(expected, token.encode("utf-8")):
        raise ValueError("Invalid token")
    return email
