from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Alert:
    level: str  # GREEN/YELLOW/RED
    message: str
    rainfall_mm_per_h: float
    created_at_utc: datetime


def check_alert(rainfall_mm_per_h: float) -> Alert:
    if rainfall_mm_per_h < 0:
        raise ValueError("Rainfall cannot be negative.")

    if rainfall_mm_per_h < 10:
        level = "GREEN"
        message = "Normal conditions."
    elif rainfall_mm_per_h <= 20:
        level = "YELLOW"
        message = "Elevated rainfall. Monitor conditions."
    else:
        level = "RED"
        message = "High rainfall. Flood risk may be elevated."

    alert = Alert(
        level=level,
        message=message,
        rainfall_mm_per_h=float(rainfall_mm_per_h),
        created_at_utc=datetime.now(timezone.utc),
    )
    logger.info("Alert generated: %s (rain=%.2f mm/h)", alert.level, alert.rainfall_mm_per_h)
    return alert

