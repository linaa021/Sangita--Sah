from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_synthetic_dem(
    n: int = 100,
    elevation_min: float = 30.0,
    elevation_max: float = 80.0,
    seed: int = 42,
) -> np.ndarray:
    """
    Generate a synthetic DEM with hills/valleys using smooth sinusoidal structure + noise.
    Returns a (n, n) array of elevations in meters.
    """
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 2 * np.pi, n)
    y = np.linspace(0, 2 * np.pi, n)
    xx, yy = np.meshgrid(x, y, indexing="xy")

    base = (
        0.9 * np.sin(xx) * np.cos(yy)
        + 0.4 * np.sin(2 * xx + 0.7) * np.sin(yy + 1.1)
        - 0.6 * np.cos(xx + 0.2) * np.cos(2 * yy - 0.4)
    )
    noise = rng.normal(loc=0.0, scale=0.15, size=(n, n))
    terrain = base + noise

    # Normalize to [elevation_min, elevation_max]
    t_min, t_max = float(terrain.min()), float(terrain.max())
    scaled = (terrain - t_min) / (t_max - t_min)
    dem = elevation_min + scaled * (elevation_max - elevation_min)
    return dem.astype(float)


def simulate_flood(dem_m: np.ndarray, flood_level_m: float) -> tuple[np.ndarray, np.ndarray, float, float]:
    """
    Given DEM (m) and flood level (m), return:
    - flooded_mask: bool array
    - depth_m: depth array (m), 0 where not flooded
    - flooded_pct: percent of cells flooded (0-100)
    - avg_depth_m: average depth over flooded cells (0 if none)
    """
    flooded = dem_m < flood_level_m
    depth = np.where(flooded, flood_level_m - dem_m, 0.0)

    flooded_pct = float(100.0 * flooded.mean())
    avg_depth = float(depth[flooded].mean()) if flooded.any() else 0.0
    return flooded, depth, flooded_pct, avg_depth


def save_dem(dem_m: np.ndarray, out_path: Path) -> None:
    np.save(out_path, dem_m)


def plot_dem_heatmap(dem_m: np.ndarray, out_path: Path) -> None:
    plt.figure(figsize=(7, 6))
    im = plt.imshow(dem_m, cmap="terrain")
    plt.title("Synthetic DEM (m)")
    plt.xlabel("X (grid cells)")
    plt.ylabel("Y (grid cells)")
    cbar = plt.colorbar(im)
    cbar.set_label("Elevation (m)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_flood_overlays(dem_m: np.ndarray, levels: list[float], out_path: Path) -> None:
    fig, axes = plt.subplots(1, len(levels), figsize=(5 * len(levels), 5), constrained_layout=True)
    if len(levels) == 1:
        axes = [axes]

    for ax, level in zip(axes, levels):
        flooded, depth, flooded_pct, _ = simulate_flood(dem_m, level)

        ax.imshow(dem_m, cmap="gray", alpha=0.9)
        depth_masked = np.ma.masked_where(~flooded, depth)
        im = ax.imshow(depth_masked, cmap="Blues", alpha=0.65)
        ax.set_title(f"Flood level {level:.0f} m\nFlooded: {flooded_pct:.1f}%")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

    cbar = fig.colorbar(im, ax=axes, shrink=0.85)
    cbar.set_label("Inundation depth (m)")
    fig.suptitle("Flood Inundation Overlays", y=1.02)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_flooded_pct_vs_level(dem_m: np.ndarray, start: float = 40.0, end: float = 60.0, step: float = 1.0, out_path: Path | None = None) -> None:
    levels = np.arange(start, end + 1e-9, step, dtype=float)
    flooded_pcts = []
    for lvl in levels:
        flooded, _, flooded_pct, _ = simulate_flood(dem_m, float(lvl))
        flooded_pcts.append(flooded_pct)

    # Monotonicity check (should be non-decreasing)
    for a, b in zip(flooded_pcts, flooded_pcts[1:]):
        if b + 1e-9 < a:
            raise AssertionError("Flooded percentage is not monotonic with rising water level.")

    plt.figure(figsize=(8, 5))
    plt.plot(levels, flooded_pcts, marker="o")
    plt.title("Flooded Area vs Water Level")
    plt.xlabel("Flood level (m)")
    plt.ylabel("Flooded area (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    if out_path is not None:
        plt.savefig(out_path, dpi=200)
        plt.close()


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    dem_npy = out_dir / "synthetic_dem.npy"
    dem_png = out_dir / "synthetic_dem_heatmap.png"
    overlay_png = out_dir / "flood_overlays.png"
    curve_png = out_dir / "flooded_pct_vs_level.png"

    dem = generate_synthetic_dem()
    save_dem(dem, dem_npy)
    plot_dem_heatmap(dem, dem_png)

    levels = [40.0, 50.0, 60.0]
    plot_flood_overlays(dem, levels, overlay_png)
    plot_flooded_pct_vs_level(dem, start=40.0, end=60.0, step=1.0, out_path=curve_png)

    for lvl in levels:
        _, _, flooded_pct, avg_depth = simulate_flood(dem, lvl)
        print(f"Level {lvl:.0f} m -> flooded={flooded_pct:.1f}% | avg depth={avg_depth:.2f} m")

    print("Wrote synthetic_dem.npy and figures in this folder.")


if __name__ == "__main__":
    main()

