from cost_model import CostModel
# from cost_eval_model.params import *
from params import *


class CarbonCostModel(CostModel):
    """
    This class is used to evaluate the cost of a carbon model.
    """

    def __init__(self, carbon_model):
        self.carbon_model = carbon_model

    def evaluate(self, data):
        """
        Evaluate the cost of the carbon model.
        :param data: The data to evaluate the model on.
        :return: The cost of the model.
        """
        carbon_cost = 0
        dist_in_km = data["distance_next_edge"]
        data["dist_mode_start_next_edge"] += dist_in_km # brauche ich das ueberhaupt
        if data["origin"]["mode_prior_edge"] == data["destination"]["mode_next_edge"]:
            if data["origin"]["mode_next_edge"] == 'train':
                carbon_cost = carbon_rail_per_km_per_ton * dist_in_km
            elif data["origin"]["mode_next_edge"] == 'air':
                carbon_cost = carbon_air_per_km_per_ton * dist_in_km
            elif data["origin"]["mode_next_edge"] == 'truck':
                carbon_cost = carbon_truck_per_km_per_ton * dist_in_km
            elif data['origin']['mode_next_edge'] == "ship":
                carbon_cost = carbon_ship_per_km_per_ton
        else:
            carbon_cost = 0

        return carbon_cost