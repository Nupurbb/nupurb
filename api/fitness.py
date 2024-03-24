import json,jwt
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.fitnessy import Fitness

fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')
api = Api(fitness_api)

class FitnessAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            exerciseName = body.get('exerciseName')
            if exerciseName is None or len(exerciseName) < 2:
                return {'message': f'exerciseName is missing or less than 2 characters'}, 400
            calories_burned = body.get('calories_burned')
            if calories_burned is None or calories_burned < 0:
                return {'message': f'calories_burned must be a positive number'}, 400

            newExercise = Fitness(
                exerciseName=exerciseName,
                calories_burned=calories_burned
            )

            just_added_exercise = newExercise.create()
            if just_added_exercise:
                return jsonify(just_added_exercise.read())
            return {'message': f'Failed to add {exerciseName}. Possible format error or duplicate'}, 400

        def get(self):
            exercises = Fitness.query.all()
            json_ready = [exercise.read() for exercise in exercises]
            return jsonify(json_ready)

        def delete(self):
            body = request.get_json()
            del_fitness = body.get('fitnessName')
            result = Fitness.query.filter(Fitness.fitnessName == del_fitness).first()
            if result is None:
                return {'message': f'Fitness {del_fitness} not found'}, 404
            else:
                result.delete()
                return {'message': f'Exercise {del_fitness} deleted successfully'}, 200

    class _Get(Resource):
        def get(self, name=None):
            if name:
                result = Fitness.query.filter_by(exerciseName=name).first()
                if result:
                    return jsonify([result.read()])
                else:
                    return jsonify({"message": "Exercise not found"}), 404

    api.add_resource(_CRUD, '/blah')
    api.add_resource(_Get, '/<string:name>')
