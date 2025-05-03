import datetime
import math
from cost_eval_model.params import *
from cost_eval_model.cost_model import CostModel
from cost_eval_model.construction_manager import ConstructionManager

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf


class RiskCostModel(CostModel):
    """
    This class is used to evaluate the risk cost of a given model.
    """

    def __init__(self):
        """
        Initialize the RiskCostModel with a given model.

        :param model: The model to be evaluated.
        """
        self.keras_utilitization_model = tf.keras.load_model(KERAS_MODEL_PATH)
        self.scaler = StandardScaler()
        

    def evaluate(self, data, construction_manager: ConstructionManager):
        """
        Evaluate the risk cost of the model on the given data.

        :param data: The data to be evaluated.
        :return: The risk cost of the model on the given data.

        data:
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
            "max_speed_next_edge": 0, 
            "distance_next_edge": 0, [km]
            "distance_mode_start_next_edge": 0, [km]
            "time_prior_edge_end": 0, 
        }

        """

        risk_score = 0
        # Placeholder for actual evaluation logic

         # in case of truck,truck and truck is on highway we need to check if there is a construction site
        if data['origin']['mode_prior_edge'] == 'truck' and data['destination']['mode_next_edge'] == 'truck' and data['highway'] in ['motorway', 'trunk']:
            construction = construction_manager.get_construction(data['origin']['lat'], data['origin']['lng'])
            if construction:
                risk_score += 1  # Placeholder for actual risk score calculation
        
            # Example of using the keras model for risk score calculation
            # input vector: ['Land', 'Strnum', 'Wotag', 'Stunde', 'Monat','inhab_plz', 'density', 'inhab_100']
            time_end: datetime.datetime = data['time_prior_edge_end']
            wochentag = datetime.strftime("%A")
            stunde = datetime.strftime("%H")
            monat = datetime.strftime("%m")

            dat = super().get_plz_data(data['origin']['lat'], data['origin']['lng'])
            inhab_plz = dat['inhab_plz']
            density = dat['density']
            inhab_100 = dat['inhab_100']

            straßennummer = 1  # Placeholder for actual street number calculation

            # input_data = np.array([[1, 8, 2, 8, 5, 12345, 0.5, 500000]])  # Example input
            input_data = np.array([[wochentag, straßennummer, stunde, monat, inhab_plz, density, inhab_100]])

            # predict
            input_data_scaled = self.scaler.transform(input_data)
            predicted_volume = self.keras_utilitization_model.predict(input_data_scaled)

            MAX_NO_TRAFFIC_VOLUME = 1500
            if predicted_volume > MAX_NO_TRAFFIC_VOLUME:
                risk_score += math.exp(predicted_volume - MAX_NO_TRAFFIC_VOLUME)
            
        # score for construction site risk

        return risk_score
