from __future__ import annotations

from datetime import date


def get_today_string() -> str:
    return date.today().isoformat()
