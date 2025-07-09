"""
Utility functions for weather calculations and analysis
"""

from datetime import datetime, timedelta

class WeatherUtils:
    """Utility functions for weather data analysis"""
    
    @staticmethod
    def calculate_weekly_average(weather_data):
        """
        Calculate weekly average temperature
        Args: weather_data (list): List of weather data dictionaries
        Returns: float: Average temperature or None if no data
        """
        if not weather_data:
            return None
        
        temperatures = []
        for entry in weather_data:
            try:
                temp = entry.get('temperature')
                if temp is not None:
                    temperatures.append(float(temp))
            except (ValueError, TypeError):
                continue
        
        if not temperatures:
            return None
        
        return round(sum(temperatures) / len(temperatures), 1)
    
    @staticmethod
    def find_min_max_temps(weather_data):
        """
        Find minimum and maximum temperatures
        Args: weather_data (list): List of weather data dictionaries
        Returns: tuple: (min_temp, max_temp) or (None, None) if no data
        """
        if not weather_data:
            return None, None
        
        temperatures = []
        for entry in weather_data:
            try:
                temp = entry.get('temperature')
                if temp is not None:
                    temperatures.append(float(temp))
            except (ValueError, TypeError):
                continue
        
        if not temperatures:
            return None, None
        
        return min(temperatures), max(temperatures)
    
    @staticmethod
    def calculate_temperature_difference(current_temp, previous_temp):
        """
        Calculate temperature difference from previous reading
        Args: current_temp (float): Current temperature
              previous_temp (float): Previous temperature
        Returns: float: Temperature difference (positive = warmer, negative = cooler)
        """
        if current_temp is None or previous_temp is None:
            return None
        
        try:
            return round(float(current_temp) - float(previous_temp), 1)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def get_previous_temperature(weather_data):
        """
        Get the most recent previous temperature reading
        Args: weather_data (list): List of weather data dictionaries
        Returns: float: Previous temperature or None if no data
        """
        if len(weather_data) < 2:
            return None
        
        # Sort by timestamp (most recent first)
        try:
            sorted_data = sorted(weather_data, 
                               key=lambda x: datetime.fromisoformat(x['timestamp']), 
                               reverse=True)
            
            # Return second most recent temperature
            prev_temp = sorted_data[1].get('temperature')
            return float(prev_temp) if prev_temp is not None else None
            
        except (ValueError, TypeError, KeyError):
            return None
    
    @staticmethod
    def format_temperature_change(temp_diff):
        """
        Format temperature change for display
        Args: temp_diff (float): Temperature difference
        Returns: string: Formatted temperature change
        """
        if temp_diff is None:
            return "No previous data"
        
        if temp_diff > 0:
            return f"+{temp_diff}°F (warmer)"
        elif temp_diff < 0:
            return f"{temp_diff}°F (cooler)"
        else:
            return "No change"
