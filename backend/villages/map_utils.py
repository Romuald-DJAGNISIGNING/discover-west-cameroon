"""
Utility for generating map API links for villages (OpenStreetMap, Google Maps, etc.)
"""
def openstreetmap_link(lat, lon, zoom=14):
    return f"https://www.openstreetmap.org/#map={zoom}/{lat}/{lon}"

def googlemaps_link(lat, lon):
    return f"https://maps.google.com/?q={lat},{lon}"