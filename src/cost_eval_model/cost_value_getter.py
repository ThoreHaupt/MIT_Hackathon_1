from cost_eval_model.params import *
from cost_eval_model.risk_cost_eval import RiskCostModel
from cost_eval_model.price_cost_eval import PriceCostModel
from cost_eval_model.carbon_cost_eval import CarbonCostModel
from cost_eval_model.time_cost_eval import TimeCostModel
from cost_eval_model.construction_manager import ConstructionManager


from scraping import ScraperAPI


class CostAPI:
    
    def __init__(self, weight, size):
        # weights for carbon, price, travel time, risk
        self.weight_price = 0.25
        self.carbon_weight = 0.25
        self.travel_time_weight = 0.25
        self.risk_weight = 0.25

        self.weight = weight
        self.size = size

        self.scraper_api = ScraperAPI()

        self.construction_site_data = self.scraper_api.get_construction_site_data() # returns a list of dicts with lat, lng, and other data
        self.construction_manager = ConstructionManager(self.construction_site_data)

        self.risk_model: RiskCostModel = RiskCostModel()
        self.price_model: PriceCostModel = PriceCostModel()
        self.carbon_model: CarbonCostModel = CarbonCostModel()
        self.time_model: TimeCostModel = TimeCostModel() 
    
    def set_price_weight(self, value:int):
        """
        Set the weight for price.
        """
        self.weight_price = value
        return self.weight_price
    
    def set_carbon_weight(self, value:int):
        """
        Set the weight for carbon.
        """
        self.carbon_weight = value
        return self.carbon_weight
    
    def set_travel_time_weight(self, value:int):
        """
        Set the weight for travel time.
        """
        self.travel_time_weight = value
        return self.travel_time_weight
    
    def set_risk_weight(self, value:int):
        """
        Set the weight for risk.
        """
        self.risk_weight = value
        return self.risk_weight
    

    def get_cost(self, edge_data:dict) -> dict:
        """
        Get the cost for a given edge.
            
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
            "highway": "motorway" | "trunk" | "primary" | "secondary" | "tertiary"
            "max_speed_next_edge": 0, [km/h]
            "distance_next_edge": 0,  [km]
            "distance_mode_start_next_edge": 0, [km]
            "time_prior_edge_end": 0, [datetime]
            "time_next_edge_end": 0, [datetime]
        }

        """
        # Extract the data from the edge_data


        
        price_cost = self.price_model.evaluate(edge_data) 
        carbon_cost = self.carbon_model.evaluate(edge_data)
        time_cost = self.time_model.evaluate(edge_data, self.construction_manager)
        risk_cost = self.risk_model.evaluate(edge_data, self.construction_manager)

        # Calculate the cost
        cost = (self.weight_price * price_cost + 
                self.carbon_weight * carbon_cost + 
                self.travel_time_weight * time_cost + 
                self.risk_weight * risk_cost)

        return_dict = {
            "price_cost": price_cost,
            "carbon_cost": carbon_cost,
            "time_cost": time_cost,
            "risk_cost": risk_cost,
            "total_cost": cost
        }

        return return_dict
