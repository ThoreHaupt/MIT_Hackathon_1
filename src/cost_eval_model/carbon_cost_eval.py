from cost_model import CostModel
from cost_eval_model.params import *


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
        # Implement the evaluation logic here
        pass