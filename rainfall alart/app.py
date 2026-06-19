from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from alerts import check_alert
from config import load_settings
from openweather_client import InvalidApiKeyError, OpenWeatherError, get_rainfall_observation
from storage import HistoryRow, append_history, now_utc_iso


def level_color(level: str) -> str:
    return {"GREEN": "#1f9d55", "YELLOW": "#f4b400", "RED": "#d93025"}.get(level, "#666666")


def main() -> None:
    st.set_page_config(page_title="Rainfall Monitoring", layout="wide")
    st.title("Rainfall Monitoring Dashboard")

    settings = load_settings()
    if not settings.api_key:
        st.info("No `OPENWEATHER_API_KEY` set. The app will fall back to demo data if API calls fail.")

    city = st.text_input("City", value="Seattle")
    history_path = Path(__file__).resolve().parent / "alert_history.csv"

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        refresh = st.button("Refresh")
    with col2:
        use_demo = st.checkbox("Force demo mode (offline)", value=False)

    if refresh:
        try:
            if use_demo:
                raise OpenWeatherError("Forced demo mode")
            obs = get_rainfall_observation(city, settings)
        except (InvalidApiKeyError, OpenWeatherError):
            # lightweight demo fallback
            import random
            from datetime import datetime, timezone

            from openweather_client import RainfallObservation

            obs = RainfallObservation(
                city=city,
                rainfall_mm_last_1h=float(random.choice([0.0, 0.5, 3.0, 9.8, 12.2, 18.6, 27.4])),
                observed_at_utc=datetime.now(timezone.utc),
                source="demo",
            )

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

    # Current status
    if history_path.exists():
        df = pd.read_csv(history_path)
        current = df.iloc[-1].to_dict()
        current_rain = float(current["rainfall_mm_last_1h"])
        current_level = str(current["alert_level"])
        current_source = str(current.get("source", "unknown"))
        current_ts = str(current["timestamp_utc"])
    else:
        current_rain = 0.0
        current_level = "GREEN"
        current_source = "none"
        current_ts = "N/A"

    colA, colB, colC, colD = st.columns(4)
    colA.metric("Current rainfall (mm last 1h)", f"{current_rain:.2f}")
    colB.metric("Alert level", current_level)
    colC.metric("Data source", current_source)
    colD.metric("Last update", current_ts)

    st.markdown(
        f"<div style='padding:10px;border-radius:8px;background:{level_color(current_level)};color:white;'>"
        f"<b>Status:</b> {current_level}"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.subheader("Alert history")
    if history_path.exists():
        df = pd.read_csv(history_path)
        st.dataframe(df.tail(50), use_container_width=True)
        st.line_chart(df.set_index("timestamp_utc")["rainfall_mm_last_1h"])
    else:
        st.write("No history yet. Click Refresh.")


if __name__ == "__main__":
    main()

