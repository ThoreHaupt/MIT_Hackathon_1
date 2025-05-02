from flask import Flask, render_template, request
from path_planner import plan_route  # Placeholder for your logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def route():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    mode = request.form.get('mode')

    route_data = plan_route(origin, destination, mode)
    return render_template('result.html', origin=origin, destination=destination, mode=mode, route=route_data)

if __name__ == '__main__':
    app.run(debug=True)
