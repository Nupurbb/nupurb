from flask import Flask, Blueprint, jsonify, request
import pandas as pd
from flask_cors import CORS
import os
from flask_restful import Api, Resource

# Create a single Flask application
app = Flask(__name__)

# Create a blueprint for the API
sleep_api = Blueprint('sleep_api', __name__, url_prefix='/sleep')
api_sleep = Api(sleep_api)

# Enable CORS for the sleep_api blueprint
CORS(sleep_api)

class SleepDataAPI(Resource):
    def get(self):
        # Get the path to the sleep database
        app_root = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(app_root, 'sleep.csv')
        
        try:
            data_sleep = pd.read_csv(csv_path)
            
            # Define default values for missing fields
            defaults = {
                'Occupation': 'Unknown',
                'Sleep Disorder': 'None'
            }
            
            # Fill missing fields with default values
            data_sleep = data_sleep.fillna(defaults)
        except FileNotFoundError:
            return {"error": "File not found"}, 404

        if data_sleep.empty:
            return jsonify({"error": "Data not available"}), 404

        return jsonify(data_sleep.to_dict(orient='records'))

    def post(self):
        # Get the sleep duration from the request
        sleep_duration = request.args.get('duration')  # Use args instead of json for GET requests

        # Get the path to the sleep database
        app_root = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(app_root, 'sleep.csv')

        try:
            data_sleep = pd.read_csv(csv_path)
            
            # Define default values for missing fields
            defaults = {
                'Occupation': 'Unknown',
                'Sleep Disorder': 'None'
            }
            
            # Fill missing fields with default values
            data_sleep = data_sleep.fillna(defaults)
        except FileNotFoundError:
            return {"error": "File not found"}, 404

        if data_sleep.empty:
            return jsonify({"error": "Data not available"}), 404

        # Filter data based on sleep duration
        filtered_data = data_sleep[data_sleep['Sleep Duration'] == float(sleep_duration)]

        if filtered_data.empty:
            return jsonify({"error": "Sleep duration not found"}), 404  # Return error if sleep duration not found

        return jsonify(filtered_data.to_dict(orient='records'))

# Register the resources with the api_sleep object
api_sleep.add_resource(SleepDataAPI, '/')

# Register the blueprint with the Flask app
app.register_blueprint(sleep_api)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
