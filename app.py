import streamlit as st
from location import get_current_location
from directions import get_nearby_services, get_directions
from search import query_duckduckgo, query_llm
from map_utils import create_map
from streamlit_folium import st_folium
import googlemaps

st.title("Ask Emily - AI-Powered Trip Planner From Praveen Barad")

# Prompt user for Google API key if not set
GOOGLE_MAPS_API_KEY = st.text_input("Enter your Google Maps API Key:", key="google_maps_api_key", type="password")
if GOOGLE_MAPS_API_KEY:
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)  # Initialize only after the key is provided
    st.session_state["GOOGLE_MAPS_API_KEY"] = GOOGLE_MAPS_API_KEY

# Initialize session state for location and map
if "location" not in st.session_state:
    initial_location = get_current_location()
    # Check if initial_location is valid, else set to None
    st.session_state["location"] = tuple(initial_location) if initial_location else None

if "map_displayed" not in st.session_state:
    st.session_state["map_displayed"] = False

if "directions_result" not in st.session_state:
    st.session_state["directions_result"] = None

st.write("Welcome! Emily is here to help you with your trip planning needs.")

st.markdown("<span style='background-color: yellow; font-weight: bold'>Note: Change Address in Drop down</span>", unsafe_allow_html=True)

# Dropdown for selecting options
option = st.selectbox("What would you like to do?", ["Find Nearby Services", "Get Directions", "Enter Address Manually"])

# Manual address entry section
if option == "Enter Address Manually":
    manual_address = st.text_input("Enter your address:", key="manual_address_input")
    if manual_address and st.button("Save Address"):
        geocode_result = gmaps.geocode(manual_address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            # Save location as a tuple
            st.session_state["location"] = (location['lat'], location['lng'])
            st.write("Address saved successfully!")
        else:
            st.write("Could not find the specified address. Please try again.")

# Service selection section
elif option == "Find Nearby Services" and GOOGLE_MAPS_API_KEY:
    service_type = st.selectbox("Choose a service", ["restaurant", "fuel station", "hospital", "mechanic", "garage", "shopping_mall"])
    
    if st.session_state["location"]:
        services = get_nearby_services(gmaps, st.session_state["location"], service_type)
        st.write(f"Top 3 {service_type}s near you:")
        
        for service in services[:3]:
            st.write(service['name'])
            if st.button(f"Get directions to {service['name']}", key=f"get_directions_{service['name']}"):
                st.session_state["directions_result"] = get_directions(gmaps, st.session_state["location"], service['geometry']['location'])
                st.session_state["map_displayed"] = True
    else:
        st.write("Could not retrieve your current location.")

# Direction input section
elif option == "Get Directions" and GOOGLE_MAPS_API_KEY:
    destination = st.text_input("Enter your destination:", key="destination_input")
    
    if destination and st.button("Get Directions", key="get_directions_button"):
        st.session_state["directions_result"] = get_directions(gmaps, st.session_state["location"], destination)
        st.session_state["map_displayed"] = True

# Display the map only if directions were successfully fetched
if st.session_state["map_displayed"] and st.session_state["directions_result"]:
    map_display = create_map(st.session_state["location"], st.session_state["directions_result"])
    st_folium(map_display, width=700, height=500)

# Sidebar for General Travel Info
st.sidebar.title("General Travel Info")
st.sidebar.write("You can ask anything related to travel. Type your question below and press 'Get Answer'.")

# General travel info input in the sidebar
question = st.sidebar.text_input("Ask your question:", key="general_query_input")
if st.sidebar.button("Get Answer", key="get_answer_button"):
    if question:
        try:
            answer = query_llm(question)
            st.sidebar.write("Answer: " + answer)
        except Exception as e:
            response = query_duckduckgo(question)
            st.sidebar.write(response)
