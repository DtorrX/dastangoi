"""Minimal daily rollup logic for the MVP reporter service.

This file intentionally favors clarity and auditability over cleverness.
We want a working report today, not a perfect classifier or clustering engine.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List

from .schema import DailyReport, NormalizedEvent, ReportItem

# MVP defaults: keep these hard-coded for simplicity and explainability.
# Technical debt: make these configurable once a paying customer asks for it.
MAX_REPORT_ITEMS = 25
EXCERPT_CHARS = 240
DEFAULT_RATIONALE = [
    "Signal score from heuristics",
    "Requires human review",
]


def load_events(base: str, day: str) -> List[NormalizedEvent]:
    """Load normalized events for a given day.

    Shortcut: we keep a flat JSONL file per day. It's easy to audit and debug.
    Future upgrade path: move to a real database if volumes demand it.
    """
    path = os.path.join(base, day, "events.jsonl")
    if not os.path.exists(path):
        return []
    events = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            data = json.loads(line)
            events.append(NormalizedEvent(**data))
    return events


def build_daily_report(events: List[NormalizedEvent], day: str) -> DailyReport:
    """Build the minimal report used in the daily email and webhook payloads."""
    items: List[ReportItem] = []
    # MVP: cap items to keep the report readable and low-cost to generate.
    for event in events[:MAX_REPORT_ITEMS]:
        items.append(
            ReportItem(
                title=event.title,
                url=event.url,
                source=event.source,
                # Short excerpt keeps the report skimmable.
                excerpt=event.text[:EXCERPT_CHARS],
                signal_score=event.signal_score or 0.0,
                # Risk note: we do not claim truth, only signal strength.
                rationale=DEFAULT_RATIONALE,
            )
        )

    # Executive summary is intentionally short and plain-language.
    # It helps a first customer decide whether to investigate further.
    executive_summary = [
        "Signals-only report; confirm with human review.",
        f"Processed {len(events)} events.",
        "Top narratives are inferred from repeated phrasing and sources.",
        "No private or restricted content was accessed.",
        "Confidence scores are indicative, not factual claims.",
    ]

    # Shortcut: fake a single narrative cluster to keep the MVP moving.
    # Technical debt: replace with real clustering once we have revenue signal.
    narratives = [
        {
            "narrative": "Sample narrative cluster",
            "volume": len(events),
            "top_sources": list({event.source for event in events})[:5],
            "confidence": 0.6,
        }
    ]

    # MVP: one example network signal placeholder to show format.
    # Future upgrade: plug in domain/host co-occurrence analysis.
    network_signals = [
        {
            "domains": ["example.com"],
            "accounts": [],
            "note": "Repeated linking pattern; verify manually.",
        }
    ]

    # Recommendations are simple, human-readable nudges.
    # Risk: these are heuristic; keep them conservative to avoid overreach.
    recommendations = [
        "Add monitoring for specific region keywords.",
        "Review domains with repeated use and confirm ownership.",
    ]

    return DailyReport(
        date=day,
        executive_summary=executive_summary,
        narratives=narratives,
        notable_items=items,
        network_signals=network_signals,
        recommendations=recommendations,
    )


def resolve_rollup_day() -> str:
    """Resolve which day to roll up based on a UTC cutoff hour.

    Assumption: UTC is acceptable for the MVP; adjust for customer locale later.
    """
    cutoff_hour = int(os.environ.get("REPORT_CUTOFF_HOUR", "6"))
    now = datetime.utcnow()
    if now.hour < cutoff_hour:
        day = now - timedelta(days=1)
    else:
        day = now
    return day.strftime("%Y-%m-%d")
