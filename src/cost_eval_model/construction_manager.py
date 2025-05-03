

class ConstructionManager:
    def __init__(self, construction_dict_array:list):
        self.calculate_construction_buckets([obj.to_dict() for obj in construction_dict_array])


    def bucket_hash(self, lat:float, lng:float) -> str:
        """
        Create a hash for the given lat and lng.
        """
        # Round the lat and lng to 1 decimal places ~10m
        lat = round(lat, 1)
        lng = round(lng, 1)
        return lat, lng
        
    def get_construction(self, lat:float, lng:float) -> dict | None:
        """
        Get the construction site data. if closer than 
        """
        # get bucket
        bucket = self.bucket_hash(lat, lng)
        # check if bucket exists
        if bucket in self.construction_dict:
            # check if construction site is closer than 4km lat distance is 0.04 and lng distance is 0.04
            for construction in self.construction_dict[bucket]:
                if abs(construction.to_dict()['latitude'] - lat) < 0.03 and abs(construction.to_dict()['longitude'] - lng) < 0.03:
                    return construction
        return None
        

    def calculate_construction_buckets(self, construction_dict_array:list):
        """
        Calculate the construction buckets for the given construction data.
        """
        self.construction_dict = {}
        for construction in construction_dict_array:
            lat = construction['latitude']
            lng = construction['longitude']
            bucket = self.bucket_hash(lat, lng)
            if bucket not in self.construction_dict:
                self.construction_dict[bucket] = []
            self.construction_dict[bucket].append(construction)

    
