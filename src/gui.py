"""
GUI module using Tkinter for the weather application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import config
from src.weather_api import WeatherAPI
from src.data_storage import DataStorage
from src.utils import WeatherUtils
from src.csv_comparator import CSVComparator

class WeatherGUI:
   """Main GUI class for the weather application"""
   
   def __init__(self):
       self.root = tk.Tk()
       self.weather_api = WeatherAPI()
       self.data_storage = DataStorage()
       self.utils = WeatherUtils()
       self.csv_comparator = CSVComparator()
       self.current_weather = None
       
       self.setup_window()
       self.create_widgets()
       self.check_api_key()
       
   def setup_window(self):
       """Configure the main window"""
       self.root.title(config.WINDOW_TITLE)
       self.root.geometry("650x700")  # Made larger for comparison section
       self.root.resizable(True, True)
       self.root.minsize(600, 650)
       
       # Center the window
       self.root.update_idletasks()
       x = (self.root.winfo_screenwidth() // 2) - (650 // 2)
       y = (self.root.winfo_screenheight() // 2) - (700 // 2)
       self.root.geometry(f"650x700+{x}+{y}")
   
   def create_widgets(self):
       """Create and arrange GUI widgets"""
       # Main frame with scrollbar capability
       main_frame = ttk.Frame(self.root, padding="20")
       main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
       
       # Title
       title_label = ttk.Label(main_frame, text="Sacramento Weather", 
                              font=("Arial", 16, "bold"))
       title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
       
       # Current weather section
       self.create_current_weather_section(main_frame)
       
       # Statistics section
       self.create_statistics_section(main_frame)
       
       # Buttons
       self.create_buttons(main_frame)
       
       # City comparisons section
       self.create_comparison_section(main_frame)
       
       # Status bar
       self.status_var = tk.StringVar()
       self.status_var.set("Ready - Click 'Refresh Weather' to get data")
       status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W)
       status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))
       
       # Configure grid weights for resizing
       main_frame.columnconfigure(1, weight=1)
       self.root.columnconfigure(0, weight=1)
       self.root.rowconfigure(0, weight=1)
   
   def create_current_weather_section(self, parent):
       """Create current weather display section"""
       # Current weather frame
       weather_frame = ttk.LabelFrame(parent, text="Current Weather", padding="15")
       weather_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
       
       # Temperature
       ttk.Label(weather_frame, text="Temperature:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=2)
       self.temp_var = tk.StringVar()
       self.temp_var.set("--°F")
       ttk.Label(weather_frame, textvariable=self.temp_var, 
                font=("Arial", 12, "bold")).grid(row=0, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Feels like
       ttk.Label(weather_frame, text="Feels like:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=2)
       self.feels_like_var = tk.StringVar()
       self.feels_like_var.set("--°F")
       ttk.Label(weather_frame, textvariable=self.feels_like_var, font=("Arial", 10)).grid(row=1, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Description
       ttk.Label(weather_frame, text="Conditions:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
       self.desc_var = tk.StringVar()
       self.desc_var.set("--")
       ttk.Label(weather_frame, textvariable=self.desc_var, font=("Arial", 10)).grid(row=2, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Humidity
       ttk.Label(weather_frame, text="Humidity:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=2)
       self.humidity_var = tk.StringVar()
       self.humidity_var.set("--%")
       ttk.Label(weather_frame, textvariable=self.humidity_var, font=("Arial", 10)).grid(row=3, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Last updated
       ttk.Label(weather_frame, text="Last updated:", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=2)
       self.updated_var = tk.StringVar()
       self.updated_var.set("Never")
       ttk.Label(weather_frame, textvariable=self.updated_var, font=("Arial", 10)).grid(row=4, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Configure column weights
       weather_frame.columnconfigure(1, weight=1)
   
   def create_statistics_section(self, parent):
       """Create statistics display section"""
       # Statistics frame
       stats_frame = ttk.LabelFrame(parent, text="7-Day Statistics", padding="15")
       stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
       
       # Weekly average
       ttk.Label(stats_frame, text="Weekly Average:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=2)
       self.avg_var = tk.StringVar()
       self.avg_var.set("--°F")
       ttk.Label(stats_frame, textvariable=self.avg_var, font=("Arial", 10)).grid(row=0, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Min/Max temperatures
       ttk.Label(stats_frame, text="Min Temperature:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=2)
       self.min_var = tk.StringVar()
       self.min_var.set("--°F")
       ttk.Label(stats_frame, textvariable=self.min_var, font=("Arial", 10)).grid(row=1, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       ttk.Label(stats_frame, text="Max Temperature:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
       self.max_var = tk.StringVar()
       self.max_var.set("--°F")
       ttk.Label(stats_frame, textvariable=self.max_var, font=("Arial", 10)).grid(row=2, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Temperature change
       ttk.Label(stats_frame, text="Since Last Reading:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=2)
       self.change_var = tk.StringVar()
       self.change_var.set("No previous data")
       ttk.Label(stats_frame, textvariable=self.change_var, font=("Arial", 10)).grid(row=3, column=1, sticky=tk.W, padx=(15, 0), pady=2)
       
       # Configure column weights
       stats_frame.columnconfigure(1, weight=1)
   
   def create_buttons(self, parent):
       """Create control buttons"""
       button_frame = ttk.Frame(parent)
       button_frame.grid(row=3, column=0, columnspan=2, pady=(15, 15))
       
       # Refresh button - Make it more prominent
       self.refresh_btn = ttk.Button(button_frame, text="🔄 Refresh Weather", 
                                    command=self.refresh_weather,
                                    width=20)
       self.refresh_btn.pack(side=tk.TOP, pady=(0, 10))
       
       # Auto-refresh checkbox
       self.auto_refresh_var = tk.BooleanVar()
       auto_refresh_cb = ttk.Checkbutton(button_frame, text="Auto-refresh every 5 minutes", 
                                        variable=self.auto_refresh_var,
                                        command=self.toggle_auto_refresh)
       auto_refresh_cb.pack(side=tk.TOP)
   
   def create_comparison_section(self, parent):
       """Create city comparison section"""
       # Comparison frame
       comp_frame = ttk.LabelFrame(parent, text="City Comparisons", padding="15")
       comp_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
       
       # Create treeview for comparison data
       columns = ('City', 'Temperature', 'Difference', 'Humidity', 'Conditions', 'Source')
       self.comparison_tree = ttk.Treeview(comp_frame, columns=columns, show='headings', height=6)
       
       # Configure column headings
       self.comparison_tree.heading('City', text='City')
       self.comparison_tree.heading('Temperature', text='Temperature')
       self.comparison_tree.heading('Difference', text='vs Sacramento')
       self.comparison_tree.heading('Humidity', text='Humidity')
       self.comparison_tree.heading('Conditions', text='Conditions')
       self.comparison_tree.heading('Source', text='Source File')
       
       # Configure column widths
       self.comparison_tree.column('City', width=100)
       self.comparison_tree.column('Temperature', width=80)
       self.comparison_tree.column('Difference', width=120)
       self.comparison_tree.column('Humidity', width=70)
       self.comparison_tree.column('Conditions', width=120)
       self.comparison_tree.column('Source', width=120)
       
       # Add scrollbar
       scrollbar = ttk.Scrollbar(comp_frame, orient=tk.VERTICAL, command=self.comparison_tree.yview)
       self.comparison_tree.configure(yscrollcommand=scrollbar.set)
       
       # Pack treeview and scrollbar
       self.comparison_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
       scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
       
       # Refresh comparisons button
       refresh_comp_btn = ttk.Button(comp_frame, text="🔄 Refresh Comparisons", 
                                    command=self.refresh_comparisons,
                                    width=20)
       refresh_comp_btn.grid(row=1, column=0, pady=(10, 0))
       
       # Configure grid weights
       comp_frame.columnconfigure(0, weight=1)
       comp_frame.rowconfigure(0, weight=1)
   
   def check_api_key(self):
       """Check if API key is configured"""
       if not self.weather_api.is_api_key_valid():
           messagebox.showerror("Configuration Error", 
                              "Please add your OpenWeatherMap API key to config.py")
           self.status_var.set("Error: API key not configured")
           return False
       return True
   
   def refresh_weather(self):
       """Fetch and display current weather"""
       if not self.check_api_key():
           return
       
       self.status_var.set("Fetching weather data...")
       self.refresh_btn.config(state='disabled')
       
       # Use after() to prevent GUI freezing
       self.root.after(100, self._fetch_weather_data)
   
   def _fetch_weather_data(self):
       """Internal method to fetch weather data"""
       try:
           # Fetch current weather
           weather_data = self.weather_api.fetch_current_weather()
           
           if weather_data:
               self.current_weather = weather_data
               
               # Save to file
               self.data_storage.save_weather_data(weather_data)
               
               # Update GUI
               self.update_weather_display(weather_data)
               self.update_statistics()
               
               # Auto-refresh comparisons when weather is updated
               self.refresh_comparisons()
               
               self.status_var.set("Weather data updated successfully")
           else:
               self.status_var.set("Error: Failed to fetch weather data - Check API key and internet connection")
               messagebox.showerror("Error", "Failed to fetch weather data.\n\nPossible causes:\n• API key needs time to activate (wait 1 hour)\n• Internet connection issue\n• API rate limit reached")
               
       except Exception as e:
           self.status_var.set(f"Error: {str(e)}")
           messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
       
       finally:
           self.refresh_btn.config(state='normal')
   
   def update_weather_display(self, weather_data):
       """Update current weather display"""
       self.temp_var.set(f"{weather_data['temperature']}°F")
       self.feels_like_var.set(f"{weather_data['feels_like']}°F")
       self.desc_var.set(weather_data['description'])
       self.humidity_var.set(f"{weather_data['humidity']}%")
       self.updated_var.set(weather_data['time'])
   
   def update_statistics(self):
       """Update statistics display"""
       # Get recent data
       recent_data = self.data_storage.get_recent_data(days=7)
       
       if recent_data:
           # Calculate weekly average
           avg_temp = self.utils.calculate_weekly_average(recent_data)
           if avg_temp:
               self.avg_var.set(f"{avg_temp}°F")
           
           # Find min/max temperatures
           min_temp, max_temp = self.utils.find_min_max_temps(recent_data)
           if min_temp is not None and max_temp is not None:
               self.min_var.set(f"{min_temp}°F")
               self.max_var.set(f"{max_temp}°F")
           
           # Calculate temperature change
           if self.current_weather:
               prev_temp = self.utils.get_previous_temperature(recent_data)
               current_temp = self.current_weather['temperature']
               temp_diff = self.utils.calculate_temperature_difference(current_temp, prev_temp)
               change_text = self.utils.format_temperature_change(temp_diff)
               self.change_var.set(change_text)
   
   def refresh_comparisons(self):
       """Refresh city comparisons"""
       try:
           # Clear existing data
           for item in self.comparison_tree.get_children():
               self.comparison_tree.delete(item)
           
           # Get comparisons if we have current weather data
           if self.current_weather:
               comparisons = self.csv_comparator.compare_with_sacramento(self.current_weather)
               
               for comp in comparisons:
                   # Format display values
                   city_name = comp['city']
                   if comp['state']:
                       city_name += f", {comp['state']}"
                   
                   temp_display = f"{comp['temperature']}°F" if comp['temperature'] is not None else "--"
                   diff_display = comp['temp_comparison'] if comp['temp_comparison'] else "--"
                   humidity_display = f"{comp['humidity']}%" if comp['humidity'] is not None else "--"
                   conditions_display = comp['description'] if comp['description'] else "--"
                   source_display = comp['source_file']
                   
                   # Insert into treeview
                   self.comparison_tree.insert('', 'end', values=(
                       city_name,
                       temp_display,
                       diff_display,
                       humidity_display,
                       conditions_display,
                       source_display
                   ))
               
               if comparisons:
                   self.status_var.set(f"Found {len(comparisons)} cities for comparison")
               else:
                   self.status_var.set("No comparison cities found in CSV files")
           else:
               self.status_var.set("Refresh weather first to enable comparisons")
               
       except Exception as e:
           self.status_var.set(f"Error refreshing comparisons: {str(e)}")
           print(f"Error in refresh_comparisons: {e}")
   
   def toggle_auto_refresh(self):
       """Toggle auto-refresh functionality"""
       if self.auto_refresh_var.get():
           self.start_auto_refresh()
       else:
           self.stop_auto_refresh()
   
   def start_auto_refresh(self):
       """Start auto-refresh timer"""
       self.refresh_weather()
       self.auto_refresh_timer = self.root.after(config.REFRESH_INTERVAL, self.start_auto_refresh)
   
   def stop_auto_refresh(self):
       """Stop auto-refresh timer"""
       if hasattr(self, 'auto_refresh_timer'):
           self.root.after_cancel(self.auto_refresh_timer)
   
   def run(self):
       """Start the GUI application"""
       # Load initial data and update statistics
       self.update_statistics()
       
       # Auto-fetch weather data on startup (after 2 seconds)
       self.root.after(2000, self.refresh_weather)
       
       # Start the GUI event loop
       self.root.mainloop()
