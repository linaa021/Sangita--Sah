from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scs_cn import calculate_runoff


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    fig_path = out_dir / "rainfall_vs_runoff_by_cn.png"
    csv_path = out_dir / "runoff_sensitivity.csv"

    cns = [60, 70, 80, 90, 95]
    rainfall = np.arange(0, 101, 1, dtype=float)  # 0..100 mm

    rows: list[dict] = []
    for cn in cns:
        for p in rainfall:
            q = calculate_runoff(float(p), float(cn))
            rows.append({"P_mm": float(p), "CN": int(cn), "Q_mm": float(q)})

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

    plt.figure(figsize=(10, 6))
    for cn in cns:
        sub = df[df["CN"] == cn]
        plt.plot(sub["P_mm"], sub["Q_mm"], label=f"CN={cn}")

    plt.title("SCS-CN Sensitivity: Rainfall vs Runoff")
    plt.xlabel("Rainfall P (mm)")
    plt.ylabel("Runoff Q (mm)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, dpi=200)

    print(f"Wrote {csv_path.name}")
    print(f"Wrote {fig_path.name}")


if __name__ == "__main__":
    main()

