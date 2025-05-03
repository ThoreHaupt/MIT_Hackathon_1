
class TrainStation:
    def __init__(self, name: str, lat: float, lon: float):
        self.name = name
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lon})"

class TrainConnection:
    def __init__(self, start_station: TrainStation, end_station: TrainStation, duration: str, departure_time: str, arrival_time: str):
        self.start_station = start_station
        self.end_station = end_station
        self.duration = duration
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def __str__(self):
        return (f"TrainConnection(start_station={self.start_station}, end_station={self.end_station}, "
                f"duration={self.duration}, departure_time={self.departure_time}, arrival_time={self.arrival_time})")