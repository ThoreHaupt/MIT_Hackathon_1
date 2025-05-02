from flask import Flask, render_template, request
from path_planner import plan_route  # Placeholder for your logic
from address_to_coord_converter import geocode_address  # Placeholder for your logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def route():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    mode = request.form.get('mode')
    origin_coords = geocode_address(origin)
    destination_coords = geocode_address(destination)

    route_data = plan_route({"name": origin, "coords": origin_coords}, {"name": destination, "coords": destination_coords}, mode)
    return render_template('result.html', origin=origin_coords, destination=destination_coords, mode=mode, route=route_data)

if __name__ == '__main__':
    app.run(debug=True)
