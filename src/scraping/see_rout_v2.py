import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, box
from geopy.distance import geodesic
import math
import numpy as np
from itertools import product

# Load land polygon dataset (Natural Earth's coastline) - load once globally
LAND = gpd.read_file("ne_10m_land/ne_10m_land.shp")


def is_water(lat, lon, grid_size=0.05, num_samples=9, threshold=0.5):
    """
    Optimized water detection using spatial indexing and vectorized operations.

    Parameters:
    - lat, lon: Point coordinates
    - grid_size: Distance between sampling points (in degrees)
    - num_samples: Number of surrounding points to test
    - threshold: Minimum percentage of water required to consider it water
    """
    # Generate sample points in a single operation
    offsets = np.linspace(-grid_size, grid_size, int(math.sqrt(num_samples)))
    lats = lat + offsets
    lons = lon + offsets

    # Create all combinations of lat/lon
    points = [Point(lon, lat) for lat, lon in product(lats, lons)]

    # Vectorized check using spatial index
    results = ~LAND.geometry.unary_union.intersects(Point(lon, lat))

    # If center point is water, assume it's water (faster for open ocean)
    if results:
        return True

    # Otherwise do the full check
    water_count = sum(1 for pt in points if not LAND.geometry.unary_union.intersects(pt))
    return (water_count / len(points)) >= threshold


def find_nearest_water(lat, lon, search_radius=10):
    """
    Optimized nearest water search using spiral pattern and early termination.
    """
    step_size = 0.05  # degrees
    max_steps = int(search_radius / (geodesic((lat, lon), (lat + step_size, lon)).km))

    # Spiral search pattern
    for step in range(1, max_steps + 1):
        for angle in np.linspace(0, 2 * math.pi, 12 * step, endpoint=False):
            new_lat = lat + step * step_size * math.cos(angle)
            new_lon = lon + step * step_size * math.sin(angle)
            if is_water(new_lat, new_lon):
                return (new_lat, new_lon)

    return (lat, lon)


def generate_grid(start, end, step=0.1):
    """
    Optimized grid generation with spatial indexing and smarter connectivity.
    """
    G = nx.Graph()
    min_lat, max_lat = sorted([start[0], end[0]])
    min_lon, max_lon = sorted([start[1], end[1]])

    # Create bounding box to limit our search area
    bbox = box(min_lon - step, min_lat - step, max_lon + step, max_lat + step)

    # Pre-filter land polygons that intersect our area of interest
    relevant_land = LAND[LAND.intersects(bbox)]

    # Generate all candidate points
    lat_range = np.arange(min_lat, max_lat + step, step)
    lon_range = np.arange(min_lon, max_lon + step, step)

    # Add water nodes
    water_nodes = []
    for lat, lon in product(lat_range, lon_range):
        if not relevant_land.geometry.unary_union.intersects(Point(lon, lat)):
            G.add_node((lat, lon))
            water_nodes.append((lat, lon))

    # Connect nodes more efficiently
    for i, (lat, lon) in enumerate(water_nodes):
        # Only check forward to avoid duplicate edges
        for other_lat, other_lon in water_nodes[i + 1:i + 100]:  # Limit search window
            if abs(lat - other_lat) <= step and abs(lon - other_lon) <= step:
                dist = geodesic((lat, lon), (other_lat, other_lon)).meters
                G.add_edge((lat, lon), (other_lat, other_lon), weight=dist)

    return G

def getRouteHamburgBoston():
    return [(53.537106, 9.904600), (53.542296, 9.894299), (53.557647, 9.778191), (53.573549, 9.644773), (53.606490, 9.580087), (53.625598, 9.540809), (53.714932, 9.480116), (53.754404, 9.407250), (53.860787, 9.302734), (53.881083, 9.059012), (53.910936, 8.782155), (54.537275, 7.785740), (53.819088, 3.769683), (51.352738, 1.983865), (50.158297, -0.950792), (48.693560, -8.924414), (41.586859, -47.659306), (41.958047, -67.688296), (42.412966, -70.245956), (42.383541, -70.832197), (42.380052, -70.902690), (42.336982, -70.950215), (42.340784, -70.997795), (42.344107, -71.013300), (42.342809, -71.021043)]


def find_best_shipping_route(start, end):
    """
    Optimized route finding with caching and early checks.
    """
    # Adjust start and end points if on land
    start = find_nearest_water(*start)
    end = find_nearest_water(*end)

    # Early check if start and end are the same
    if start == end:
        return [start]

    G = generate_grid(start, end)

    if start not in G.nodes or end not in G.nodes:
        raise ValueError("Could not find enough water nodes nearby.")

    try:
        path = nx.shortest_path(G, source=start, target=end, weight='weight')
        return path
    except nx.NetworkXNoPath:
        # Try with a coarser grid if no path found
        G = generate_grid(start, end, step=0.2)
        return nx.shortest_path(G, source=start, target=end, weight='weight')


# Example usage
if __name__ == "__main__":
    start_point = (53.5461, 9.9937)  # Hamburg, Germany
    end_point = (34.0522, -118.2437)  # Los Angeles, USA

    route = find_best_shipping_route(start_point, end_point)

    print("Optimized Shipping Route Waypoints:")
    for i, (lat, lon) in enumerate(route, start=1):
        print(f"{lon:.6f}, {lat:.6f}")