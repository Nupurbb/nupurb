import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.pulses import Pulse
pulse_api = Blueprint('pulse_api', __name__,
                   url_prefix='/api/pulses')
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(pulse_api)
class PulseyAPI:
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
            # validate drinkName
            Active = body.get('Active')
            if Active is None or len(Active) < 2:
                return {'message': f'Active is missing, or is less than 2 characters'}, 400
            # validate uid
            Exercise = body.get('Exercise')
            if Exercise is None or Exercise < 0 :
                return {'message': f'Exercise has to be positive number'}, 400
            ''' #1: Key code block, setup USER OBJECT '''
            newPulse = Pulse(Active=Active,
                      Exercise=Exercise)
            ''' #2: Key Code block to add user to database '''
            # create drink in database
            just_added_pulse = newPulse.create()
            # success returns json of user
            if just_added_pulse:
                return jsonify(just_added_pulse.read())
            # failure returns error
            return {'message': f'Processed {Active}, either a format error or it is duplicate'}, 400
        def get(self): # Read Method
            pulses = Pulse.query.all()    # read/extract all users from the database
            json_ready = [pulse.read() for pulse in pulses]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        def delete(self):  # Delete method
            ''' Find user by ID '''
            body = request.get_json()
            del_pulse = body.get('Active')
            result = Pulse.query.filter(Pulse._Active == del_pulse).first()
            if result is None:
                 return {'message': f'pulse {del_pulse} not found'}, 404
            else:
                result.delete()
                print("delete")
           # del_found = Drink.query.get(del_drink)
            # print(del_found)
            # if del_found is None:
            #     return {'message': f'drink {del_drink} not found'}, 404
            # else:
            #     del_found.delete()
    class _get(Resource):
        def get(self, lname=None):  # Updated method with lname parameter
            #lname="'" + lname + "'"
            print(lname)
            if lname:
                result = Pulse.query.filter_by(_Active=lname).first()
                #result = Drink.query.filter(Drink._drinkName == lname).first()
                #result = Drink.query.first_or_404(lname)  # Adjust this based on your model attributes
                print(result)
                if result:
                    print(result)
                    return jsonify([result.read()])  # Assuming you have a read() method in your PulseyApi model
                else:
                    return jsonify({"message": "Pulse not found"}), 404
    # class _update(Resource):
    #     def put(self, id):  # Update method
    #         ''' Read data for json body '''
    #         body = request.get_json()
    #         ''' Find user by ID '''
    #         user = User.query.get(id)
    #         if user is None:
    #             return {'message': f'User with ID {id} not found'}, 404
    #         ''' Update fields '''
    #         name = body.get('name')
    #         if name:
    #             user.name = name
    #         uid = body.get('uid')
    #         if uid:
    #             user.uid = uid
    #         user.server_needed = body.get('server_needed')
    #         user.active_classes = body.get('active_classes')
    #         user.archived_classes = body.get('archived_classes')
    #         ''' Commit changes to the database '''
    #         user.update()
    #         return jsonify(user.read())
    # class _Security(Resource):
    #     def post(self):
    #         try:
    #             body = request.get_json()
    #             if not body:
    #                 return {
    #                     "message": "Please provide user details",
    #                     "data": None,
    #                     "error": "Bad request"
    #                 }, 400
    #             ''' Get Data '''
    #             uid = body.get('uid')
    #             if uid is None:
    #                 return {'message': f'User ID is missing'}, 400
    #             password = body.get('password')
    #             ''' Find user '''
    #             user = User.query.filter_by(_uid=uid).first()
    #             if user is None or not user.is_password(password):
    #                 return {'message': f"Invalid user id or password"}, 400
    #             if user:
    #                 try:
    #                     token = jwt.encode(
    #                         {"_uid": user._uid},
    #                         current_app.config["SECRET_KEY"],
    #                         algorithm="HS256"
    #                     )
    #                     resp = Response("Authentication for %s successful" % (user._uid))
    #                     resp.set_cookie("jwt", token,
    #                             max_age=3600,
    #                             secure=True,
    #                             httponly=True,
    #                             path='/',
    #                             samesite='None'  # This is the key part for cross-site requests
    #                             # domain="frontend.com"
    #                             )
    #                     return resp
    #                 except Exception as e:
    #                     return {
    #                         "error": "Something went wrong",
    #                         "message": str(e)
    #                     }, 500
    #             return {
    #                 "message": "Error fetching auth token!",
    #                 "data": None,
    #                 "error": "Unauthorized"
    #             }, 404
    #         except Exception as e:
    #             return {
    #                     "message": "Something went wrong!",
    #                     "error": str(e),
    #                     "data": None
    #             }, 500
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_get, '/<string:lname>')
    #api.add_resource(_Security, '/authenticate')