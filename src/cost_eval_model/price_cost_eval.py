# from cost_eval_model.cost_model import CostModel
# from cost_eval_model.params import *
from .cost_model import CostModel
from .params import *

class PriceCostModel(CostModel):
    """
    This class is used to evaluate the cost of a price model.
    """

    def __init__(self, price_model):
        self.price_model = price_model

    def evaluate(self, data, settings: dict):
        """
        Evaluate the cost of the price model.
        :param data: The data to evaluate the model on.
        :return: The cost of the model.
        """
        edge_cost = 0

        if data['destination']['mode_next_edge'] == data.get("type", "Truck") and not settings.get("use_truck", True):
            edge_cost = 1000
            return edge_cost
        if data['origin']['mode_prior_edge'] == data.get("type", "Ship") and not settings.get("use_ship", True):
            edge_cost = 1000
            return edge_cost
        if data['origin']['mode_prior_edge'] == data.get("type", "Train") and not settings.get("use_train", True):
            edge_cost = 1000
            return edge_cost
        if data['origin']['mode_prior_edge'] == data.get("type", "Air") and not settings.get("use_plane", True):
            edge_cost = 1000
            return edge_cost
        
        dist_in_km = data["distance_next_edge"]
        # data["dist_mode_start_next_edge"] += dist_in_km
        if data["origin"]["mode_prior_edge"] == data["destination"]["mode_next_edge"]:
            if data["origin"]["mode_next_edge"] == 'train':
                edge_cost = us_price_rail_per_km_per_ton*dist_in_km
            elif data["origin"]["mode_next_edge"] == 'air':
                edge_cost = price_air_per_km_per_ton*dist_in_km
            elif data["origin"]["mode_next_edge"] == 'truck':
                edge_cost = us_price_truck_per_km_per_ton*dist_in_km
            elif data['origin']['mode_next_edge'] == "ship":
                edge_cost = price_ship_per_km_per_ton
        else:
            edge_cost = 2

        return edge_cost
