import streamlit as st
from streamlit.components.v1 import html
import json

def get_current_location():
    # JavaScript to get user's geolocation and send back to Streamlit
    location_js = """
        <script>
        // Function to get location and send to Streamlit
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        // Send the latitude and longitude to Streamlit as JSON
                        const data = {latitude: lat, longitude: lng};
                        const json = JSON.stringify(data);
                        const blob = new Blob([json], { type: 'application/json' });
                        const url = URL.createObjectURL(blob);
                        window.parent.postMessage({data: data}, '*');
                    }
                );
            } else {
                console.log("Geolocation is not supported by this browser.");
            }
        }
        getLocation();
        </script>
    """
    
    # Display the HTML containing the JavaScript
    html(location_js, height=0)
    
    # Read the location from Streamlit's query parameters
    latitude = st.experimental_get_query_params().get("latitude", [None])[0]
    longitude = st.experimental_get_query_params().get("longitude", [None])[0]
    
    # Return coordinates in the form [latitude, longitude] if both are available
    return [float(latitude), float(longitude)]

# Streamlit App Code
st.title("Get Current Location in Streamlit")
location = get_current_location()

if location:
    st.success(f"Location: {location}")
else:
    st.info("Retrieving location, please allow location access in your browser...")
