import requests
from .WetterEnum import WeatherCondition


PICTOCODE_TO_WEATHER = {
    2: WeatherCondition.SUNNY,
    3: WeatherCondition.PARTLY_CLOUDY,
    4: WeatherCondition.CLOUDY,
    8: WeatherCondition.RAINY,
    16: WeatherCondition.POURING,
    # Extend if needed
}

location_cache = {}

def get_wetter_data(loc_lat, loc_lon):
    location_key = f"{loc_lat},{loc_lon}"

    # Check if the data is already cached
    if location_key in location_cache:
        print("Using cached data for location.")
        return location_cache[location_key]

    url = f"https://my.meteoblue.com/packages/basic-day?apikey=QRX0VH281kMZpluv&lat={loc_lat}&lon={loc_lon}&asl=118&format=json"
    response = requests.get(url, headers={"accept": "application/json"})

    if not response.ok:
        print(f"Failed to get weather data: {response.status_code}")
        return None

    data = response.json()

    pictocodes = data["data_day"]["pictocode"]
    dates = data["data_day"]["time"]

    worst_weather = [
        PICTOCODE_TO_WEATHER.get(code, WeatherCondition.EXTREME_WEATHER_WARNING)
        for code in pictocodes
    ]

    # Combine date and weather
    result = list(zip(dates, worst_weather))
    location_cache[location_key] = result

    # for date, weather in result:
    #     print(f"{date}: {weather.value}")

    return result

# print(get_wetter_data(50.1, 8.6))