# from cost_eval_model.params import *
from params import *
from cost_model import CostModel

class TimeCostModel(CostModel):
    def __init__(self, time_cost):
        self.time_cost = time_cost

    def evaluate(self, data):

        """
        Calculate the time per km for each transport type.
        """
        # same mode
        #   cost = dependent on mode
        #           => distance * cost
        #           dist_mode_start_next_edge += dist
        # not same mode (for time => add 2 Stunden)
        # speed?
        edge_time = 0
        dist_in_km = data["distance_next_edge"]
        data["dist_mode_start_next_edge"] += data["time_prior_edge_end"]

        if data["origin"]["mode_prior_edge"] == data["destination"]["mode_next_edge"]:
            if data["origin"]["mode_next_edge"] == 'train':
                edge_time = dist_in_km * 1/max_speed_train
            elif data["origin"]["mode_next_edge"] == 'air':
                edge_time = dist_in_km * 1/max_speed_air
            elif data["origin"]["mode_next_edge"] == 'truck':
                edge_time = dist_in_km * 1/max_speed_truck
            elif data['origin']['mode_next_edge'] == "ship":
                edge_time = dist_in_km * 1/max_speed_ship
        else:
            edge_time = 2

        return edge_time

    """
        edge_data:
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
        "highway": 
                        "motorway" | "trunk" | "primary" | "secondary" | "tertiary"
                                                                    "max_speed_next_edge": 0,
        "distance_next_edge": 0,
        "distance_mode_start_next_edge": 0,
        "time_prior_edge_end": 0,
        }

        """