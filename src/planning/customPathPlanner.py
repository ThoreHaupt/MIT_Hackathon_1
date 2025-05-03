import heapq
import networkx as nx
from anyio import current_time
from math import radians, cos, sin, sqrt, atan2
from networkx.algorithms.shortest_paths.astar import astar_path
from datetime import datetime


class CustomPathPlanner:
    def __init__(self, G):
        self.G = G

    # Custom edge cost function
    def custom_cost(self, u, v, data, current_time):
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
        u_point = (self.G.nodes[u]['y'], self.G.nodes[u]['x'])
        v_point = (self.G.nodes[v]['y'], self.G.nodes[v]['x'])
        return self.haversine(*u_point, *v_point)


    def calculate_path(self, orig, dest):
        current_time = datetime.now()
        # Priority queue (min-heap) for A* search
        open_list = []
        heapq.heappush(open_list, (0, orig))
        came_from = {}
        g_score = {orig: 0}
        f_score = {orig: self.custom_cost(orig, dest, {}, current_time)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == dest:
                # Reconstruct the path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(orig)
                path.reverse()
                return path

            # For each neighbor of the current node
            for neighbor in self.G.neighbors(current):
                tentative_g_score = g_score[current] + self.custom_cost(current, neighbor, self.G[current][neighbor],
                                                                   current_time)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, dest)

                    if neighbor not in open_list:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None  # No path found
