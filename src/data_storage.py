"""
Data storage module for saving and loading weather data
"""

import json
import os
from datetime import datetime
import config

class DataStorage:
    """Handles file-based storage of weather data"""
    
    def __init__(self):
        self.data_file = config.DATA_FILE
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Create data file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            # Create directory if needed
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            # Create empty data file
            self.save_data([])
    
    def save_weather_data(self, weather_data):
        """
        Save weather data to file
        Args: weather_data (dict): Weather data to save
        """
        try:
            # Load existing data
            existing_data = self.load_data()
            
            # Add new data
            existing_data.append(weather_data)
            
            # Keep only last 100 entries to prevent file from growing too large
            if len(existing_data) > 100:
                existing_data = existing_data[-100:]
            
            # Save updated data
            self.save_data(existing_data)
            
        except Exception as e:
            print(f"Error saving weather data: {e}")
    
    def load_data(self):
        """
        Load weather data from file
        Returns: list of weather data dictionaries
        """
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
    
    def save_data(self, data):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data to file: {e}")
    
    def get_recent_data(self, days=7):
        """
        Get recent weather data
        Args: days (int): Number of days to look back
        Returns: list of recent weather data
        """
        all_data = self.load_data()
        
        if not all_data:
            return []
        
        # Filter data from last N days
        recent_data = []
        current_date = datetime.now()
        
        for entry in all_data:
            try:
                entry_date = datetime.fromisoformat(entry['timestamp'])
                days_diff = (current_date - entry_date).days
                
                if days_diff <= days:
                    recent_data.append(entry)
            except (KeyError, ValueError):
                continue
        
        return recent_data

