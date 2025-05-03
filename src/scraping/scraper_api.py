import datetime
from scraping.WetterEnum import WeatherCondition
from scraping.airplane_data.AtlasAirScraper import AtlasAirScraper
from scraping.airplane_data.getAirports import getAirportsAsDict
from scraping.traffic_data.traffic_issues import traffic_issues

import scraping.train_data.scarpeTrainStations as ts
import scraping.train_data.scrapeTrainData as train_data

from src.scraping.wetter_data import wetter_scraper


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

def get_wetter_data(location_lat, location_lon):
    return wetter_scraper.get_wetter_data(round(location_lat, 1), round(location_lon, 1))


def unavailabe_edges():
    return [1, 1232, 12322, 23231]

def get_train_stations():
    return ts.get_all_train_stations()

def get_airports():
    return getAirportsAsDict()

def get_ships():
    return ["Berlin", "Karlsruhe", "Hamburg"]

def ship_available(locationStart, locationTaget):
    return True

def train_available(locationStart, time = datetime.datetime.now()):
    return train_data.get_connections(locationStart, time)

def flight_available(locationStart, locationTaget):
    return True

def get_traffic_issues():
    return traffic_issues()

def get_construction_data():
    return get_construction_data()

def get_flights():
    return AtlasAirScraper().getData()

def get_all_train_stations():
    return get_train_stations()

