import googlemaps

def get_nearby_services(gmaps, location, service_type="restaurant", radius=5000):
    # Ensure the service type is valid
    valid_service_types = ["restaurant", "fuel station", "hospital", "mechanic", "garage", "shopping_mall"]
    
    if service_type not in valid_service_types:
        raise ValueError(f"Invalid service type: {service_type}. Choose from {valid_service_types}.")

    places = gmaps.places_nearby(location=location, radius=radius, type=service_type)
    return places.get('results', [])

def get_directions(gmaps, start, end):
    directions = gmaps.directions(start, end, mode="driving")
    return directions
