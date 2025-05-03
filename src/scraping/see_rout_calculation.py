import requests
from geographiclib.geodesic import Geodesic

# from src.scraping import get_ships


from geopy.distance import geodesic
import numpy as np
import osmnx as ox
import networkx as nx
from global_land_mask import globe


def adjust_to_water(lon: float, lat: float, max_steps: int = 10, step_km: float = 1) -> tuple:
    """
    Adjusted version with coordinate validation and boundary handling.
    """
    geod = Geodesic.WGS84
    directions = [0, 90, 180, 270]  # North, East, South, West

    # Validate initial coordinates
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        print(f"Invalid coordinates: ({lon}, {lat})")
        return (lon, lat)  # Return invalid point as fallback

    for steps in range(1, max_steps + 1):
        for direction in directions:
            distance = steps * step_km * 1000
            p = geod.Direct(lat, lon, direction, distance)

            # Get new coordinates with boundary checks
            new_lat = np.clip(p['lat2'], -89.9999, 89.9999)
            new_lon = p['lon2'] % 360  # Normalize longitude
            if new_lon > 180:
                new_lon -= 360

            # Skip invalid coordinates
            if not (-90 <= new_lat <= 90) or not (-180 <= new_lon <= 180):
                continue

            try:
                if not globe.is_land(new_lat, new_lon):
                    return (new_lon, new_lat)
            except IndexError:
                continue  # Skip invalid grid positions

    return (lon, lat)  # Fallback to original point


def get_hybrid_route(start_long: float, start_lat: float,
                     end_long: float, end_lat: float,
                     coastal_threshold_km: float = 50,
                     ocean_point_spacing_km: float = 500) -> list:
    """
    Get intermediate waypoints for a shipping route, ensuring all points are in water.
    """
    start = (start_lat, start_long)
    end = (end_lat, end_long)
    total_distance = geodesic(start, end).kilometers

    if total_distance > coastal_threshold_km:
        waypoints = get_ocean_waypoints(start_long, start_lat, end_long, end_lat, ocean_point_spacing_km)
    else:
        waypoints = get_coastal_waypoints(start_long, start_lat, end_long, end_lat)

    # Adjust all waypoints to ensure they're in water
    adjusted_waypoints = []
    for point in waypoints:
        lon, lat = point
        if globe.is_land(lat, lon):
            adjusted = adjust_to_water(lon, lat)
            adjusted_waypoints.append(adjusted)
        else:
            adjusted_waypoints.append(point)

    return adjusted_waypoints


# def get_ocean_waypoints(start_long: float, start_lat: float,
#                         end_long: float, end_lat: float,
#                         point_spacing_km: float) -> list:
#     """
#     Get waypoints along a great circle route (ocean navigation).
#     """
#     start = (start_lat, start_long)
#     end = (end_lat, end_long)
#
#     total_distance = geodesic(start, end).kilometers
#     num_points = max(2, int(total_distance / point_spacing_km))
#
#     waypoints = []
#     total_distance = geodesic((start_lat, start_long),
#                               (end_lat, end_long)).kilometers
#     bearing = geodesic((start_lat, start_long),
#                        (end_lat, end_long)).azimuth
#
#     for i in np.linspace(0, 1, num_points):
#         point = geodesic(kilometers=i * total_distance).destination(
#             point=(start_lat, start_long),
#             bearing=bearing
#         )
#         waypoints.append((point.longitude, point.latitude)) # Return as (long, lat)
#
#     return waypoints


def get_ocean_waypoints(start_long, start_lat, end_long, end_lat, spacing_km=100):
    # ===== 1. INPUT VALIDATION =====
    if not all(isinstance(coord, (int, float)) for coord in [start_lat, start_long, end_lat, end_long]):
        raise ValueError("Coordinates must be numbers (float/int).")

    if abs(start_lat) > 90 or abs(end_lat) > 90:
        raise ValueError("Latitude must be between -90 and 90.")

    if abs(start_long) > 180 or abs(end_long) > 180:
        raise ValueError("Longitude must be between -180 and 180.")

    # ===== 2. HANDLE IDENTICAL POINTS =====
    if (start_lat == end_lat) and (start_long == end_long):
        return [(start_long, start_lat)]  # Single point

    # ===== 3. COMPUTE DISTANCE & BEARING =====
    geod = Geodesic.WGS84
    g = geod.Inverse(start_lat, start_long, end_lat, end_long)

    if not isinstance(g['s12'], (int, float)):
        raise ValueError(f"Failed to compute distance. Geodesic result: {g}")

    total_distance_km = g['s12'] / 1000  # Convert meters → km
    initial_bearing = g['azi1']

    # ===== 4. GENERATE WAYPOINTS =====
    num_points = max(2, int(total_distance_km / spacing_km) + 1)  # At least 2 points
    waypoints = []

    for i in np.linspace(0, 1, num_points):
        p = geod.Direct(
            start_lat, start_long,
            initial_bearing,
            i * total_distance_km * 1000  # Distance in meters
        )
        waypoints.append((p['lon2'], p['lat2']))

    return waypoints

def get_coastal_waypoints(start_long: float, start_lat: float,
                          end_long: float, end_lat: float,
                          bbox_buffer: float = 0.5) -> list:
    """
    Get waypoints following OSM waterways (coastal/inland navigation).
    """
    # Create bounding box
    north = max(start_lat, end_lat) + bbox_buffer
    south = min(start_lat, end_lat) - bbox_buffer
    east = max(start_long, end_long) + bbox_buffer
    west = min(start_long, end_long) - bbox_buffer

    try:
        # Get waterway network
        G = ox.graph_from_bbox(
            north, south, east, west,
            custom_filter='["waterway"~"river|canal|fairway|dock|ferry"]',
            retain_all=True,
            simplify=True
        )

        if len(G.nodes) == 0:
            raise ValueError("No waterways found in area")

        # Find nearest nodes
        start_node = ox.distance.nearest_nodes(G, start_long, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_long, end_lat)

        # Get shortest path
        route = nx.shortest_path(G, start_node, end_node, weight='length')

        # Extract waypoints (long, lat order)
        waypoints = [
            (G.nodes[node]['x'], G.nodes[node]['y'])  # OSMnx stores lon as x, lat as y
            for node in route
        ]

        return waypoints

    except Exception as e:
        print(f"Waterway routing failed: {str(e)}")
        # Fall back to straight line if waterway routing fails
        return [(start_long, start_lat), (end_long, end_lat)]



# Example usage
p1 = (8.889906, 44.404263)
p2 = (-118.199826, 33.762325)
waypoints = get_hybrid_route(p1[0], p1[1], p2[0], p2[1], coastal_threshold_km=10, ocean_point_spacing_km=10)
print("Route waypoints (longitude, latitude):")
waypoints.append(p1)
waypoints.append(p2)

for i, (lon, lat) in enumerate(waypoints):
    print(f"{lon:.6f}, {lat:.6f}")


