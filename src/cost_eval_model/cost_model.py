from cost_eval_model.params import *

import pandas as pd
from collections import defaultdict
import numpy as np

class CostModel:
    
    plz_data = pd.read_csv(PLZ_DATA_PATH) # plz;lat;lng;inhab_plz;density;inhab_100
    buckets = defaultdict(list)
    bucket_size = 0.1  # Adjust based on desired granularity (degrees)

    def __init__(self):
        # load the html data
        pass


    @classmethod
    def preprocess_buckets(cls):
        for idx, row in cls.plz_data.iterrows():
            key = cls._get_bucket_key(row['lat'], row['lng'])
            cls.buckets[key].append(idx)

    @staticmethod
    def _get_bucket_key(lat, lng):
        return (int(lat // CostModel.bucket_size), int(lng // CostModel.bucket_size))


    def get_plz_data(lat, long) -> dict:
        """
        Get the data for a given lat long.
        """
        
        # Apply the function to each row in html_data
        data = CostModel.find_closest_plz_data(lat, long)
        return data[['plz', 'lat', 'lng', 'inhab_plz', 'density', 'inhab_100']].to_dict()


    def find_closest_plz_data(lat, lng):
        key = CostModel._get_bucket_key(lat, lng)
        nearby_indices = []

        # Check current bucket and neighboring buckets
        for dlat in [-1, 0, 1]:
            for dlng in [-1, 0, 1]:
                neighbor_key = (key[0] + dlat, key[1] + dlng)
                nearby_indices.extend(CostModel.buckets.get(neighbor_key, []))

        if not nearby_indices:
            return None  # Fallback or error handling

        candidates = CostModel.plz_data.loc[nearby_indices]
        distances = np.sqrt((candidates['lng'] - lng)**2 + (candidates['lat'] - lat)**2)
        closest_index = distances.idxmin()
        return CostModel.plz_data.loc[closest_index]
