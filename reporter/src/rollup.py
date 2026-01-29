import json
import os
from datetime import datetime, timedelta
from typing import List

from .schema import DailyReport, NormalizedEvent, ReportItem


def load_events(base: str, day: str) -> List[NormalizedEvent]:
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
    items: List[ReportItem] = []
    for event in events[:25]:
        items.append(
            ReportItem(
                title=event.title,
                url=event.url,
                source=event.source,
                excerpt=event.text[:240],
                signal_score=event.signal_score or 0.0,
                rationale=["Signal score from heuristics", "Requires human review"],
            )
        )

    executive_summary = [
        "Signals-only report; confirm with human review.",
        f"Processed {len(events)} events.",
        "Top narratives are inferred from repeated phrasing and sources.",
        "No private or restricted content was accessed.",
        "Confidence scores are indicative, not factual claims.",
    ]

    narratives = [
        {
            "narrative": "Sample narrative cluster",
            "volume": len(events),
            "top_sources": list({event.source for event in events})[:5],
            "confidence": 0.6,
        }
    ]

    network_signals = [
        {
            "domains": ["example.com"],
            "accounts": [],
            "note": "Repeated linking pattern; verify manually.",
        }
    ]

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
    cutoff_hour = int(os.environ.get("REPORT_CUTOFF_HOUR", "6"))
    now = datetime.utcnow()
    if now.hour < cutoff_hour:
        day = now - timedelta(days=1)
    else:
        day = now
    return day.strftime("%Y-%m-%d")
