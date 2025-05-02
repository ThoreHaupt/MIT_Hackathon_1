
class CostEvaluator:
    
    def __init__(self):
        # weights for carbon, price, travel time, risk
        self.weight_price = 0.25
        
        self.carbon_weight = 0.25
        self.travel_time_weight = 0.25
        self.risk_weight = 0.25

        self.max_speed_traffic_jam = 25 # km/h
        self.max_speed_highway = 80 # km/h
        self.max_speed_train = 80 # km/h
        self.max_speed_ship = 20 # km/h
        self.max_speed_air = 800 # km/h


        self.scraper_api = None

    def time_cost(self, distance:float, transport_type:str, weather:str, max_speed:float):
        """
        Calculate the time per km for each transport type.
        """
        cost_dict = {
            "train": 1 / self.max_speed_train,
            "ship": 1 / self.max_speed_ship,
            "road": 1 / self.max_speed_highway,
            "air": 1 / self.max_speed_air
        }

        return cost_dict[transport_type] * distance
    
    def carbon_cost(self, distance:float, transport_type:str, weather:str):
        """
        Calculate the carbon per km for each transport type.
        """
        cost_dict = {
            "train": 0.1,
            "ship": 0.05,
            "road": 0.2,
            "air": 0.3
        }

        return cost_dict[transport_type] * distance
    
    def price_cost(self, distance:float, transport_type:str, weather:str):
        """
        Calculate the price per km for each transport type.
        """
        cost_dict = {
            "train": 0.1,
            "ship": 0.05,
            "road": 0.2,
            "air": 0.3
        }

        return cost_dict[transport_type] * distance
    
    def risk_cost(self, distance:float, transport_type:str, weather:str):
        """
        Calculate the failiure risk of an edge for each transport type.
        """
        cost_dict = {
            "train": 0.1,
            "ship": 0.05,
            "road": 0.2,
            "air": 0.3
        }

        return cost_dict[transport_type] * distance


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
    
    def get_cost(self, edge_data:dict[str, float], ):
        """
        Get the cost for a given edge.
            
        "type": ["train", "ship", "road", "air"]

        """
        # Extract the data from the edge_data
        
        # Calculate the cost
        cost = (self.weight_price * self.price_cost(edge_data) +
                self.carbon_weight * self.carbon_cost(edge_data) +
                self.travel_time_weight * self.time_cost(edge_data) +
                self.risk_weight * self.risk_cost(edge_data))
        
        return cost
