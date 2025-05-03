from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from path_planner import plan_route  # Placeholder for your logic
from address_to_coord_converter import geocode_address  # Placeholder for your logic

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html', route=None)

@app.route('/route', methods=['POST'])
def route():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    origin_coords = geocode_address(origin)
    destination_coords = geocode_address(destination)
    settings = {
        "use_truck": request.form.get('truckCheckBox') == 'on',
        "use_train": request.form.get('trainCheckBox') == 'on',
        "use_ship": request.form.get('shipCheckBox') == 'on',
        "use_plane": request.form.get('airCheckBox') == 'on',
        "weight_time": float(request.form.get('timeImportance', 0)),
        "weight_co2": float(request.form.get('co2Importance', 0)),
        "weight_money": float(request.form.get('moneyImportance', 0)),
        "weight_risk": float(request.form.get('riskImportance', 0)),
        "freight_weight": float(request.form.get('freightWeight', 0)),
        "freight_size": float(request.form.get('freightSize', 0)),
    }

    route_data = plan_route({"name": origin, "coords": origin_coords}, {"name": destination, "coords": destination_coords}, settings)
    return jsonify(route_data)

if __name__ == '__main__':
    app.run(debug=True)
