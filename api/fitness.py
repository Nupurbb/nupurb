import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.fitnessy import fitness
fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')
api = Api(fitness_api)

class FitnessAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            activity = body.get('activity')
            calories_burned_per_hour = body.get('calories_burned_per_hour')
            intensity_level = body.get('intensity_level')
            equipment_needed = body.get('equipment_needed')

            if not all([activity, calories_burned_per_hour, intensity_level, equipment_needed]):
                return {'message': 'Missing required fields'}, 400

            new_activity = fitness(activity=activity, calories_burned_per_hour=calories_burned_per_hour,
                                            intensity_level=intensity_level, equipment_needed=equipment_needed)
            new_activity.save()

            return jsonify(new_activity.serialize())

        def get(self):
            activities = fitness.query.all()
            json_ready = [activity.serialize() for activity in activities]
            return jsonify(json_ready)

        def delete(self):
            body = request.get_json()
            activity_name = body.get('activity')

            activity =fitness.query.filter_by(activity=activity_name).first()

            if activity:
                activity.delete()
                return {'message': f'{activity_name} deleted successfully'}
            else:
                return {'message': f'{activity_name} not found'}, 404

    class _get(Resource):
        def get(self, activity_name=None):
            if activity_name:
                activity = fitness.query.filter_by(activity=activity_name).first()
                if activity:
                    return jsonify(activity.serialize())
                else:
                    return {'message': 'Activity not found'}, 404
            else:
                return {'message': 'Please provide an activity name'}, 400

    api.add_resource(_CRUD, '/')
    api.add_resource(_get, '/<string:activity_name>')
