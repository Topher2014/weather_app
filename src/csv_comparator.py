"""
CSV Comparator module for comparing Sacramento weather with other cities
"""

import os
import csv
from datetime import datetime
import config

class CSVComparator:
   """Handles CSV file processing and city comparison"""
   
   def __init__(self):
       self.data_dir = config.COMPARISON_CSV_DIR
       self.app_data_file = config.DATA_FILE
       
   def get_comparison_files(self):
       """Get list of CSV files to compare (excluding app's own data file)"""
       try:
           all_files = []
           if os.path.exists(self.data_dir):
               for file in os.listdir(self.data_dir):
                   if file.endswith('.csv') and file != os.path.basename(self.app_data_file):
                       all_files.append(os.path.join(self.data_dir, file))
           return all_files
       except Exception as e:
           print(f"Error getting comparison files: {e}")
           return []
   
   def normalize_column_names(self, headers):
       """Normalize different column name variations to standard format"""
       normalized = {}
       
       for i, header in enumerate(headers):
           header_lower = header.lower().strip()
           
           # Temperature mappings
           if header_lower in ['temp', 'temperature']:
               normalized['temperature'] = i
           elif header_lower in ['feels_like', 'feels like', 'apparent_temp']:
               normalized['feels_like'] = i
           
           # Location mappings
           elif header_lower in ['city', 'location', 'place']:
               normalized['city'] = i
           elif header_lower in ['state', 'region']:
               normalized['state'] = i
           
           # Weather condition mappings
           elif header_lower in ['description', 'conditions', 'weather', 'summary']:
               normalized['description'] = i
           elif header_lower in ['humidity', 'humid']:
               normalized['humidity'] = i
           elif header_lower in ['wind_speed', 'wind speed', 'wind']:
               normalized['wind_speed'] = i
           
           # Date/time mappings
           elif header_lower in ['date', 'weather_date', 'timestamp']:
               normalized['date'] = i
           elif header_lower in ['time']:
               normalized['time'] = i
       
       return normalized
   
   def parse_csv_file(self, file_path):
       """Parse a single CSV file and extract first city's data"""
       try:
           with open(file_path, 'r', encoding='utf-8') as file:
               # Try to detect if file has headers
               sample = file.read(1024)
               file.seek(0)
               sniffer = csv.Sniffer()
               has_header = sniffer.has_header(sample)
               
               reader = csv.reader(file)
               
               if has_header:
                   headers = next(reader)
                   column_map = self.normalize_column_names(headers)
                   
                   # Check if we have required columns
                   if 'city' not in column_map or 'temperature' not in column_map:
                       print(f"Skipping {file_path}: Missing required columns")
                       return None
                   
                   # Get first data row
                   try:
                       first_row = next(reader)
                       return self.extract_city_data(first_row, column_map, file_path)
                   except StopIteration:
                       print(f"Skipping {file_path}: No data rows")
                       return None
               else:
                   # No header, try to guess format based on first row
                   first_row = next(reader)
                   return self.guess_format_and_extract(first_row, file_path)
                   
       except Exception as e:
           print(f"Error parsing {file_path}: {e}")
           return None
   
   def extract_city_data(self, row, column_map, file_path):
       """Extract city data from a row using column mapping"""
       try:
           city_data = {
               'source_file': os.path.basename(file_path),
               'city': row[column_map['city']].strip(),
               'temperature': None,
               'feels_like': None,
               'humidity': None,
               'description': None,
               'state': None
           }
           
           # Extract temperature
           if 'temperature' in column_map:
               temp_str = row[column_map['temperature']].strip()
               try:
                   city_data['temperature'] = round(float(temp_str))
               except ValueError:
                   print(f"Invalid temperature in {file_path}: {temp_str}")
                   return None
           
           # Extract optional fields
           if 'feels_like' in column_map and column_map['feels_like'] < len(row):
               try:
                   city_data['feels_like'] = round(float(row[column_map['feels_like']]))
               except (ValueError, IndexError):
                   pass
           
           if 'humidity' in column_map and column_map['humidity'] < len(row):
               try:
                   city_data['humidity'] = int(float(row[column_map['humidity']]))
               except (ValueError, IndexError):
                   pass
           
           if 'description' in column_map and column_map['description'] < len(row):
               try:
                   city_data['description'] = row[column_map['description']].strip()
               except IndexError:
                   pass
           
           if 'state' in column_map and column_map['state'] < len(row):
               try:
                   city_data['state'] = row[column_map['state']].strip()
               except IndexError:
                   pass
           
           return city_data
           
       except Exception as e:
           print(f"Error extracting data from {file_path}: {e}")
           return None
   
   def guess_format_and_extract(self, row, file_path):
       """Attempt to guess format when no headers are present"""
       # Skip files that are clearly malformed
       if len(row) < 2:
           print(f"Skipping {file_path}: Too few columns")
           return None
       
       # Try common patterns
       try:
           # Pattern: city, temperature, description
           if len(row) >= 3:
               city = row[0].strip()
               temp = float(row[1])
               desc = row[2].strip()
               
               return {
                   'source_file': os.path.basename(file_path),
                   'city': city,
                   'temperature': round(temp),
                   'feels_like': None,
                   'humidity': None,
                   'description': desc,
                   'state': None
               }
       except (ValueError, IndexError):
           pass
       
       print(f"Skipping {file_path}: Could not determine format")
       return None
   
   def get_all_comparison_cities(self):
       """Get weather data for all cities from CSV files"""
       comparison_files = self.get_comparison_files()
       cities_data = []
       
       for file_path in comparison_files:
           city_data = self.parse_csv_file(file_path)
           if city_data:
               cities_data.append(city_data)
       
       return cities_data
   
   def compare_with_sacramento(self, sacramento_data):
       """Compare Sacramento weather with other cities"""
       if not sacramento_data:
           return []
       
       comparison_cities = self.get_all_comparison_cities()
       comparisons = []
       
       sacramento_temp = sacramento_data.get('temperature')
       sacramento_humidity = sacramento_data.get('humidity')
       
       for city_data in comparison_cities:
           comparison = {
               'city': city_data['city'],
               'state': city_data['state'],
               'temperature': city_data['temperature'],
               'feels_like': city_data['feels_like'],
               'humidity': city_data['humidity'],
               'description': city_data['description'],
               'source_file': city_data['source_file'],
               'temp_difference': None,
               'humidity_difference': None,
               'temp_comparison': None
           }
           
           # Calculate temperature difference
           if sacramento_temp is not None and city_data['temperature'] is not None:
               temp_diff = city_data['temperature'] - sacramento_temp
               comparison['temp_difference'] = temp_diff
               
               if temp_diff > 0:
                   comparison['temp_comparison'] = f"+{temp_diff}°F warmer"
               elif temp_diff < 0:
                   comparison['temp_comparison'] = f"{temp_diff}°F cooler"
               else:
                   comparison['temp_comparison'] = "Same temperature"
           
           # Calculate humidity difference
           if sacramento_humidity is not None and city_data['humidity'] is not None:
               humidity_diff = city_data['humidity'] - sacramento_humidity
               comparison['humidity_difference'] = humidity_diff
           
           comparisons.append(comparison)
       
       # Sort by temperature difference (closest to Sacramento first)
       comparisons.sort(key=lambda x: abs(x['temp_difference']) if x['temp_difference'] is not None else float('inf'))
       
       return comparisons
