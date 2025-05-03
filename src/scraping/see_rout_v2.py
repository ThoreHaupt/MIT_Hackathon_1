import geopandas as gpd
from geographiclib.geodesic import Geodesic
from shapely.geometry import Point, MultiLineString

# Load Natural Earth ocean data and extract boundaries
water = gpd.read_file('ne_10m_ocean/ne_10m_ocean.shp')
water_boundaries = water.boundary.unary_union  # Convert to MultiLineString


def is_in_water(lon: float, lat: float) -> bool:
    """Check if a point is in water using the Natural Earth dataset."""
    point = Point(lon, lat)
    return water.contains(point).any()


def adjust_to_water(lon: float, lat: float) -> tuple:
    """Move a point to the nearest coastline using boundary geometry."""
    point = Point(lon, lat)

    # Find nearest point on coastline boundaries
    nearest_water = water_boundaries.interpolate(water_boundaries.project(point))
    return (nearest_water.x, nearest_water.y)


def generate_waypoints(start: tuple, end: tuple, interval: int = 5000):
    """Generate waypoints every 5 km along a great circle path."""
    geod = Geodesic.WGS84
    line = geod.InverseLine(*start, *end)
    waypoints = []
    distance = 0

    while distance <= line.s13:
        point = line.Position(distance, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        lon, lat = point['lon2'], point['lat2']

        if not is_in_water(lon, lat):
            lon, lat = adjust_to_water(lon, lat)
        waypoints.append((lat, lon))
        distance += interval

    return waypoints


# Example usage (replace with your coordinates)
start_point = (48.8566, 2.3522)  # Paris
end_point = (40.7128, -74.0060)  # New York

waypoints = generate_waypoints(start_point, end_point)

print("Waypoints (lat, lon):")
for idx, (lat, lon) in enumerate(waypoints):
    print(f"{lon:.6f}, {lat:.6f}")