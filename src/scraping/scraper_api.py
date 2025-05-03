import datetime
import WetterEnum
from src.scraping.airplane_data.AtlasAirScraper import AtlasAirScraper
from src.scraping.airplane_data.getAirports import getAirportsAsDict
from src.scraping.traffic_data.traffic_issues import traffic_issues


def get_ship_data(locationStart, locationTaget):
    return {
        datetime.datetime.now(): 300,
        datetime.datetime.max : 100
    }

def get_train_data(locationStart, locationTaget):
    return {
        datetime.datetime.now(): 300,
        datetime.datetime.max : 100
    }

def get_air_data(locationStart, locationTaget):
    return {
        datetime.datetime.now(): 300,
        datetime.datetime.max : 100
    }

def get_wetter_data(edge):
    return WetterEnum.WeatherCondition.SUNNY

def unavailabe_edges():
    return [1, 1232, 12322, 23231]

def get_train_stations():
    return ["Berlin", "Karlsruhe", "Hamburg"]

def get_airports():
    return getAirportsAsDict()

def get_ships():
    return ["Berlin", "Karlsruhe", "Hamburg"]

def ship_available(locationStart, locationTaget):
    return True

def train_available(locationStart, locationTaget):
    return True

def flight_available(locationStart, locationTaget):
    return True

def get_traffic_issues():
    return traffic_issues()

def get_construction_data():
    return get_construction_data()

def get_flights():
    return AtlasAirScraper().getData()


