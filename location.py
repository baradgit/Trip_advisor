import streamlit as st
from streamlit.components.v1 import html

# Function to display location in Streamlit
def get_current_location():
    # Inject JavaScript to get the user's location
    location_js = """
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        // Send data back to Streamlit via hidden input
                        document.getElementById("latitude").value = lat;
                        document.getElementById("longitude").value = lng;
                        document.getElementById("location-form").dispatchEvent(new Event("submit"));
                    },
                    (error) => {
                        console.error("Error getting location:", error);
                    }
                );
            } else {
                console.log("Geolocation is not supported by this browser.");
            }
        }
        getLocation();
        </script>
        <form id="location-form">
            <input type="hidden" id="latitude" name="latitude">
            <input type="hidden" id="longitude" name="longitude">
        </form>
    """

    # Display JavaScript in Streamlit and get location data
    latitude = st.experimental_get_query_params().get("latitude", [None])[0]
    longitude = st.experimental_get_query_params().get("longitude", [None])[0]

    # Display location data if available
    if latitude and longitude:
        st.write(f"Latitude: {latitude}, Longitude: {longitude}")
        return [float(latitude), float(longitude)]
    else:
        html(location_js, height=0)
        return None

# Streamlit app code
st.title("Get Current Location in Streamlit")
location = get_current_location()
if location:
    st.success(f"Location retrieved: {location}")
else:
    st.info("Retrieving location...")
