from cost_eval_model.params import *


class CostModel:


    def __init__(self):
        # load the html data
        self.plz_data = pd.read_csv(PLZ_DATA_PATH)

    def get_plz_data(self, lat, long):
        """
        Get the data for a given lat long.
        """
        
        # Apply the function to each row in html_data
        plz = self.find_closest_plz(self.plz_data, lat, long)

    def find_closest_plz(df, lat, long):
        """ 
            df is dataframe with columns 'lat', 'lng', 'plz' where
            'lat' and 'lng' are the coordinates of the plz 
            """
        # Calculate the distance between the row and all rows in df
        distances = ((df['lng'] - long)**2 + (df['lat'] - lat)**2)**0.5
        # Find the index of the closest row
        closest_index = distances.idxmin()
        # Return the plz of the closest row
        return df.loc[closest_index, 'plz']