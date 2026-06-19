💧 Reservoir Optimization System

> Experiment 3 of the Software Development coursework. This module focuses on simulating and optimizing reservoir water release strategies under constrained hydrological conditions.

A Python-based simulation system that models reservoir behavior and computes optimized water release schedules. The goal is to maintain system stability while respecting physical constraints such as storage limits, inflow variation, and controlled discharge.

The system is implemented using a single optimization workflow script: `optimize_reservoir.py`.

 What it does

- Simulates reservoir inflow and storage dynamics over time
- Models water balance using time-step based computation
- Applies constraints on:
  - Maximum reservoir capacity
  - Minimum storage limits
  - Release rate boundaries
- Computes optimized release schedule for system stability
- Generates output logs for analysis (`week6_output.txt`)
- Tracks system behavior across simulation steps

 System behavior

At each time step, the model updates reservoir state:


Storage(t+1) = Storage(t) + Inflow(t) - Release(t)


Where:

- Inflow(t) is externally defined or simulated
- Release(t) is optimized under constraints
- Storage must remain within physical limits

 Key components

- `optimize_reservoir.py` → Core simulation and optimization logic
- `week6_output.txt` → Generated results from simulation runs
- `prompt_log.md` → Development and iteration history
- `requirements.txt` → Dependency configuration

 Optimization objective

The system aims to:

- Maintain reservoir stability over time
- Avoid overflow or underflow conditions
- Optimize release decisions based on inflow variation
- Ensure constraint satisfaction at every step


Requirements

- Python 3.10+
- NumPy

Install dependencies:

bash
pip install -r requirements.txt
Usage

Run the simulation:

python optimize_reservoir.py
Output
Time-series reservoir simulation results
Optimized release schedule
Constraint validation logs
Generated output file (week6_output.txt)
Project structure
reservoir_optimization/
├── optimize_reservoir.py
├── week6_output.txt
├── prompt_log.md
├── requirements.txt
Result

The system produces stable and feasible reservoir operation strategies that respect physical constraints while optimizing water release decisions over time.