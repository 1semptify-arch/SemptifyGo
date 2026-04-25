"""
UTC Datetime Utilities
All times stored and processed in UTC.
"""

from datetime import datetime, timezone
from typing import Optional


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def utc_from_timestamp(timestamp: float) -> datetime:
    """Convert Unix timestamp to UTC datetime."""
    return datetime.fromtimestamp(timestamp, timezone.utc)


def format_utc(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime as ISO 8601 UTC string."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def parse_utc(iso_string: str) -> datetime:
    """Parse ISO 8601 string to UTC datetime."""
    # Handle various ISO formats
    if iso_string.endswith('Z'):
        iso_string = iso_string[:-1] + '+00:00'
    return datetime.fromisoformat(iso_string)
