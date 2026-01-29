import hashlib


def canonical_hash(url: str, title: str) -> str:
    combined = f"{url.strip().lower()}|{title.strip().lower()}"
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()
