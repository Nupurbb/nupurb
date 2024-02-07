from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api, Resource
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)

pulse_api = Blueprint('pulse_api', __name__, url_prefix='/api/data')
api = Api(pulse_api)

CORS(pulse_api)

class PulseAPI:
    class _Read(Resource):
        def get(self):
            app_root = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(app_root, 'pulse.csv')  # Update the CSV file name
            data = pd.read_csv(csv_path)
            if data.empty:
                return jsonify({"error": "Data not available"}), 404
            return jsonify(data.to_dict(orient='records'))

    class _Create(Resource):
        def post(self):
            # You can handle the creation of a new entry here if needed
            pass

    class _PulseData(Resource):
        def get(self, pulse_name):
            app_root = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(app_root, 'pulse.csv')  # Update the CSV file name
            data = pd.read_csv(csv_path)
            pulse_data = data[(data['Pulse'] == pulse_name) & (data['Year'] == 2022)]  # Filter data for the specified county and year
            if pulse_data.empty:
                return jsonify({"error": "County data not found"}), 404
            result = pulse_data.to_dict(orient='records')[0]
            return jsonify(result)

api.add_resource(PulseAPI._Read, '/')
api.add_resource(PulseAPI._Create, '/create')
api.add_resource(PulseAPI._PulseData, '/pulse/<string:pulse_name>')

app.register_blueprint(pulse_api)

if __name__ == "__main__":
    app.run(debug=True)
