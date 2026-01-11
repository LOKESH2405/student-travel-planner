import folium
from geopy.geocoders import Nominatim
import config

def get_coordinates(location):
    """Get latitude and longitude for a given location"""
    try:
        geolocator = Nominatim(user_agent="student_travel_planner")
        location_data = geolocator.geocode(location)
        
        if location_data:
            return location_data.latitude, location_data.longitude
        else:
            return 0, 0
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return 0, 0


def create_travel_map(destination, itinerary_data=None):
    """Create an interactive map for the travel destination"""
    lat, lon = get_coordinates(destination)
    
    travel_map = folium.Map(
        location=[lat, lon],
        zoom_start=config.DEFAULT_MAP_ZOOM,
        tiles=config.MAP_TILE
    )
    
    folium.Marker(
        [lat, lon],
        popup=f"<b>{destination}</b><br>Your destination!",
        tooltip=destination,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(travel_map)
    
    if itinerary_data and 'days' in itinerary_data:
        colors = ['blue', 'green', 'purple', 'orange', 'darkred']
        
        for idx, day in enumerate(itinerary_data['days']):
            color = colors[idx % len(colors)]
            folium.Circle(
                [lat + (idx * 0.02 - 0.04), lon + (idx * 0.02 - 0.04)],
                radius=500,
                popup=f"<b>Day {day['day']}</b><br>{day['title']}",
                color=color,
                fill=True,
                fillOpacity=0.3
            ).add_to(travel_map)
    
    return travel_map
