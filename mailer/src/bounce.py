from fastapi import APIRouter

router = APIRouter()


@router.post("/bounce")
def bounce_handler(payload: dict):
    # Placeholder: log and mark subscriber as suppressed.
    return {"received": True}
