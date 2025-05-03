
from src.scraping.train_data.TrainClasses import TrainStation

import re
import requests

import os

def merge_station_files(source_folder: str, output_file: str):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in sorted(os.listdir(source_folder)):
            if filename.endswith(".txt"):
                filepath = os.path.join(source_folder, filename)
                with open(filepath, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    if content.strip():
                        outfile.write(content.strip() + "\n")
    print(f"Alle Dateien aus '{source_folder}' wurden in '{output_file}' zusammengeführt.")


def get_geofabrik_regions():
    url = "https://download.geofabrik.de/index-v1.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching Geofabrik data: {response.status_code}")

    data = response.json()
    regions = []

    def extract_regions(obj):
        if isinstance(obj, dict):
            if "name" in obj and "url" in obj:
                regions.append(obj["name"])
            for value in obj.values():
                extract_regions(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_regions(item)

    extract_regions(data)
    return sorted(set(regions))


# Usage:
# print(get_geofabrik_regions())


def speichere_bahnhoefe(region: str, dateiname: str):

    overpass_url = "http://overpass-api.de/api/interpreter"

    query = f"""
    [out:json][timeout:180];
    area["name"="{region}"]->.searchArea;
    (
      node["railway"="station"](area.searchArea);
      way["railway"="station"](area.searchArea);
      relation["railway"="station"](area.searchArea);
    );
    out center tags;
    """

    response = requests.post(overpass_url, data={"data": query})

    if response.status_code == 200:
        result = response.json()
        stations = []

        for element in result["elements"]:
            tags = element.get("tags", {})
            name = tags.get("name")
            lat = element.get("lat") or element.get("center", {}).get("lat")
            lon = element.get("lon") or element.get("center", {}).get("lon")

            if name and lat and lon:
                station = TrainStation(name, lat, lon)
                stations.append(station)

        # In Datei schreiben
        with open(dateiname, "w", encoding="utf-8") as f:
            for station in stations:
                f.write(str(station) + "\n")

        print(f"{len(stations)} Bahnhöfe gespeichert in {dateiname}")
    else:
        print(f"Fehler: {response.status_code} - {response.text}")

def get_osm_countries():
    query = """
    [out:json][timeout:180];
    relation["admin_level"="2"]["boundary"="administrative"];
    out tags;
    """
    response = requests.post("https://overpass-api.de/api/interpreter", data={"data": query})
    response.raise_for_status()
    data = response.json()
    countries = [el["tags"]["name"] for el in data["elements"] if "name" in el.get("tags", {})]
    return sorted(set(countries))

# def train_stations_eu():
#     url = "https://apis.deutschebahn.com/db-api-marketplace/apis/ris-stations/v1/stations?limit=2147483647&locales=FR"
#
#     headers = {
#         "DB-Client-ID": "d3dc669d4c3aa1ab24d627ed228d740c",
#         "DB-Api-Key": "a688710f9210a460f36f246ffd2e140d",
#         "accept": "application/vnd.de.db.ris+json"
#     }
#
#     response = requests.get(url, headers=headers)
#
#     # Save response to a text file
#     with open("api_response4.json", "w", encoding="utf-8") as file:
#         file.write(response.text)
#
#     print("Response saved to api_response.txt")
  # show first 10 for sanity check

def sanitize_filename(name: str) -> str:
    """
    Converts a region name into a safe filename.
    Removes or replaces characters that are invalid in filenames.
    """
    # Replace slashes and other special chars with underscores
    name = re.sub(r'[\/:*?"<>|\\]', '_', name)
    # Strip leading/trailing whitespace and dots
    name = name.strip().strip('.')
    return name


# for region in get_osm_countries():
#     print(region)
#     try:
#         speichere_bahnhoefe(region, f"tainstations/{sanitize_filename(region)}_stations.txt")
#     except Exception as e:
#         print(f"Fehler bei {region}: {e}")

# merge_station_files("tainstations", "trainstations.txt")

def parse_train_stations_from_file(filepath: str):
    stations = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                # Split name from coordinates
                name_part, coord_part = line.rsplit("(", 1)
                name = name_part.strip()
                lat_str, lon_str = coord_part.rstrip(")").split(",")
                lat = float(lat_str.strip())
                lon = float(lon_str.strip())
                stations.append(TrainStation(name, lat, lon))
            except Exception as e:
                print(f"⚠️ Fehler beim Parsen der Zeile: '{line}': {e}")
    return stations

def get_all_train_stations():
    return parse_train_stations_from_file("trainstations.txt")
