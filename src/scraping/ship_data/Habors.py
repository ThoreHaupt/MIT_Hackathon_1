
class Habor:
    def __init__(self, id: int, name: str, latitude: float, longitude: float) -> None:
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Habor(id={self.id}, name={self.name}, latitude={self.latitude}, longitude={self.longitude})"

