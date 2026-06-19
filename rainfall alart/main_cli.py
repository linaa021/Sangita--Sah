from __future__ import annotations

import argparse
import logging
import random
from pathlib import Path

from alerts import check_alert
from config import load_settings
from openweather_client import InvalidApiKeyError, OpenWeatherError, RainfallObservation, get_rainfall_observation
from storage import HistoryRow, append_history, now_utc_iso


def demo_observation(city: str) -> RainfallObservation:
    mm_1h = random.choice([0.0, 1.2, 4.5, 11.0, 17.8, 25.3])
    from datetime import datetime, timezone

    return RainfallObservation(
        city=city,
        rainfall_mm_last_1h=float(mm_1h),
        observed_at_utc=datetime.now(timezone.utc),
        source="demo",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Week 5A: Rainfall monitoring CLI")
    parser.add_argument("--city", default="Seattle", help="City name (OpenWeather search)")
    parser.add_argument("--history", default="alert_history.csv", help="CSV path for history")
    parser.add_argument("--demo", action="store_true", help="Run without OpenWeather (offline demo)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    settings = load_settings()
    history_path = Path(__file__).resolve().parent / args.history

    obs: RainfallObservation
    if args.demo:
        obs = demo_observation(args.city)
    else:
        try:
            obs = get_rainfall_observation(args.city, settings)
        except InvalidApiKeyError as exc:
            logging.getLogger(__name__).warning("%s Using demo mode instead.", exc)
            obs = demo_observation(args.city)
        except OpenWeatherError as exc:
            logging.getLogger(__name__).warning("API failed: %s Using demo mode instead.", exc)
            obs = demo_observation(args.city)

    alert = check_alert(obs.rainfall_mm_last_1h)
    append_history(
        history_path,
        HistoryRow(
            timestamp_utc=now_utc_iso(),
            city=obs.city,
            rainfall_mm_last_1h=obs.rainfall_mm_last_1h,
            alert_level=alert.level,
            alert_message=alert.message,
            source=obs.source,
        ),
    )

    print("Rainfall Monitoring (Week 5 Session A)")
    print("-" * 36)
    print(f"City: {obs.city}")
    print(f"Rainfall (last 1h): {obs.rainfall_mm_last_1h:.2f} mm")
    print(f"Alert: {alert.level} - {alert.message}")
    print(f"History CSV: {history_path.name}")


if __name__ == "__main__":
    main()

