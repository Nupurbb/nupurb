""" database dependencies to support sqliteDB examples """
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
class Fitness(db.Model):
    __tablename__ = 'fitnessy'  # table name is plural, class name is singular

    # Define the Drink schema with "vars" from object
    _fitnessName = db.Column(db.String(255), primary_key=True)
    _age = db.Column(db.Integer, unique=False, nullable=False)

    # constructor of a Drink object, initializes the instance variables within object (self)
    def __init__(self, fitnessName, age):
        self._fitnessName = fitnessName    # variables with self prefix become part of the object, 
        self._age = age


    # a drinkName getter method, extracts drinkName from object
    @property
    def fitnessName(self):
        return self._fitnessName
    
    # a setter function, allows drinkName to be updated after initial object creation
    @fitnessName.setter
    def fitnessName(self, fitnessName):
        self._fitnessName = fitnessName
    
    # a getter method, extracts calories from object
    @property
    def age(self):
        return self._age
    
    # a setter function, allows calories to be updated after initial object creation
    @age.setter
    def age(self, age):
        self._age = age
          
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
            "fitnessName": self.fitnessName,
            "age": self.age
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, fitnessName="", age=0):
        """only updates values with length"""
        if len(fitnessName) > 0:
            self.fitnessName = fitnessName
        if age >= 0:
            self.age = age
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
def initFitnessy():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        #f1 = Fitnessy(fitnessName='run', age=10)
        #f2 = Fitnessy(drinkName='Pilates', age=20)

        fitnessytoadd = []
        try:
            with open(r'fitness.json','r') as json_file:
                data = json.load(json_file)
        except Exception as error:
            print("failed")

        for item in data:
            print(item)
            f_toadd = Fitness(FitnessName=item['fitnessName'], age=item['age'])
            fitnessytoadd.append(f_toadd)

        """Builds sample user/note(s) data"""
        for f in fitnessytoadd:
            try:
                f.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {f.fitnessytoadd}")
            
