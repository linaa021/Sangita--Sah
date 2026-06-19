from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class HistoryRow:
    timestamp_utc: str
    city: str
    rainfall_mm_last_1h: float
    alert_level: str
    alert_message: str
    source: str


def append_history(csv_path: Path, row: HistoryRow) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not csv_path.exists()

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(row).keys()))
        if is_new:
            writer.writeheader()
        writer.writerow(asdict(row))


def now_utc_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

