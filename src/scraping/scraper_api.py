import datetime
import WetterEnum

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
    return ["Berlin", "Karlsruhe", "Hamburg"]

def get_ships():
    return ["Berlin", "Karlsruhe", "Hamburg"]

def ship_available(locationStart, locationTaget):
    return True

def train_available(locationStart, locationTaget):
    return True

def flight_available(locationStart, locationTaget):
    return True

