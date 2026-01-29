from ..schema import DailyReport


def render_pdf(_report: DailyReport) -> bytes:
    # Placeholder: use weasyprint or wkhtmltopdf in production.
    # This returns an empty PDF-like payload to keep the interface stable.
    return b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
