🌊 Smart Water Lab: Software Development Experiments

I built this for the 2025–2026 **Software Development course** at **Xi'an Jiaotong University**, one of the early university courses focusing on **AI-driven software engineering and applied simulation systems**.

Each experiment solves a different water-engineering problem using Python.  
For every assignment, I implemented all required features, then extended the system with optional improvements, additional validation logic, visualization tools, and automated test suites.

Each project is fully independent, reproducible, and includes both simulation logic and verification tests.


📌 Project Overview

1 · Rainfall Forecasting & Alert System

A real-time rainfall monitoring system that retrieves weather data from OpenWeatherMap and generates alerts based on rainfall intensity levels. It supports both CLI execution and interactive dashboard visualization.

| Feature | Status |
|--------|--------|
| OpenWeatherMap API integration and error handling | ✅ Required |
| Rainfall threshold alerts (Green / Yellow / Red) | ✅ Required |
| Streamlit dashboard with live updates | ✅ Required |
| Map visualization using Folium | ⭐ Extra |
| 5-day forecast prediction model | ⭐ Extra |
| Email alert notifications (SMTP) | ⭐ Extra |
| Simulation mode for testing | ⭐ Extra |
| Pytest validation suite for alert logic | ⭐ Extra |

📂 [`rainfall_alert/`](rainfall_alert/) · 🧾 [`prompt_log.md`](rainfall_alert/prompt_log.md)


 2 · SCS-CN Runoff Calculation Model

A hydrological model implementing the Soil Conservation Service Curve Number (SCS-CN) method to estimate rainfall runoff and analyze sensitivity to soil and land-use conditions.

| Feature | Status |
|--------|--------|
| Runoff computation `Q(P, CN)` with physical constraints | ✅ Required |
| Boundary condition validation (P=0, CN=100, etc.) | ✅ Required |
| Rainfall vs runoff sensitivity plots | ✅ Required |
| Time-area runoff routing | ⭐ Extra |
| Antecedent Moisture Condition adjustment | ⭐ Extra |
| Interactive CN/rainfall visualization | ⭐ Extra |
| Rational method comparison | ⭐ Extra |
| Full test suite with conservation checks | ⭐ Extra |

📂 [`scs-cn_runoff_calculation/`](scs-cn_runoff_calculation/) · 🧾 [`prompt_log.md`](scs-cn_runoff_calculation/prompt_log.md)


3 · Reservoir Dispatch Optimization

A constrained optimization model for reservoir water release planning over a 7-day period. The system balances hydropower revenue, storage constraints, and ecological flow requirements using numerical optimization methods.

| Feature | Status |
|--------|--------|
| 7-day reservoir dispatch optimization problem | ✅ Required |
| Mass balance + storage constraints | ✅ Required |
| Scipy-based constrained optimization solver | ✅ Required |
| Validation of system constraints | ✅ Required |
| Monte Carlo inflow uncertainty analysis | ⭐ Extra |
| Rolling horizon optimization | ⭐ Extra |
| Water quality dilution constraint | ⭐ Extra |
| Solver comparison (LP vs SLSQP vs L-BFGS-B) | ⭐ Extra |

📂 [`reservoir_optimization/`](reservoir_optimization/) · 🧾 [`prompt_log.md`](reservoir_optimization/prompt_log.md)

4 · Flood Inundation Analysis

A simulation system that models flood propagation over a Digital Elevation Model (DEM). It calculates flood extent, depth, and inundation percentage, and visualizes flood behavior under rising water levels.

| Feature | Status |
|--------|--------|
| DEM-based flood mask and depth calculation | ✅ Required |
| Flood visualization (overlay, heatmap, curve) | ✅ Required |
| Monotonic flood validation across water levels | ✅ Required |
| Physical validation checks (depth, bounds, consistency) | ✅ Required |
| Connected-component flood routing | ⭐ Extra |
| Building footprint flood barriers | ⭐ Extra |
| Animated flood simulation (GIF) | ⭐ Extra |
| Flood volume computation | ⭐ Extra |
| Full pytest suite (63 tests) | ⭐ Extra |

📂 [`flood_inundation/`](flood_inundation/) · 🧾 [`prompt_log.md`](flood_inundation/prompt_log.md)



🧪 Testing Summary

Each module includes a dedicated automated test suite.

| Project | Test Count | Coverage |
|--------|-----------|----------|
| Rainfall Alert System | 26 tests | API, alerts, logging |
| SCS-CN Model | 27 tests | runoff correctness + physical bounds |
| Reservoir Optimization | 22 tests | constraints + optimization correctness |
| Flood Inundation | 63 tests | simulation, routing, validation, visualization |


⚙️ Tech Stack

- Python 3.10+
- NumPy
- SciPy
- Matplotlib
- Pandas
- Requests
- Streamlit
- Folium
- Pytest



📁 Repository Structure


Smart-Water-Lab/
├── rainfall_alert/
├── scs-cn_runoff_calculation/
├── reservoir_optimization/
├── flood_inundation/
└── README.md



📌 Key Design Philosophy

Across all experiments, the following principles were applied:

- Each system is physically consistent with real hydrological behavior
- Every model is validated using automated test cases
- Extra features extend beyond assignment requirements
- Visualization is used to verify correctness, not just display results
- Code is modular and reproducible across environments


 🚀 Final Result

This repository demonstrates a complete pipeline of:

- environmental data processing
- hydrological simulation
- numerical optimization
- physical validation
- automated testing

