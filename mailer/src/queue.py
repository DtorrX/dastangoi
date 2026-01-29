from typing import Iterable, Dict


def batch_recipients(recipients: Iterable[str], size: int = 50):
    batch = []
    for recipient in recipients:
        batch.append(recipient)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def load_recipients() -> Dict[str, str]:
    # Placeholder for subscriber lookup; in production read from billing DB.
    return {
        "demo@example.com": "paid",
    }
