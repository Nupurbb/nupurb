from flask import Flask, Blueprint, jsonify, request
import pandas as pd
from flask_cors import CORS  # Import CORS
import os
from flask_restful import Api, Resource

app = Flask(__name__)

pulse_api = Blueprint('heartrate_api', __name__, url_prefix='/api/heartrate')
api_pulse = Api(pulse_api)

# Enable CORS for all routes
CORS(app)

class PulseAPI(Resource):
    class _Read(Resource):
        def get(self):
            csv_path = os.path.join("api", 'pulse.csv')  # Update the CSV file path
            data = pd.read_csv(csv_path)
            if data.empty:
                return jsonify({"error": "Data not available"}), 404
            return jsonify(data.to_dict(orient='records'))

    class _Create(Resource):
        def post(self):
            data = request.get_json()

            # Check if data is not empty and contains required fields
            if not data or not isinstance(data, list) or not all(key in data[0] for key in ['Active', 'Rest', 'Smoke', 'Sex', 'Exercise', 'Hgt', 'Wgt']):
                return jsonify({"error": "Invalid data format"}), 400

            # Convert data into DataFrame
            df = pd.DataFrame(data)

            # Calculate average heart rate by gender
            gender_avg_hr = df.groupby('Sex')['Active'].mean().to_dict()

            # Calculate average heart rate by level of exercise
            exercise_avg_hr = df.groupby('Exercise')['Active'].mean().to_dict()

            response_data = {
                "averageHeartRate": {
                    "gender": gender_avg_hr,
                    "exercise": exercise_avg_hr
                }
            }

            return jsonify(response_data)

    class _PulseData(Resource):
        def get(self, pulse_id):
            csv_path = os.path.join("api", 'pulse.csv')  # Update the CSV file path
            data = pd.read_csv(csv_path)
            pulse_data = data[data.index == int(pulse_id)]
            if pulse_data.empty:
                return jsonify({"error": "Data not found"}), 404
            result = pulse_data.to_dict(orient='records')[0]
            return jsonify(result)

# Register the resources with the api_pulse object
api_pulse.add_resource(PulseAPI._Read, '/')
api_pulse.add_resource(PulseAPI._PulseData, '/<int:pulse_id>')
api_pulse.add_resource(PulseAPI._Create, '/create')
# Register the blueprint with the Flask app
app.register_blueprint(pulse_api)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
