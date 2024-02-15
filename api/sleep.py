from flask import Blueprint, jsonify, request
from model.sleeps import Sleep

sleep_api = Blueprint('sleep_api', __name__)

# Endpoint to get all sleep data
@sleep_api.route('/sleep', methods=['GET'])
def get_all_sleep():
    sleeps = Sleep.read_all()
    sleep_list = []
    for sleep in sleeps:
        sleep_dict = {
            'id': sleep.id,
            'gender': sleep.gender,
            'age': sleep.age,
            'occupation': sleep.occupation,
            'sleep_duration': sleep.sleep_duration,
            'quality_of_sleep': sleep.quality_of_sleep,
            'physical_activity_level': sleep.physical_activity_level,
            'stress_level': sleep.stress_level,
            'bmi_category': sleep.bmi_category,
            'blood_pressure': sleep.blood_pressure,
            'heart_rate': sleep.heart_rate,
            'daily_steps': sleep.daily_steps,
            'sleep_disorder': sleep.sleep_disorder
        }
        sleep_list.append(sleep_dict)
    return jsonify({'sleeps': sleep_list})

# Endpoint to create a new sleep entry
@sleep_api.route('/sleep', methods=['POST'])
def create_sleep():
    data = request.get_json()
    sleep = Sleep(
        data['id'],
        data['gender'],
        data['age'],
        data['occupation'],
        data['sleep_duration'],
        data['quality_of_sleep'],
        data['physical_activity_level'],
        data['stress_level'],
        data['bmi_category'],
        data['blood_pressure'],
        data['heart_rate'],
        data['daily_steps'],
        data['sleep_disorder']
    )
    try:
        sleep.create()
        return jsonify({'message': 'Sleep entry created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
