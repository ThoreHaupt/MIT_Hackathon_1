from cost_eval_model.params import *
from cost_model import CostModel

class TimeCostModel(CostModel):
    def __init__(self, time_cost):
        self.time_cost = time_cost

    def evaluate(self, data):

        """
        Calculate the time per km for each transport type.
        """
        cost_dict = {
            "train": 1 / self.,
            "ship": 1 / self.,
            "road": 1 / self.,
            "air": 1 / self.
        }

        return cost_dict[transport_type] * distance