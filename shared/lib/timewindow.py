from datetime import datetime, timedelta


def previous_day_window(reference: datetime) -> tuple[datetime, datetime]:
    end = reference.replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=1)
    return start, end
