from src.rollup import build_daily_report
from src.schema import NormalizedEvent


def test_build_daily_report():
    event = NormalizedEvent(
        source="rss",
        url="https://example.com",
        title="Example",
        published_at="2026-01-01",
        text="Sample text",
        language="en",
    )
    report = build_daily_report([event], "2026-01-01")
    assert report.date == "2026-01-01"
    assert report.notable_items
