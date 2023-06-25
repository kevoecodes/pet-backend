from shapely.geometry import Point, Polygon

from pets_management.models import PetGeofenceCoord


def coordinate_outside_boundary(pet, lat, lng):
    # Replace 'YOUR_API_KEY' with your actual Google Maps API key
    # gmaps = googlemaps.Client(key='AIzaSyDQz72mL0bI2Li-VJ2AAyFl78sB4UbQIMk')

    # Define the geosync boundary coordinates as a list of latitude-longitude pairs
    boundary = []
    pet_geofence = PetGeofenceCoord.objects.filter(pet_id=pet.id).order_by('-id')
    print(lat, lng, pet_geofence)
    for i in pet_geofence:
        boundary.append((i.latitudes, i.longitudes))
    print(boundary)
    # Create a polygon object from the boundary coordinates
    boundary_polygon = Polygon(boundary)

    # Create a point object for the given coordinate
    coordinate_point = Point(lat, lng)

    # Check if the coordinate is outside the boundary polygon
    is_outside_boundary = not boundary_polygon.contains(coordinate_point)

    return is_outside_boundary
