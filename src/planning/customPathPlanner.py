import heapq
from math import radians, cos, sin, sqrt, atan2
from datetime import datetime
from datetime import timedelta

from cost_eval_model import CostAPI

class CustomPathPlanner:
    def __init__(self, G):
        self.G = G

    # Custom edge cost function
    def custom_cost(self, u, v, path_of_type, previous_edge_data, data, current_time):

        """ 
        u current node
        v next node
        data: edge data (dict)
        previous_edge_data: previous edge data (dict)
        current_time: current time (datetime)

        data input for cost function:
        {
            "origin": { 
                "lat": 0,
                "lng": 0
                "mode_prior_edge": | "train" | "ship" | "truck" | "air"
            },
            "destination": {
                "lat": 0,
                "lng": 0,
                "mode_next_edge": | "train" | "ship" | "truck" | "air"
            },
            "highway": "motorway" | "trunk" | "primary" | "secondary" | "tertiary"
            "max_speed_next_edge": 0, [km/h]
            "distance_next_edge": 0, [km]
            "distance_mode_start_next_edge": 0, [km]
            "time_prior_edge_end": 0, 
        } """
        data["origin"]["lat"] = self.G.nodes[u]['y']
        data["origin"]["lng"] = self.G.nodes[u]['x']
        data["origin"]["mode_prior_edge"] = data.get("type", "Truck")
        data["destination"]["lat"] = self.G.nodes[v]['y']
        data["destination"]["lng"] = self.G.nodes[v]['x']
        data["destination"]["mode_next_edge"] = previous_edge_data[u].get("type", "Truck")
        data["highway"] = data.get("highway", "motorway")
        data["max_speed_next_edge"] = data.get("max_speed", 0)
        data["distance_next_edge"] = data.get("length", 0) / 1000  # Convert to km
        data["distance_mode_start_next_edge"] = path_of_type.get("length", 0) / 1000  # Convert to km
        data["time_prior_edge_end"] = current_time
        data["time_next_edge_end"] = current_time 

        base_cost = data.get("length", 1)
        custom_costs = self.cost_api.get_cost(data)
        return custom_costs.get("cost", base_cost)  # Default to base cost if not found

    def get_travel_time(self, u, v, data, current_time):
        return 1

    def get_all_costs(self,u,v,data,current_time):
        return { "distance": self.haversine(self.G.nodes[u]['x'], self.G.nodes[u]['y'], self.G.nodes[v]['x'], self.G.nodes[v]['y']),  # in m
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
        u_point = (self.G.nodes[u]['x'], self.G.nodes[u]['y'])
        v_point = (self.G.nodes[v]['x'], self.G.nodes[v]['y'])
        return self.haversine(*u_point, *v_point)
        
    def calculate_path(self, orig, dest, settings):
        self.cost_api = CostAPI(settings["freight_weight"], settings["freight_size"])
        self.cost_api.set_price_weight(settings["weight_money"])
        self.cost_api.set_carbon_weight(settings["weight_co2"])
        self.cost_api.set_travel_time_weight(settings["weight_time"])
        self.cost_api.set_risk_weight(settings["weight_risk"])
        
        if orig == dest:
            return []  # Edge case: origin is the same as destination

        current_time = datetime.now()

        # Priority queue (min-heap) for A* search
        open_list = []
        heapq.heappush(open_list, (0, orig))

        open_set = {orig}
        closed_set = set()

        came_from = {orig: None}
        path_of_type = {orig: 0}
        mode_of_transport = {orig: "None"}
        g_score = {orig: 0}
        segCost = {orig: None}
        times = {orig: current_time}
        f_score = {orig: 0}

        while open_list:
            _, current = heapq.heappop(open_list)
            open_set.discard(current)

            if current in closed_set:
                continue
            closed_set.add(current)

            if current == dest:
                # Reconstruct the path
                last = current
                current = came_from[current]
                path = []
                while current in came_from and came_from[current] is not None:
                    segment = {
                        "type": mode_of_transport[last],
                        "path": [
                            [self.G.nodes[current]['y'], self.G.nodes[current]['x']],
                            [self.G.nodes[last]['y'], self.G.nodes[last]['x']]
                        ],
                        "distance": segCost[last].get("distance", 0),
                        "duration": segCost[last].get("duration", 0),
                        "cost": segCost[last].get("cost", 0),
                        "co2_emissions": segCost[last].get("CO2", 0)
                    }
                    path.append(segment)
                    last = current
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.G.neighbors(current):
                edge_data = self.G[current][neighbor]
                travel_time = self.get_travel_time(current, neighbor, edge_data, times[current])
                tentative_g_score = g_score[current] + self.custom_cost(current, neighbor, path_of_type, mode_of_transport, edge_data, times[current])

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    heuristic_cost = self.heuristic(neighbor, dest)
                    f_score[neighbor] = tentative_g_score + heuristic_cost
                    times[neighbor] = times[current] + timedelta(seconds=travel_time)

                    transport_mode = edge_data.get("type", "Truck")
                    mode_of_transport[neighbor] = transport_mode

                    if transport_mode == mode_of_transport[current]:
                        path_of_type[neighbor] = path_of_type[current] + edge_data.get("length", 0)
                    else:
                        path_of_type[neighbor] = 0

                    segCost[neighbor] = self.get_all_costs(current, neighbor, edge_data, times[current])

                    if neighbor not in open_set:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
                        open_set.add(neighbor)

        return None  # No path found