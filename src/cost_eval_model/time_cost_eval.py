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
        pass