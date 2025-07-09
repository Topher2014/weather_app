"""
Data storage module for saving and loading weather data
"""

import csv
import os
from datetime import datetime
import config

class DataStorage:
    """Handles file-based storage of weather data"""
    
    def __init__(self):
        self.data_file = config.DATA_FILE
        self.fieldnames = [
            'city', 'temperature', 'feels_like', 'humidity', 
            'description', 'timestamp', 'date', 'time'
        ]
        print(f"DataStorage initialized with file: {self.data_file}")
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Create data file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
            print(f"Created new CSV file with headers: {self.data_file}")
        else:
            print(f"CSV file already exists: {self.data_file}")
    
    def save_weather_data(self, weather_data):
        """Save weather data to CSV file"""
        print(f"Attempting to save weather data: {weather_data}")
        
        try:
            # Load existing data
            existing_data = self.load_data()
            
            # Keep only last 99 entries
            if len(existing_data) >= 100:
                existing_data = existing_data[-99:]
                with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(existing_data)
            
            # Append new data
            with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writerow(weather_data)
            
            print(f"Successfully saved to CSV: {weather_data['city']}, {weather_data['temperature']}°F")
            
        except Exception as e:
            print(f"ERROR in save_weather_data: {e}")
            import traceback
            traceback.print_exc()
    
    def load_data(self):
        """Load weather data from CSV file"""
        try:
            data = []
            with open(self.data_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert numeric fields
                    if row.get('temperature'):
                        row['temperature'] = int(float(row['temperature']))
                    if row.get('feels_like'):
                        row['feels_like'] = int(float(row['feels_like']))
                    if row.get('humidity'):
                        row['humidity'] = int(float(row['humidity']))
                    data.append(row)
            return data
        except (FileNotFoundError, csv.Error):
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
    
    def save_data(self, data):
        """Save data list to CSV file"""
        try:
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"Error saving data to file: {e}")
    
    def get_recent_data(self, days=7):
        """Get recent weather data"""
        all_data = self.load_data()
        
        if not all_data:
            return []
        
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

