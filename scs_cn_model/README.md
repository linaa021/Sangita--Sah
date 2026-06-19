🌦️ SCS-CN Runoff Simulation Model

> Experiment 4 of the Software Development coursework. This module implements rainfall-runoff modeling using the Soil Conservation Service Curve Number (SCS-CN) method and performs sensitivity analysis on hydrological parameters.


A Python-based hydrological simulation tool that models how rainfall is converted into surface runoff using the SCS-CN method. The system evaluates runoff behavior under different Curve Number (CN) conditions and generates both numerical and visual outputs for analysis.

It includes simulation, sensitivity analysis, visualization, and unit testing components.


What it does

- Simulates rainfall-runoff conversion using SCS-CN hydrological model
- Computes runoff depth based on Curve Number (CN)
- Performs sensitivity analysis across CN values
- Generates CSV dataset of rainfall vs runoff (`runoff_sensitivity.csv`)
- Visualizes rainfall-runoff relationship (`rainfall_vs_runoff_by_cn.png`)
- Validates model behavior using automated unit tests

The method

The SCS-CN model estimates runoff using hydrological relationships:


Q = (P - Ia)^2 / (P - Ia + S)


Where:

- Q = runoff depth  
- P = rainfall  
- Ia = initial abstraction  
- S = retention parameter based on CN  

Curve Number (CN) controls how much rainfall becomes runoff:

- High CN → high runoff (urban areas)
- Low CN → more infiltration (natural land)


Key components

- `scs_cn.py` → Core runoff computation model
- `sensitivity_analysis.py` → CN parameter sensitivity study
- `test_scs_cn.py` → Unit tests for validation
- `runoff_sensitivity.csv` → Generated simulation dataset
- `rainfall_vs_runoff_by_cn.png` → Visualization output
- `week5_sessionB_output.txt` → Execution log results

Features

- Rainfall-runoff simulation engine
- Curve Number sensitivity analysis
- Data export to CSV format
- Graphical visualization of hydrological response
- Automated testing for correctness validation

Requirements

- Python 3.10+
- NumPy
- Pandas
- Matplotlib

Install dependencies:

pip install -r requirements.txt
Usage
Run simulation
python scs_cn.py
Run sensitivity analysis
python sensitivity_analysis.py
Run tests
python -m pytest test_scs_cn.py
Project structure
scs_cn_model/
├── scs_cn.py
├── sensitivity_analysis.py
├── test_scs_cn.py
├── runoff_sensitivity.csv
├── rainfall_vs_runoff_by_cn.png
├── week5_sessionB_output.txt
├── requirements.txt
Result

The model demonstrates physically consistent hydrological behavior where runoff increases with rainfall and varies significantly depending on Curve Number sensitivity, matching expected real-world hydrology trends.