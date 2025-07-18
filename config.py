# Configuration settings for the weather app

# OpenWeatherMap API configuration
API_KEY = "eaf68ffb413d707283399af330d02c3f"  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Location settings
CITY = "Sacramento"
STATE = "CA"
COUNTRY = "US"

# Data storage settings
DATA_FILE = "data/weather_data.csv"  # Changed from .json to .csv
COMPARISON_CSV_DIR = "data/"  # Directory to scan for comparison CSV files

# GUI settings
WINDOW_TITLE = "Sacramento Weather App"
WINDOW_SIZE = "600x550"  # Made larger to accommodate comparison section
REFRESH_INTERVAL = 300000  # 5 minutes in milliseconds
