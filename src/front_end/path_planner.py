from scraping.traffic_data.traffic_issues import traffic_issues, get_construction_data


def plan_route(start, destination, settings):
    return {
        "route_segments": [
        { "type": "Truck", # in {"Truck", "Train", "Ship", "Plane"}
            "path": [start["coords"], [51.127157518967245, 1.3116239025809384]], # Coordinates of origin and destination
            "distance": 100000, # in m
            "duration": 5700, # in s
            "cost": 100, # in s
            "co2_emissions": 50, # in CO₂e
        }, 
        { "type": "Ship",
            "path": [[51.127157518967245, 1.3116239025809384], [50.96130680566652, 1.8480674104593646]], # Coordinates of origin and destination
            "distance": 60000, # in m
            "duration": 5400, # in s
            "cost": 200, # in s
            "co2_emissions": 100, # in CO₂e
        }, 
        { "type": "Truck",
            "path": [[50.96130680566652, 1.8480674104593646], [48.86424304263961, 2.347387426187569]], # Coordinates of origin and destination
            "distance": 288000, # in m
            "duration": 11000, # in s
            "cost": 150, # in s
            "co2_emissions": 250, # in CO₂e
        },
        { "type": "Train",
            "path": [[48.86424304263961, 2.347387426187569], [48.14250741518001, 11.578348511310208]], # Coordinates of origin and destination
            "distance": 800000, # in m
            "duration": 24000, # in s
            "cost": 250, # in s
            "co2_emissions": 150, # in CO₂e
        },
        { "type": "Truck",
            "path": [[48.14250741518001, 11.578348511310208], destination["coords"]],
            "distance": 160000, # in m
            "duration": 6800, # in s
            "cost": 150, # in s
            "co2_emissions": 200,
        }
        ],
    }
