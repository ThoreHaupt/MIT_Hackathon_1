import datetime
import re

import requests

from scraping.traffic_data.TrafficIssue import TrafficIssue

baseURL = "https://verkehr.autobahn.de/o/autobahn/"

def fetch_german_streets():
    url = f"{baseURL}"
    response = requests.get(url, headers={"accept": "application/json"})
    if response.status_code == 200:
        data = response.json().get("roads", [])
        street_ids = [street for street in data]
        return street_ids
    else:
        print(f"Error: Unable to fetch data, status code {response.status_code}")
        return []

def parse_end_time(description):
    pattern = r"Ende: (\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}).*"
    for line in description:
        match = re.search(pattern, line)
        if match:
            date_str = match.group(1)
            time_str = match.group(2)
            return datetime.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

    return datetime.datetime.max

def parse_time_loss(description):
    pattern = r"Reisezeitverlust: (\d+) Minuten"
    for line in description:
        match = re.search(pattern, line)
        if match:
            minutes = int(match.group(1))
            return datetime.timedelta(minutes=minutes)

    return datetime.timedelta()

def fetch_traffic_warnings(road_id):
    url = f"{baseURL}{road_id}/services/warning"
    response = requests.get(url, headers={"accept": "application/json"})

    if response.status_code == 200:
        data = response.json().get("warning", [])
        traffic_issues = []

        for item in data:
            longitude = float(item["coordinate"]["long"])
            latitude = float(item["coordinate"]["lat"])
            description = " ".join(item["description"])
            isBlocked = item["isBlocked"] == "true"
            estimatedTimeLoss = parse_time_loss(item["description"]).total_seconds()
            beginTime = datetime.datetime.fromisoformat(item["startTimestamp"])
            endTime = parse_end_time(item["description"])

            traffic_issues.append(TrafficIssue(longitude, latitude, description, isBlocked,
                                               estimatedTimeLoss, beginTime, endTime))

        return traffic_issues
    else:
        print(f"Error: Unable to fetch data, status code {response.status_code}")
        return []

def featch_constructions(road_id):
    url = f"{baseURL}{road_id}/services/roadworks"
    response = requests.get(url, headers={"accept": "application/json"})
    if response.status_code == 200:
        data = response.json().get("roadworks", [])
        traffic_issues = []

        for item in data:
            longitude = float(item["coordinate"]["long"])
            latitude = float(item["coordinate"]["lat"])
            description = " ".join(item["description"])
            isBlocked = item["isBlocked"] == "true"
            estimatedTimeLoss = parse_time_loss(item["description"]).total_seconds()
            beginTime = datetime.datetime.now()
            try:
                beginTime = datetime.datetime.fromisoformat(item["startTimestamp"])
            except Exception as e:
                pass
            endTime = parse_end_time(item["description"])

            traffic_issues.append(TrafficIssue(longitude, latitude, description, isBlocked,
                                               estimatedTimeLoss, beginTime, endTime))

        return traffic_issues
    else:
        print(f"Error: Unable to fetch data, status code {response.status_code}")
        return []

def get_all_traffic_warnings():
    street_ids = fetch_german_streets()
    all_traffic_warnings = []

    for road_id in street_ids:
        traffic_warnings = fetch_traffic_warnings(road_id)
        all_traffic_warnings.extend(traffic_warnings)

    return all_traffic_warnings

def get_all_constructions():
    street_ids = fetch_german_streets()
    all_constructions = []

    for road_id in street_ids:
        constructions = featch_constructions(road_id)
        all_constructions.extend(constructions)

    return all_constructions

print(get_all_constructions())