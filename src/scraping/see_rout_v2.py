import numpy as np
from geographiclib.geodesic import Geodesic
import geopandas as gpd
from shapely.geometry import Point
from collections import deque

# Load higher resolution data (download from Natural Earth)
land = gpd.read_file('ne_10m_land/ne_10m_land.shp')
ocean = gpd.read_file('ne_10m_ocean/ne_10m_ocean.shp')

# Configuration
GRID_RESOLUTION = 0.1  # Degrees (~11 km at equator)
MAX_SEARCH_DISTANCE = 5  # Grid cells to search


def is_in_water(lon, lat):
    point = Point(lon, lat)
    return ocean.geometry.contains(point).any()


def create_maritime_grid(start, end):
    """Create a navigable grid around the route"""
    geod = Geodesic.WGS84
    bearing = geod.Inverse(*start, *end)['azi1']

    # Create grid bounds with buffer
    min_lon = min(start[0], end[0]) - 2
    max_lon = max(start[0], end[0]) + 2
    min_lat = min(start[1], end[1]) - 2
    max_lat = max(start[1], end[1]) + 2

    # Generate grid points
    lons = np.arange(min_lon, max_lon, GRID_RESOLUTION)
    lats = np.arange(min_lat, max_lat, GRID_RESOLUTION)

    grid = {}
    for lon in lons:
        for lat in lats:
            grid[(lon, lat)] = is_in_water(lon, lat)

    return grid


def bfs_maritime_route(start, end, grid):
    """Find path using breadth-first search"""
    geod = Geodesic.WGS84
    queue = deque()
    queue.append(start)
    visited = {start: None}

    while queue:
        current = queue.popleft()

        # Check if we've reached the end
        if geod.Inverse(current[1], current[0], end[1], end[0])['s12'] < 5000:
            return reconstruct_path(current, visited)

        # Explore neighbors
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)

    return None


def get_neighbors(point, grid):
    """Get valid water neighbors within search distance"""
    lon, lat = point
    neighbors = []

    for dlon in [-GRID_RESOLUTION, 0, GRID_RESOLUTION]:
        for dlat in [-GRID_RESOLUTION, 0, GRID_RESOLUTION]:
            if dlon == 0 and dlat == 0:
                continue

            new_lon = lon + dlon
            new_lat = lat + dlat
            if (new_lon, new_lat) in grid and grid[(new_lon, new_lat)]:
                neighbors.append((new_lon, new_lat))

    return neighbors


def reconstruct_path(end, visited):
    """Backtrack from end point to start"""
    path = []
    current = end

    while current:
        path.append(current)
        current = visited[current]

    return path[::-1]


def generate_continuous_route(start, end):
    """Generate complete maritime route"""
    # Find initial water entry
    if not is_in_water(*start):
        water_start = find_water_entry(start, end)
        if not water_start:
            raise ValueError("Start point is landlocked")
    else:
        water_start = start

    # Create navigation grid
    grid = create_maritime_grid(water_start, end)

    # Find path using BFS
    path = bfs_maritime_route(water_start, end, grid)
    if not path:
        raise ValueError("No navigable path found")

    # Convert to (lat, lon) format
    return [(p[1], p[0]) for p in path]


def find_water_entry(start, end, steps=20):
    """Binary search to find water entry point"""
    geod = Geodesic.WGS84
    line = geod.InverseLine(start[1], start[0], end[1], end[0])

    low = 0
    high = line.s13

    for _ in range(steps):
        mid = (low + high) / 2
        point = line.Position(mid, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        if is_in_water(point['lon2'], point['lat2']):
            high = mid
        else:
            low = mid

    final_point = line.Position(high, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
    return (final_point['lon2'], final_point['lat2'])


# Example usage
start_point = (2.3522, 48.8566)  # (lon, lat) Paris
end_point = (-74.0060, 40.7128)  # (lon, lat) New York

try:
    route = generate_continuous_route(start_point, end_point)
    print("Continuous Maritime Route:")
    for idx, (lat, lon) in enumerate(route):
        print(f"{idx + 1}: {lat:.6f}, {lon:.6f}")
except ValueError as e:
    print(f"Routing failed: {str(e)}")