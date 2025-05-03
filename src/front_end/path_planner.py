from scraping.traffic_data.traffic_issues import traffic_issues, get_construction_data


def plan_route(start, destination, settings):
    traffic_issues_data = [issue.to_dict() for issue in traffic_issues()]
    construction_sites_data = [issue.to_dict() for issue in get_construction_data()]
    return {
        "route_segments": [
        { "type": "Truck", # in {"Truck", "Train", "Ship", "Plane"}
            "path": [start["coords"], [3, 6]], # Coordinates of origin and destination
            "distance": 10, # in m
            "duration": 3600, # in s
            "cost": 100, # in s
            "co2_emissions": 50, # in CO₂e
        }, 
        { "type": "Train",
            "path": [[3, 6], [7, 8]], # Coordinates of origin and destination
            "distance": 20, # in m
            "duration": 7200, # in s
            "cost": 200, # in s
            "co2_emissions": 100, # in CO₂e
        }, 
        { "type": "Train",
            "path": [[7, 8], [10, 8]], # Coordinates of origin and destination
            "distance": 30, # in m
            "duration": 10800, # in s
            "cost": 300, # in s
            "co2_emissions": 150, # in CO₂e
        },
        { "type": "Plane",
            "path": [[10, 8], [15, 3]], # Coordinates of origin and destination
            "distance": 30, # in m
            "duration": 10800, # in s
            "cost": 300, # in s
            "co2_emissions": 150, # in CO₂e
        },
        { "type": "Train",
            "path": [[15, 3], destination["coords"]],
            "distance": 40, # in m
            "duration": 14400, # in s
            "cost": 400, # in s
            "co2_emissions": 200,
        }
        ],
        "traffic_issues": traffic_issues_data,
        "construction_sites": construction_sites_data,
    }
