from __future__ import annotations

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    timeout_s: float = 10.0
    cache_ttl_s: int = 600


def load_settings() -> Settings:
    # Use env var so keys never get committed.
    api_key = getenv("OPENWEATHER_API_KEY")
    return Settings(api_key=api_key if api_key else None)

