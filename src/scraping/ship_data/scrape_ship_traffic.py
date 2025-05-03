from typing import Tuple

from .Harbors import Harbor
import os

# Shanghai 4393
# Rotterdam 4023
# Genua 466
# LA 1032
# new york 4068

take = [4393, 4023, 466, 1032, 4068]

def read_harbors_from_file(filename: str) -> dict[int, Harbor]:
    harbors = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(', ')
            if len(parts) >= 4:
                try:
                    harbor_id = int(parts[0])
                    if not harbor_id in take:
                        continue

                    name = parts[1]
                    latitude = float(parts[2])
                    longitude = float(parts[3])
                    harbors[harbor_id] = Harbor(harbor_id, name, latitude, longitude)
                except (ValueError, IndexError):
                    continue
    return harbors

def generate_filtered_pairs(set_a: dict[int, Harbor], set_b: dict[int, Harbor]) -> list[tuple[Harbor, Harbor]]:
    pairs = []
    for harbor_a in set_a.values():
        for harbor_b in set_b.values():
            if harbor_a.id != harbor_b.id:
                # Skip if IDs are equal
                #print(harbor_b)
                pairs.append((harbor_a, harbor_b))
    return pairs

def get_mock_data() -> tuple[Harbor, Harbor]:
    return (Harbor(1, "Hamburg", 53.534105, 9.913202), Harbor(2, "Boston", 42.341633, -71.020979))

def get_all_routes_ship():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    harbor_file = os.path.join(dir_path, "world_harbors_with_ids.txt")
    habors = read_harbors_from_file(harbor_file)
    # print(habors)
    # return generate_filtered_pairs(habors, habors)
    return get_mock_data()
