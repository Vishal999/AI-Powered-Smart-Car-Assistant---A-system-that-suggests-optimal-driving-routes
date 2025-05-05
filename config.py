import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
MODEL_PATH = "model.pkl"

# API URLs
GEOCODING_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
DIRECTIONS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"

# Map styling
MAP_COLORS = ["green", "orange", "purple"]
DEFAULT_ZOOM = 7

# Default locations
DEFAULT_START = "Bengaluru Palace"
DEFAULT_END = "Chennai Central"
