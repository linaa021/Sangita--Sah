from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import requests
from cachetools import TTLCache, cached

from config import Settings

logger = logging.getLogger(__name__)


class OpenWeatherError(RuntimeError):
    pass


class CityNotFoundError(OpenWeatherError):
    pass


class InvalidApiKeyError(OpenWeatherError):
    pass


@dataclass(frozen=True)
class RainfallObservation:
    city: str
    rainfall_mm_last_1h: float
    observed_at_utc: datetime
    source: str  # "openweather" or "demo"


def _extract_rainfall_mm_last_1h(payload: dict[str, Any]) -> float:
    rain = payload.get("rain") or {}
    # OpenWeather often provides "1h" and/or "3h" rainfall in mm.
    mm_1h = rain.get("1h")
    if mm_1h is None:
        # Treat missing rainfall as 0 (explicit lab requirement).
        return 0.0
    try:
        return float(mm_1h)
    except (TypeError, ValueError):
        logger.warning("Unexpected rain['1h'] value: %r", mm_1h)
        return 0.0


def build_cached_fetcher(settings: Settings) -> tuple[TTLCache, Any]:
    cache = TTLCache(maxsize=256, ttl=settings.cache_ttl_s)

    @cached(cache)
    def fetch_city_weather(city: str) -> dict[str, Any]:
        if not settings.api_key:
            raise InvalidApiKeyError(
                "Missing OPENWEATHER_API_KEY env var. Set it to use live data."
            )

        params = {"q": city, "appid": settings.api_key, "units": "metric"}
        try:
            resp = requests.get(settings.base_url, params=params, timeout=settings.timeout_s)
        except requests.RequestException as exc:
            raise OpenWeatherError(f"Network error calling OpenWeather: {exc}") from exc

        if resp.status_code in (401, 403):
            raise InvalidApiKeyError("Invalid OpenWeather API key (401/403).")
        if resp.status_code == 404:
            raise CityNotFoundError(f"City not found: {city!r}")
        if not resp.ok:
            raise OpenWeatherError(f"OpenWeather error {resp.status_code}: {resp.text}")

        return resp.json()

    return cache, fetch_city_weather


def get_rainfall_observation(city: str, settings: Settings) -> RainfallObservation:
    cache, fetch_city_weather = build_cached_fetcher(settings)
    _ = cache  # cache is held by closure; returned mainly for debugging if needed

    payload = fetch_city_weather(city)
    mm_1h = _extract_rainfall_mm_last_1h(payload)
    return RainfallObservation(
        city=city,
        rainfall_mm_last_1h=mm_1h,
        observed_at_utc=datetime.now(timezone.utc),
        source="openweather",
    )

