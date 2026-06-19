from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.optimize import minimize


@dataclass(frozen=True)
class ReservoirParams:
    v_min_mcm: float = 50.0
    v_max_mcm: float = 200.0
    q_min_m3s: float = 10.0  # ecological flow
    q_max_m3s: float = 200.0
    seconds_per_day: float = 86400.0


def m3s_to_mcm_per_day(q_m3s: float, seconds_per_day: float = 86400.0) -> float:
    return q_m3s * seconds_per_day / 1e6


def revenue_for_release(q_m3s: float, price_per_mwh: float) -> float:
    """
    Simple hydropower revenue proxy:
      revenue = price * energy
    Here we use energy proportional to release (q) for a toy lab model.
    """
    energy_mwh = max(0.0, q_m3s) * 1.0  # scaling factor for lab simplicity
    return price_per_mwh * energy_mwh


def optimize_day(
    storage_mcm: float,
    inflow_m3s: float,
    price_per_mwh: float,
    params: ReservoirParams,
) -> tuple[float, float, float]:
    """
    Optimize a single day release decision.
    Returns (release_m3s, next_storage_mcm, revenue).
    """

    inflow_mcm_day = m3s_to_mcm_per_day(inflow_m3s, params.seconds_per_day)

    def next_storage(release_m3s: float) -> float:
        release_mcm_day = m3s_to_mcm_per_day(release_m3s, params.seconds_per_day)
        return storage_mcm + inflow_mcm_day - release_mcm_day

    def objective(x: np.ndarray) -> float:
        release = float(x[0])
        # negative revenue because scipy minimizes
        return -revenue_for_release(release, price_per_mwh)

    def storage_lower_constraint(x: np.ndarray) -> float:
        return next_storage(float(x[0])) - params.v_min_mcm

    def storage_upper_constraint(x: np.ndarray) -> float:
        return params.v_max_mcm - next_storage(float(x[0]))

    bounds = [(params.q_min_m3s, params.q_max_m3s)]
    constraints = [
        {"type": "ineq", "fun": storage_lower_constraint},
        {"type": "ineq", "fun": storage_upper_constraint},
    ]

    x0 = np.array([(params.q_min_m3s + params.q_max_m3s) / 2.0], dtype=float)
    res = minimize(objective, x0=x0, bounds=bounds, constraints=constraints, method="SLSQP")
    if not res.success:
        # Fall back to minimum ecological release if solver fails.
        release_opt = params.q_min_m3s
    else:
        release_opt = float(res.x[0])

    ns = next_storage(release_opt)
    # Clamp to be safe against numerical drift
    ns = float(min(max(ns, params.v_min_mcm), params.v_max_mcm))
    revenue = float(revenue_for_release(release_opt, price_per_mwh))
    return release_opt, ns, revenue


def optimize_7day(
    inflows_m3s: Iterable[float],
    prices_per_mwh: Iterable[float],
    initial_storage_mcm: float,
    params: ReservoirParams,
) -> dict:
    inflows = list(inflows_m3s)
    prices = list(prices_per_mwh)
    if len(inflows) != 7 or len(prices) != 7:
        raise ValueError("Provide exactly 7 inflows and 7 prices for the 7-day horizon.")

    storage = float(initial_storage_mcm)
    releases: list[float] = []
    storages: list[float] = [storage]
    revenues: list[float] = []

    for i in range(7):
        r, storage, rev = optimize_day(storage, inflows[i], prices[i], params)
        releases.append(r)
        storages.append(storage)
        revenues.append(rev)

    return {
        "releases_m3s": releases,
        "storages_mcm": storages,
        "revenues": revenues,
        "total_revenue": float(sum(revenues)),
    }


def main() -> None:
    params = ReservoirParams()

    inflows = [20, 18, 25, 22, 19, 21, 23]  # m3/s
    prices = [40, 38, 45, 44, 39, 41, 43]  # $/MWh (toy)
    initial_storage = 120.0  # MCM

    result = optimize_7day(inflows, prices, initial_storage, params)

    print("7-Day Reservoir Optimization (toy model)")
    print("-" * 40)
    for day, (q, s) in enumerate(zip(result["releases_m3s"], result["storages_mcm"][1:]), start=1):
        print(f"Day {day}: release={q:7.2f} m3/s | end storage={s:7.2f} MCM")
    print()
    print(f"Total revenue (proxy): {result['total_revenue']:.2f}")


if __name__ == "__main__":
    main()

