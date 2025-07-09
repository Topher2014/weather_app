"""
Weather API module for fetching data from OpenWeatherMap
"""

import requests
import json
from datetime import datetime
import config

class WeatherAPI:
    """Handles weather data fetching from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = config.API_KEY
        self.base_url = config.BASE_URL
        self.city = config.CITY
        self.state = config.STATE
        self.country = config.COUNTRY
    
    def fetch_current_weather(self):
        """
        Fetch current weather data for Sacramento
        Returns: dict with weather data or None if error
        """
        try:
            # Build the API URL
            location = f"{self.city},{self.state},{self.country}"
            url = f"{self.base_url}?q={location}&appid={self.api_key}&units=imperial"
            
            # Make API request
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract relevant weather information
            weather_data = {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].title(),
                'timestamp': datetime.now().isoformat(),
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M:%S')
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None
        except KeyError as e:
            print(f"Data parsing error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def is_api_key_valid(self):
        """Check if API key is configured"""
        return self.api_key and self.api_key != "your_api_key_here"
