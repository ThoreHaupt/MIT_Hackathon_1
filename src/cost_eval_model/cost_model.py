from cost_eval_model.params import *

import pandas as pd


class CostModel:
    
    plz_data = pd.read_csv(PLZ_DATA_PATH) # plz;lat;lng;inhab_plz;density;inhab_100

    def __init__(self):
        # load the html data
        pass

    def get_plz_data(lat, long):
        """
        Get the data for a given lat long.
        """
        
        # Apply the function to each row in html_data
        data = CostModel.find_closest_plz_data(lat, long)
        return data[['plz', 'lat', 'lng', 'inhab_plz', 'density', 'inhab_100']].to_dict()


    def find_closest_plz_data(lat, long):
        """ 
            df is dataframe with columns 'lat', 'lng', 'plz' where
            'lat' and 'lng' are the coordinates of the plz 
            returns all data of the closest plz
            """
        # Calculate the distance between the row and all rows in df
        distances = ((CostModel.plz_data['lng'] - long)**2 + (CostModel.plz_data['lat'] - lat)**2)**0.5
        # Find the index of the closest row
        closest_index = distances.idxmin()
        # Return the plz of the closest row
        return CostModel.plz_data.iloc[closest_index]