 🌧️ Rainfall Alart System

> Experiment 2 of the Software Development coursework. This system implements a real-time rainfall monitoring and alert generation pipeline using weather API data and modular Python components.


A Python-based weather monitoring system that collects rainfall data from an external API and generates alerts based on rainfall intensity levels. The system is designed with a modular architecture to separate data collection, processing, alert logic, and storage.

It supports both command-line execution and full application workflow through `app.py` and `main_cli.py`.


 What it does

- Retrieves live weather data using OpenWeather API (`openweather_client.py`)
- Processes rainfall information in real time
- Generates alerts based on rainfall thresholds
- Classifies conditions into:
  - Normal
  - Warning
  - Critical
- Stores alert history in CSV format (`alert_history.csv`)
- Provides CLI-based execution for manual monitoring

 System components

The project is divided into multiple modules:

- `app.py` → Main application entry point
- `main_cli.py` → Command-line interface for execution
- `alerts.py` → Alert generation and classification logic
- `config.py` → Configuration settings (thresholds, API keys)
- `openweather_client.py` → Handles API requests and responses
- `storage.py` → Stores alert history in CSV format
- `alert_history.csv` → Saved alert logs for analysis

Alert logic

Rainfall data is evaluated against predefined thresholds:


rainfall < threshold_1 → Normal
threshold_1 ≤ rainfall < threshold_2 → Warning
rainfall ≥ threshold_2 → Critical


Each incoming data update is processed and immediately classified into an alert level.


Requirements

- Python 3.10+
- requests (for API calls)

Install dependencies:

bash
pip install -r requirements.txt
Usage
Run main application
python app.py
Run CLI version
python main_cli.py
Output
Real-time rainfall monitoring
Alert classification (Normal / Warning / Critical)
Stored CSV logs of all detected events
Terminal-based system feedback
Project structure
rainfall alart/
├── app.py
├── main_cli.py
├── alerts.py
├── config.py
├── openweather_client.py
├── storage.py
├── alert_history.csv
├── requirements.txt
└── prompt_log.md
Result

The system successfully processes live rainfall data and generates structured alerts that can be stored and analyzed over time for weather pattern tracking.