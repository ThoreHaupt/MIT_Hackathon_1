def plan_route(origin, destination, settings):

    # Simulated multimodal route: Truck to Chicago, Train to LA
    return {
        "steps": [
            f"Truck from {origin["name"]} to {destination["name"]}",
        ],
        "duration": "12 hours",
        "cost_estimate": "$1,800",
        "co2_emissions": "200 kg CO2",
        "segments": [
            {
                "type": "Truck",
                "path": [origin["coords"], destination["coords"]]
            }
        ]
    }
