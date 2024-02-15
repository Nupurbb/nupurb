""" database dependencies to support sqliteDB examples """
import csv
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the drinks class to manage actions in the 'drinks' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Drink represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Pulse(db.Model):
    __tablename__ = 'pulses'  # table name is plural, class name is singular

    # Define the Drink schema with "vars" from object
    _Active = db.Column(db.String(255), primary_key=True)
    _Exercise = db.Column(db.Integer, unique=False, nullable=False)

    # constructor of a Drink object, initializes the instance variables within object (self)
    def __init__(self, Active, Exercise):
        self._Active = Active    # variables with self prefix become part of the object, 
        self._Exercise = Exercise


    # a drinkName getter method, extracts drinkName from object
    @property
    def Active(self):
        return self._Active
    
    # a setter function, allows drinkName to be updated after initial object creation
    @Active.setter
    def Active(self, Active):
        self._Active = Active
    
    # a getter method, extracts calories from object
    @property
    def Exercise(self):
        return self._Exercise 
    
    # a setter function, allows calories to be updated after initial object creation
    @Exercise.setter
    def Exercise(self, Exercise):
        self._Exercise = Exercise
          
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a drink object from Drink(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist drink object to drinks table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "Active": self.Active,
            "Exercise": self.Exercise
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, Active="", Exercise=0):
        """only updates values with length"""
        if len(Active) > 0:
            self.Active = Active
        if Exercise >= 0:
            self.Exercise = Exercise
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


    # Builds working data for testing
def initPulses():
        with app.app_context():
             """Create database and tables"""
             db.create_all()
             """Tester data for table"""
              #d1 = Pulse(Active='97', Exercise=1)
           #d2 = Pulse(Active='82', Exercise=3)

import csv

# Define lists to store data for each column
active_data = []
rest_data = []
smoke_data = []
sex_data = []
exercise_data = []
height_data = []
weight_data = []

try:
    with open('pulse.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            active_data.append(int(row['Active']))
            rest_data.append(int(row['Rest']))
            smoke_data.append(int(row['Smoke']))
            sex_data.append(int(row['Sex']))
            exercise_data.append(int(row['Exercise']))
            height_data.append(int(row['Hgt']))
            weight_data.append(int(row['Wgt']))
except Exception as e:
    print("Failed to read from CSV:", e)

for item in date:
            # print(item)
            p_toadd = Pulse(Active=item['Active'], Exercise=item['Exercise'])
            pulsestoadd.append(p_toadd)

"""Builds sample user/note(s) data"""
for p in pulsestoadd:
            try:
                p.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {p.pulsestoadd}")
            
