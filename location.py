import geocoder

def get_current_location():
    g = geocoder.ip('me')
    print(g.latlng)
    return g.latlng if g.ok else None
