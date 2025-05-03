import requests
import time
from tqdm import tqdm


def query_overpass(bbox):
    """Query Overpass API for harbors in a given bounding box"""
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["harbour"]({bbox});
      way["harbour"]({bbox});
      relation["harbour"]({bbox});
    );
    out center;
    """

    try:
        response = requests.get(overpass_url, params={'data': query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Overpass API: {e}")
        return None


def process_osm_data(data):
    """Process OSM data to extract harbor information"""
    harbors = []

    for element in data['elements']:
        name = element.get('tags', {}).get('name', 'Unnamed Harbor')

        if element['type'] == 'node':
            lat = element['lat']
            lon = element['lon']
        elif element['type'] in ['way', 'relation']:
            lat = element.get('center', {}).get('lat')
            lon = element.get('center', {}).get('lon')
        else:
            continue

        if lat is not None and lon is not None:
            harbors.append((name, lat, lon))

    return harbors


def get_world_bboxes(grid_size=10):
    """Divide the world into smaller bounding boxes for querying"""
    # Bounding box format: (min_lat, min_lon, max_lat, max_lon)
    bboxes = []
    lat_step = 180 / grid_size
    lon_step = 360 / grid_size

    for lat_idx in range(grid_size):
        for lon_idx in range(grid_size):
            min_lat = -90 + lat_idx * lat_step
            max_lat = -90 + (lat_idx + 1) * lat_step
            min_lon = -180 + lon_idx * lon_step
            max_lon = -180 + (lon_idx + 1) * lon_step
            bboxes.append(f"{min_lat},{min_lon},{max_lat},{max_lon}")

    return bboxes


def main():
    output_file = "world_harbors.txt"
    grid_size = 10  # Higher number = smaller areas per query (reduce if getting timeouts)

    print(f"Dividing world into {grid_size}x{grid_size} grid for querying...")
    bboxes = get_world_bboxes(grid_size)

    all_harbors = []

    print("Querying OpenStreetMap for harbor data...")
    for bbox in tqdm(bboxes):
        data = query_overpass(bbox)
        if data and 'elements' in data:
            harbors = process_osm_data(data)
            all_harbors.extend(harbors)
        time.sleep(1)  # Be polite to the API

    # Remove duplicates (some harbors might appear in multiple bounding boxes)
    unique_harbors = list({(name, lat, lon) for name, lat, lon in all_harbors})

    print(f"Found {len(unique_harbors)} harbors. Saving to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        for name, lat, lon in unique_harbors:
            f.write(f"{name}, {lat}, {lon}\n")

    print("Done!")


def add_line_numbers_as_ids(input_file, output_file=None, delimiter=','):
    """
    Add line numbers as IDs to each line in a text file.

    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to the output file (if None, overwrites input file)
        delimiter (str): Delimiter to use between ID and original line content
    """
    # Read all lines from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process each line to add ID
    processed_lines = []
    for i, line in enumerate(lines, start=1):
        # Remove any existing newline characters
        cleaned_line = line.strip('\n\r')
        # Add ID and original content with delimiter
        processed_line = f"{i}{delimiter} {cleaned_line}\n"
        processed_lines.append(processed_line)

    # Determine output file path
    output_path = output_file if output_file else input_file

    # Write processed lines to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

    print(f"Successfully added IDs to {len(processed_lines)} lines.")


if __name__ == "__main__":
    add_line_numbers_as_ids("world_harbors.txt", "world_harbors_with_ids.txt")