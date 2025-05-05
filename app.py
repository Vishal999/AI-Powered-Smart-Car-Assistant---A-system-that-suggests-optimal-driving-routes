import streamlit as st 
import folium 
import pickle 
import requests 
import polyline 
from datetime import datetime, timedelta 
from streamlit_folium import folium_static 

# Set page configuration and styling
st.set_page_config(
    page_title="AI Smart Car Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better visual consistency
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        padding: 10px;
    }
    .success-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #e8f5e9;
    }
    </style>
    """, unsafe_allow_html=True)

# Error handling decorator
def handle_api_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: Unable to connect to the service. Please check your internet connection.")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred. Please try again.")
            return None
    return wrapper

# Load ML model with error handling
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ Error: ML model file not found. Please ensure model.pkl exists in the project directory.")
    model = None
except Exception as e:
    st.error("❌ Error loading ML model. Please contact support.")
    model = None

# Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyD5ELJ03IEUL98JtLBnSN_IKMOHfxOB9Jw"

@handle_api_errors
def get_lat_lng(place_name):
    # ... existing code ...

@handle_api_errors
def get_directions(start, end):
    # ... existing code ...

# Main UI Layout
st.title("🚗 AI-Powered Smart Car Assistant")
st.markdown("""
    <div class='success-message'>
    Welcome to the Smart Car Assistant! This tool helps you:
    * Find optimal driving routes using AI
    * Get real-time traffic updates
    * View multiple route alternatives
    </div>
    """, unsafe_allow_html=True)

# Create two columns for input fields
col1, col2 = st.columns(2)
with col1:
    start_place = st.text_input("📍 Start Location", "Bengaluru Palace", 
                               help="Enter your starting point")
with col2:
    end_place = st.text_input("📍 Destination", "Chennai Central",
                             help="Enter your destination")

# Center the Find Routes button
_, col2, _ = st.columns([1,2,1])
with col2:
    search_button = st.button("🔍 Find Routes")

if search_button:
    if not model:
        st.error("Cannot proceed: ML model is not loaded properly.")
    else:
        with st.spinner("Finding optimal routes..."):
            start_lat, start_lng = get_lat_lng(start_place)
            end_lat, end_lng = get_lat_lng(end_place)

            if None in (start_lat, start_lng, end_lat, end_lng):
                st.error("❌ Unable to get coordinates. Please check location names and try again.")
            else:
                # Create tabs for different views
                tab1, tab2 = st.tabs(["📊 Predictions", "🗺️ Route Map"])
                
                with tab1:
                    # ... existing prediction code ...
                    distance_km = ((start_lat - end_lat)**2 + (start_lng - end_lng)**2)**0.5 * 111
                    steps = 10
                    predicted_time = model.predict([[distance_km, steps]])[0]
                    total_minutes = int(predicted_time)
                    hours = total_minutes // 60
                    minutes = total_minutes % 60
                    time_str = f"{hours} hr {minutes} min" if hours else f"{minutes} min"
                    
                    st.success(f"📊 AI Model Prediction: **{time_str}**")

                with tab2:
                    routes = get_directions(start_place, end_place)
                    if routes:
                        # ... existing map code ...
                        route_map = folium.Map(location=[(start_lat + end_lat)/2, 
                                                       (start_lng + end_lng)/2], 
                                             zoom_start=7)
                        
                        # Add markers and routes
                        # ... existing code ...
                        
                        st.subheader("🗺️ Interactive Route Map")
                        folium_static(route_map)
                    else:
                        st.warning("⚠️ Could not fetch routes. Please try again later.")
