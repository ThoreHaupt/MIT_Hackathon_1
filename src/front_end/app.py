from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from .path_planner import plan_route  # Placeholder for your logic
from .address_to_coord_converter import geocode_address  # Placeholder for your logic
from scraping.traffic_data.traffic_issues import traffic_issues, get_construction_data

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html', route=None)

@app.route('/route', methods=['POST'])
def route():
    start = request.form.get('start')
    destination = request.form.get('destination')
    start_coords = [51.51152244586142, -0.11945285580050813] #geocode_address(start)
    destination_coords = [47.60407666445795, 12.986876363537341] #geocode_address(destination)
    settings = {
        "use_truck": request.form.get('truckCheckBox') == 'on',
        "use_train": request.form.get('trainCheckBox') == 'on',
        "use_ship": request.form.get('shipCheckBox') == 'on',
        "use_plane": request.form.get('planeCheckBox') == 'on',
        "weight_time": float(request.form.get('timeImportance', 0)),
        "weight_co2": float(request.form.get('co2Importance', 0)),
        "weight_money": float(request.form.get('moneyImportance', 0)),
        "weight_risk": float(request.form.get('riskImportance', 0)),
        "freight_weight": float(request.form.get('freightWeight', 0)),
        "freight_size": float(request.form.get('freightSize', 0)),
    }

    route_data = plan_route({"name": start, "coords": start_coords}, {"name": destination, "coords": destination_coords}, settings)
    return jsonify(route_data)


@app.route('/traffic_issues_request', methods=['POST'])
def traffic_issues_request():
    traffic_issues_data = [issue.to_dict() for issue in traffic_issues()]
    return jsonify(traffic_issues_data)

@app.route('/construction_sites_request', methods=['POST'])
def construction_sites_request():
    construction_data = [site.to_dict() for site in get_construction_data()]
    return jsonify(construction_data)

if __name__ == '__main__':
    app.run(debug=True)
