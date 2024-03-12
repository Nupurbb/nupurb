""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Fitness(db.Model):
    __tablename__ = 'fitness_activities'
    _Activity = db.Column(db.String(255), primary_key=True)
    _CaloriesBurned = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, Activity, CaloriesBurned):
        self._Activity = Activity
        self._CaloriesBurned = CaloriesBurned

    @property
    def Activity(self):
        return self._Activity

    @Activity.setter
    def Activity(self, Activity):
        self._Activity = Activity

    @property
    def CaloriesBurned(self):
        return self._CaloriesBurned

    @CaloriesBurned.setter
    def CaloriesBurned(self, CaloriesBurned):
        self._CaloriesBurned = CaloriesBurned

    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "Activity": self.Activity,
            "CaloriesBurned": self.CaloriesBurned
        }

    def update(self, Activity="", CaloriesBurned=0):
        if len(Activity) > 0:
            self.Activity = Activity
        if CaloriesBurned >= 0:
            self.CaloriesBurned = CaloriesBurned
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initfitnessy():
    with app.app_context():
        db.create_all()
        activities_to_add = []
        try:
            with open(r'fitness_activities.json', 'r') as json_file:
                data = json.load(json_file)
        except Exception as error:
            print("failed")
        for item in data:
            activity_to_add = Fitness(Activity=item['Activity'], CaloriesBurned=item['CaloriesBurned'])
            activities_to_add.append(activity_to_add)
        for activity in activities_to_add:
            try:
                activity.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate activity, or error: {activity}")

initfitnessy()

