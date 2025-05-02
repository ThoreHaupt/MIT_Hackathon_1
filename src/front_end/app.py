from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        start_point = request.form.get('start_point')
        end_point = request.form.get('end_point')
        time_weight = float(request.form.get('time_weight', 1))
        cost_weight = float(request.form.get('cost_weight', 1))
        carbon_weight = float(request.form.get('carbon_weight', 1))
        product_type = request.form.get('product_type')

        # Here we'll add the logic to calculate routes and costs
        # For now, we'll just return the input data
        return jsonify({
            'start': start_point,
            'end': end_point,
            'weights': {
                'time': time_weight,
                'cost': cost_weight,
                'carbon': carbon_weight
            },
            'product': product_type
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)