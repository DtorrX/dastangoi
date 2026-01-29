import os
from fastapi import Header, HTTPException


def require_admin(x_admin_key: str = Header(default="")):
    expected = os.environ.get("ADMIN_API_KEY", "")
    if expected and x_admin_key != expected:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    return True
