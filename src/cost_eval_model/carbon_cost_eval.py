from .cost_model import CostModel
# from cost_eval_model.params import *
from .params import *


class CarbonCostModel(CostModel):
    """
    This class is used to evaluate the cost of a carbon model.
    """
    def evaluate(self, data, settings: dict):
        """
        Evaluate the cost of the carbon model.
        :param data: The data to evaluate the model on.
        :return: The cost of the model.
        """
        carbon_cost = 0
        
        if data['destination']['mode_next_edge'] == data.get("type", "truck") and not settings.get("use_truck", True):
            carbon_cost = 1000
            return carbon_cost
        if data['origin']['mode_prior_edge'] == data.get("type", "ship") and not settings.get("use_ship", True):
            carbon_cost = 1000
            return carbon_cost
        if data['origin']['mode_prior_edge'] == data.get("type", "train") and not settings.get("use_train", True):
            carbon_cost = 1000
            return carbon_cost
        if data['origin']['mode_prior_edge'] == data.get("type", "plane") and not settings.get("use_plane", True):
            carbon_cost = 1000
            return carbon_cost
        
        dist_in_km = data["distance_next_edge"]
        # data["dist_mode_start_next_edge"] += dist_in_km
        if data["origin"]["mode_prior_edge"] == data["destination"]["mode_next_edge"]:
            if data["destination"]["mode_next_edge"] == 'train':
                carbon_cost = carbon_rail_per_km_per_ton * dist_in_km
            elif data["destination"]["mode_next_edge"] == 'plane':
                carbon_cost = carbon_air_per_km_per_ton * dist_in_km
            elif data["destination"]["mode_next_edge"] == 'truck':
                carbon_cost = carbon_truck_per_km_per_ton * dist_in_km
            elif data['destination']['mode_next_edge'] == "ship":
                carbon_cost = carbon_ship_per_km_per_ton
        else:
            carbon_cost = 0

        return carbon_cost