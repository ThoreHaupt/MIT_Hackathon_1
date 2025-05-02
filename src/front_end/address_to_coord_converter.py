import requests

def geocode_address(address):
    """
    Geocode a single address to its latitude and longitude coordinates.
    :param address: The address to geocode as a string.
    :return: A tuple containing the latitude and longitude of the address.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "freight-planner/1.0"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        return None