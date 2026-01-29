import json
import os
from datetime import datetime
from typing import Iterable

from .schema import NormalizedEvent


def archive_path() -> str:
    base = os.environ.get("REPORT_ARCHIVE_PATH", "/data/archives")
    return base


def write_events(events: Iterable[NormalizedEvent]) -> str:
    base = archive_path()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    day_dir = os.path.join(base, today)
    os.makedirs(day_dir, exist_ok=True)
    out_path = os.path.join(day_dir, "events.jsonl")

    with open(out_path, "a", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event.model_dump()) + "\n")

    return out_path
