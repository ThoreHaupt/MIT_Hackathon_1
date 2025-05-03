from math import radians, cos, sin, sqrt, atan2
from networkx.algorithms.shortest_paths.astar import astar_path

class PathPlanner:
    def __init__(self, G):
        self.graph = G

    # Custom edge cost function
    def custom_cost(self, u, v, data):
        base_cost = data.get("length", 1)
        if data.get("highway") in ["motorway", "trunk"]:
            base_cost *= 2  # Penalize motorways
        if data.get("tunnel"):
            base_cost *= 3  # Strongly penalize tunnels
        return base_cost

    def haversine(self, lat1, lon1, lat2, lon2):
        # distance between (lat1, lon1) and (lat2, lon2)
        R = 6371e3
        phi1, phi2 = radians(lat1), radians(lat2)
        dphi = radians(lat2 - lat1)
        dlambda = radians(lon2 - lon1)
        a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
        return R * 2 * atan2(sqrt(a), sqrt(1 - a))

    # Heuristic using haversine distance
    def heuristic(self, u, v):
        u_point = (self.graph.nodes[u]['x'], self.graph.nodes[u]['y'])
        v_point = (self.graph.nodes[v]['x'], self.graph.nodes[v]['y'])
        return self.haversine(*u_point, *v_point)

    def calculate_path(self, orig, dest):
        return astar_path(self.graph, orig, dest, heuristic=self.heuristic, weight=self.custom_cost)