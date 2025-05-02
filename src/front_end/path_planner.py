def plan_route(origin, destination, mode):
    # Simulated coordinates
    coords = {
        "New York": [40.7128, -74.0060],
        "Los Angeles": [34.0522, -118.2437],
        "Chicago": [41.8781, -87.6298],
        "Houston": [29.7604, -95.3698]
    }

    origin_coords = coords.get(origin, [40.0, -75.0])
    destination_coords = coords.get(destination, [35.0, -90.0])

    return {
        "steps": [
            f"Start at {origin}",
            f"Use {mode} to reach {destination}"
        ],
        "duration": "5 hours",
        "cost_estimate": "$1,200",
        "origin_coords": origin_coords,
        "destination_coords": destination_coords
    }
