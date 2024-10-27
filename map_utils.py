import folium
from folium import PolyLine
import polyline
 # You may need to install this package if you don't have it: pip install polyline

def create_map(location, directions):
    # Create a Folium map centered on the starting location
    m = folium.Map(location=location, zoom_start=13)

    # Check if directions are available
    if directions and 'legs' in directions[0]:
        route = directions[0]['legs'][0]
        
        # Get the starting location
        start_location = route['start_location']
        folium.Marker(
            location=[start_location['lat'], start_location['lng']],
            popup="Start",
            icon=folium.Icon(color="green")
        ).add_to(m)

        full_path = []  # Initialize a list to store the path coordinates

        for step in route['steps']:
            # Decode the polyline points
            polyline_points = polyline.decode(step['polyline']['points'])
            # Add each point to the full_path
            full_path.extend([(point[0], point[1]) for point in polyline_points])

            # Optionally, add markers or popups for each step
            instruction = step['html_instructions']  # Use html_instructions for step info

        # Draw the blue line on the map
        PolyLine(locations=full_path, color="blue", weight=5, opacity=0.7).add_to(m)

    return m
