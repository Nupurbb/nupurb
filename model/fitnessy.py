""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Fitness(db.Model):
    __tablename__ = 'fitness'

    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _age = db.Column(db.Integer, nullable=False)
    _weight = db.Column(db.Float, nullable=False)
    _height = db.Column(db.Float, nullable=False)
    _gender = db.Column(db.String(10), nullable=False)
    _activity_level = db.Column(db.String(20), nullable=False)

    def __init__(self, name, age, weight, height, gender, activity_level):
        self._name = name
        self._age = age
        self._weight = weight
        self._height = height
        self._gender = gender
        self._activity_level = activity_level

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def weight(self):
        return self._weight

    @property
    def height(self):
        return self._height

    @property
    def gender(self):
        return self._gender

    @property
    def activity_level(self):
        return self._activity_level

    def serialize(self):
        return {
            "name": self._name,
            "age": self._age,
            "weight": self._weight,
            "height": self._height,
            "gender": self._gender,
            "activity_level": self._activity_level
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

def initFitnessy():
    with app.app_context():
        db.create_all()
        # Add initialization data if needed


