import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.planners import Food, Exercise

fitness_api = Blueprint('fitness_api', __name__,
                   url_prefix='/api/fitness')

api = Api(fitness_api)

class FitnessAPI:        
    class _Log(Resource):
        @token_required
        def post(self, current_user): # Log food intake or exercise activity
            body = request.get_json()
            log_type = body.get('log_type')

            if log_type == 'food':
                food_name = body.get('food_name')
                calories = body.get('calories')
                if not food_name or not calories:
                    return {'message': 'Food name or calories missing'}, 400

                new_food = Food(food_name=food_name, calories=calories, user_id=current_user.id)
                created_food = new_food.create()

                if created_food:
                    return jsonify(created_food.serialize()), 201
                else:
                    return {'message': 'Failed to log food intake'}, 500

            elif log_type == 'exercise':
                exercise_name = body.get('exercise_name')
                calories_burned = body.get('calories_burned')
                if not exercise_name or not calories_burned:
                    return {'message': 'Exercise name or calories burned missing'}, 400

                new_exercise = Exercise(exercise_name=exercise_name, calories_burned=calories_burned, user_id=current_user.id)
                created_exercise = new_exercise.create()

                if created_exercise:
                    return jsonify(created_exercise.serialize()), 201
                else:
                    return {'message': 'Failed to log exercise activity'}, 500

            else:
                return {'message': 'Invalid log type'}, 400

        @token_required
        def get(self, current_user):  # Retrieve user's fitness log
            foods = Food.query.filter_by(user_id=current_user.id).all()
            exercises = Exercise.query.filter_by(user_id=current_user.id).all()

            food_logs = [food.serialize() for food in foods]
            exercise_logs = [exercise.serialize() for exercise in exercises]

            return jsonify({'foods': food_logs, 'exercises': exercise_logs}), 200

    api.add_resource(_Log, '/log')