# from cost_eval_model.params import *
from params import *
from cost_model import CostModel

class TimeCostModel(CostModel):
    def __init__(self, time_cost):
        self.time_cost = time_cost

    def evaluate(self, data, construction_manager, transport_time_api):

        """
        Calculate the time per km for each transport type.
        """
        
        # in case of truck,truck and truck is on highway we need to check if there is a construction site
        # current_time = data["time_prior_edge_end"]
        time_cost = 0

        if data['origin']['mode_prior_edge'] == 'truck' and data['destination']['mode_next_edge'] == 'truck' and data['highway'] in ['motorway', 'trunk']:
            construction = construction_manager.get_construction(data['origin']['lat'], data['origin']['lng'])
            if construction:
                time_cost += construction["estimatedTimeLoss"]

            time_cost += data['distance_next_edge'] / data['max_speed_next_edge']

        if data['origin']['mode_prior_edge'] == data['destination']['mode_next_edge']:
            time_cost += data['distance_next_edge'] / data['max_speed_next_edge']
        
        # calculate the time if we have to switch 
        if data['origin']['mode_prior_edge'] != data['destination']['mode_next_edge']:
            # fetch wait time from 
            #next_leave_time = transport_time_api.get_next_departure_time(data['origin']['lat'], data['origin']['lng'], data['destination']['lat'], data['destination']['lng'], data['origin']['mode_prior_edge'], data['destination']['mode_next_edge'])
            #wait_time = next_leave_time - current_time
            if data['origin']['mode_next_edge'] == 'air':
                time_cost = data["time_next_edge_end"] - data["time_prior_edge_end"]
            else:
                wait_time = 3
                time_cost += wait_time

        return time_cost
