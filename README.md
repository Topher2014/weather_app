# Weather App

A simple weather application that displays current weather for Sacramento, CA using OpenWeatherMap API, with city comparison features.

## Features
- Current weather display for Sacramento, CA
- Weekly average calculation
- Min/max temperature tracking
- Temperature difference analysis
- File-based data storage
- **NEW: City comparison from CSV files**

## City Comparison Feature
The app now compares Sacramento's weather with cities from CSV files in the `data/` directory:
- Automatically scans for CSV files in the data directory
- Extracts the first city from each properly formatted CSV
- Displays temperature differences, humidity, and conditions
- Supports multiple CSV formats with automatic column detection
- Shows results in an easy-to-read table format

### Supported CSV Formats
The app handles various CSV formats including:
- `city, temp, feels_like, humidity, description, date`
- `date, city, temp, feels_like, humidity, wind_speed, description`
- `weather_date, city, state, temp, humidity, rain, summary`
- Basic formats like `city, temperature, description`

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Get a free API key from OpenWeatherMap
3. Add your API key to `config.py`
4. Place comparison CSV files in the `data/` directory
5. Run: `python main.py`

## Requirements
- Python 3.6+
- OpenWeatherMap API key (free at openweathermap.org)

## File Structureweather-app/
├── data/
│   ├── weather_data.csv          # App's weather data
│   ├── your_comparison_files.csv # Your CSV files for comparison
│   └── ...
├── src/
│   ├── csv_comparator.py         # Handles CSV processing
│   ├── gui.py                    # Main GUI interface
│   ├── weather_api.py            # OpenWeatherMap API integration
│   ├── data_storage.py           # Data persistence
│   └── utils.py                  # Utility functions
├── config.py                     # Configuration settings
└── main.py                       # Application entry point## Usage
1. Start the application with `python main.py`
2. Click "Refresh Weather" to get current Sacramento weather
3. Click "Refresh Comparisons" to compare with cities from your CSV files
4. Enable auto-refresh for continuous updates

The comparison table shows:
- City name and state (if available)
- Current temperature
- Temperature difference vs Sacramento
- Humidity percentage
- Weather conditions
- Source CSV file
