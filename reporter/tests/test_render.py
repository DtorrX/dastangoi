from src.render.html import render_html
from src.render.md import render_markdown
from src.schema import DailyReport, ReportItem


def test_renderers(tmp_path):
    report = DailyReport(
        date="2026-01-01",
        executive_summary=["Summary"],
        narratives=[],
        notable_items=[
            ReportItem(
                title="Item",
                url="https://example.com",
                source="rss",
                excerpt="Text",
                signal_score=0.5,
            )
        ],
        network_signals=[],
        recommendations=[],
    )

    html = render_html(report, template_dir="reporter/templates")
    md = render_markdown(report, template_dir="reporter/templates")

    assert "Daily Signals" in html
    assert "Daily Signals" in md
