import heapq
from math import radians, cos, sin, sqrt, atan2
from datetime import datetime
from datetime import timedelta


class CustomPathPlanner:
    def __init__(self, G):
        self.G = G

    # Custom edge cost function
    def custom_cost(self, u, v, data, current_time):
        base_cost = data.get("length", 1)
        return base_cost

    def get_travel_time(self, u, v, data, current_time):
        return 1

    def get_all_costs(self,u,v,data,current_time):
        return { "distance": self.haversine(self.G.nodes[u]['y'], self.G.nodes[u]['x'], self.G.nodes[v]['y'], self.G.nodes[v]['x']),  # in m
        "duration": 0,  # in s
        "cost": 0,  # in s
        "CO2": 0,  # in CO₂e
        }

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
        came_from = {orig:None}
        path_of_type = {orig: 0}
        mode_of_transport = {orig: "None"}
        g_score = {orig: 0}
        segCost = {orig: None}
        times = {orig: current_time}
        f_score = {orig: self.custom_cost(orig, dest, {}, current_time)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == dest:

                # Reconstruct the path
                last = current
                current = came_from[current]
                path = []
                while current in came_from:

                    segment = { "type": mode_of_transport[last], # in {"Truck", "Train", "Ship", "Plane"}
                                "path": [[self.G.nodes[current]['y'], self.G.nodes[current]['x']], [self.G.nodes[last]['y'], self.G.nodes[last]['x']]], # Coordinates of start and destination
                                "distance": segCost[last]["distance"], # in m
                                "duration": segCost[last]["duration"], # in s
                                "cost": segCost[last]["cost"], # in s
                                "co2_emissions": segCost[last]["CO2"], # in CO₂e
  }
                    path.append(segment)
                    current = came_from[current]
                path.reverse()
                return path

            # For each neighbor of the current node
            for neighbor in self.G.neighbors(current):
                tentative_g_score = g_score[current] + self.custom_cost(current, neighbor, self.G[current][neighbor],
                                                                   times[current])
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:

                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, dest)
                    times[neighbor] = current_time + timedelta(seconds=self.get_travel_time(current, neighbor, self.G[current][neighbor],
                                                                   times[current]))
                    # detect mode of transport
                    mode_of_transport[neighbor] = self.G[current][neighbor].get("type", "Truck")
                    if mode_of_transport[neighbor] == mode_of_transport[current]:
                        path_of_type[neighbor] = path_of_type[current] + self.G[current][neighbor].get("length", 0)
                    else:
                        path_of_type[neighbor] = 0

                    segCost[neighbor] = self.get_all_costs(current, neighbor, self.G[current][neighbor], times[current])


                    if neighbor not in open_list:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None  # No path found
