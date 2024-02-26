import json
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required

from model.fitnessy import Fitness

fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')

api = Api(fitness_api)

class FitnessAPI:
    class _CRUD(Resource):
        @token_required
        def post(self, current_user):
            body = request.get_json()
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            
            # Adjustments for fitness data
            age = body.get('age')
            weight = body.get('weight')
            height = body.get('height')
            gender = body.get('gender')
            activity_level = body.get('activity_level')

            # Example validation
            if age is None or age <= 0:
                return {'message': 'Invalid age'}, 400
            if weight is None or weight <= 0:
                return {'message': 'Invalid weight'}, 400
            if height is None or height <= 0:
                return {'message': 'Invalid height'}, 400
            if gender not in ['male', 'female']:
                return {'message': 'Invalid gender'}, 400
            if activity_level not in ['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active']:
                return {'message': 'Invalid activity level'}, 400
            
            # Create Fitness object
            fitness_data = {
                'name': name,
                'age': age,
                'weight': weight,
                'height': height,
                'gender': gender,
                'activity_level': activity_level
            }
            new_fitness_record = Fitness(**fitness_data)

            # Example: saving to database
            new_fitness_record.save()

            return jsonify({'message': 'Fitness data saved successfully'}), 201

        def get(self, current_user):
            # Example: Retrieving fitness data
            fitness_records = Fitness.query.all()
            json_ready = [record.serialize() for record in fitness_records]
            return jsonify(json_ready)

    api.add_resource(_CRUD, '/')



