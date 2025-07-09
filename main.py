"""
Weather App - Main Entry Point
Simple weather application for Sacramento, CA
"""

import os
import sys
from src.gui import WeatherGUI

def main():
    """Main function to start the weather application"""
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    try:
        # Start the GUI application
        app = WeatherGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
