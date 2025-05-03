from datetime import datetime

import requests
import xml.etree.ElementTree as ET

from scraping.train_data.TrainClasses import TrainStation, TrainConnection
from scraping.train_data.scarpeTrainStations import get_all_train_stations

from fuzzywuzzy import fuzz

# A dictionary of common abbreviations and their full forms
abbreviation_map = {
    "hbf": "hauptbahnhof",
    "hbf.": "hauptbahnhof",
    "stn": "station",
    "bahnhof": "station",
    # Add other abbreviations as needed
}

# Function to normalize abbreviations in a string
def normalize_abbreviations(text):
    text = text.lower()  # Make lowercase to ensure case-insensitivity
    for abbr, full_form in abbreviation_map.items():
        text = text.replace(abbr, full_form)  # Replace abbreviation with full form
    return text

# Function to find a train station by name with fuzzy comparison
def find_train_station_by_name_sim(target_name, threshold=80):
    if target_name is None:
        return None

    # Normalize the target name
    target_name = normalize_abbreviations(target_name.strip())

    best_match = None
    best_score = 0

    # Iterate through all stations and compare their names
    for station in get_all_train_stations():
        station_name = normalize_abbreviations(station.name.strip())

        # Calculate the similarity score between the normalized station name and the target name
        score = fuzz.ratio(station_name, target_name)

        # If the score is above the threshold, consider it a match
        if score > best_score and score >= threshold:
            best_score = score
            best_match = station

    print(f"Best match for '{target_name}' is '{best_match.name}' with score {best_score}") if best_match else print(f"No match found for '{target_name}'")
    return best_match

def get_eva_by_name(xml_text, station_name):
    root = ET.fromstring(xml_text)
    for station in root.findall('station'):
        if station.attrib.get('name').lower() == station_name.lower():
            return station.attrib['eva']
    return None

def get_eva_id(start):
    url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/" + start

    headers = {
        "DB-Client-ID": "d3dc669d4c3aa1ab24d627ed228d740c",
        "DB-Api-Key": "a688710f9210a460f36f246ffd2e140d",
        "accept": "application/vnd.de.db.ris+json"
    }
    response = requests.get(url, headers=headers)
    #print(response.text)
    return get_eva_by_name(response.text, start)

def parse_train_connections(xml_data: str, target_station: str):
    root = ET.fromstring(xml_data)
    connections = []

    # print(xml_data)

    for s in root.findall('s'):
        dp = s.find('dp')

        if dp is None:
            continue

        pde = dp.get('pde')
        dp_ppth = dp.get('ppth', '')

        dp_stations = dp_ppth.split('|') if dp_ppth else []
        dp_stations += [pde]

        connections.append((dp_stations, datetime.strptime(dp.get("pt"), '%y%m%d%H%M')))

    return connections

def get_connection(eva_number, target, dt):
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/{eva_number}/{dt.strftime('%y%m%d')}/{dt.strftime('%H')}"

    headers = {
        "DB-Client-ID": "d3dc669d4c3aa1ab24d627ed228d740c",
        "DB-Api-Key": "a688710f9210a460f36f246ffd2e140d",
        "accept": "application/vnd.de.db.ris+json"
    }

    response = requests.get(url, headers=headers)
    return parse_train_connections(response.text, target)

def find_train_station_by_name(target_name):
    if target_name is None:
        return

    for station in get_all_train_stations():
        if station.name.lower() == target_name.lower():  # Case-insensitive comparison
            return station
    return None

def parse_to_connections(start, connections):
    start_station = find_train_station_by_name_sim(start)
    ret = []
    for stops, time in connections:
        for stop in stops:
            end_station = find_train_station_by_name_sim(stop)
            ret.append(TrainConnection(start_station, end_station, "00:00", time.strftime('%H:%M'), time.strftime('%H:%M')))

    return ret


def get_connections(start, target, time=datetime.now()):
    return parse_to_connections(start, get_connection(get_eva_id(start), target, time))

# print(get_connections("Karlsruhe HBF", "Konstanz", datetime.now())[0])