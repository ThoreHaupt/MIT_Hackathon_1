def plan_route(origin, destination, mode):
    # Simulated coordinates
    coords = {
        "New York": [40.7128, -74.0060],
        "Chicago": [41.8781, -87.6298],
        "Los Angeles": [34.0522, -118.2437],
    }

    origin_coords = coords.get(origin, [40.0, -75.0])
    mid_coords = coords.get("Chicago", [41.8, -87.6])
    destination_coords = coords.get(destination, [35.0, -90.0])

    # Simulated multimodal route: Truck to Chicago, Train to LA
    return {
        "steps": [
            f"Truck from {origin} to Chicago",
            f"Train from Chicago to {destination}"
        ],
        "duration": "12 hours",
        "cost_estimate": "$1,800",
        "co2_emissions": "200 kg CO2",
        "segments": [
            {
                "mode": "Truck",
                "path": [origin_coords, mid_coords]
            },
            {
                "mode": "Train",
                "path": [mid_coords, destination_coords]
            }
        ]
    }
