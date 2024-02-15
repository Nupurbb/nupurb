import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Import the Flask app and SQLAlchemy instance from __init__.py
from __init__ import app, db
import csv
import sqlite3

# Define the Sleep class to represent the 'sleep' table in the database
class Sleep:
    def __init__(self, id, gender, age, occupation, sleep_duration, quality_of_sleep, physical_activity_level, stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, sleep_disorder):
        self._id = id
        self._gender = gender
        self._age = age
        self._occupation = occupation
        self._sleep_duration = sleep_duration
        self._quality_of_sleep = quality_of_sleep
        self._physical_activity_level = physical_activity_level
        self._stress_level = stress_level
        self._bmi_category = bmi_category
        self._blood_pressure = blood_pressure
        self._heart_rate = heart_rate
        self._daily_steps = daily_steps
        self._sleep_disorder = sleep_disorder

    # Getters and setters for properties
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def gender(self):
        return self._gender
    
    @gender.setter
    def gender(self, value):
        self._gender = value
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value
    
    @property
    def occupation(self):
        return self._occupation
    
    @occupation.setter
    def occupation(self, value):
        self._occupation = value
    
    @property
    def sleep_duration(self):
        return self._sleep_duration
    
    @sleep_duration.setter
    def sleep_duration(self, value):
        self._sleep_duration = value
    
    @property
    def quality_of_sleep(self):
        return self._quality_of_sleep
    
    @quality_of_sleep.setter
    def quality_of_sleep(self, value):
        self._quality_of_sleep = value
    
    @property
    def physical_activity_level(self):
        return self._physical_activity_level
    
    @physical_activity_level.setter
    def physical_activity_level(self, value):
        self._physical_activity_level = value
    
    @property
    def stress_level(self):
        return self._stress_level
    
    @stress_level.setter
    def stress_level(self, value):
        self._stress_level = value
    
    @property
    def bmi_category(self):
        return self._bmi_category
    
    @bmi_category.setter
    def bmi_category(self, value):
        self._bmi_category = value
    
    @property
    def blood_pressure(self):
        return self._blood_pressure
    
    @blood_pressure.setter
    def blood_pressure(self, value):
        self._blood_pressure = value
    
    @property
    def heart_rate(self):
        return self._heart_rate
    
    @heart_rate.setter
    def heart_rate(self, value):
        self._heart_rate = value
    
    @property
    def daily_steps(self):
        return self._daily_steps
    
    @daily_steps.setter
    def daily_steps(self, value):
        self._daily_steps = value
    
    @property
    def sleep_disorder(self):
        return self._sleep_disorder
    
    @sleep_disorder.setter
    def sleep_disorder(self, value):
        self._sleep_disorder = value

    # CRUD functions
    def create(self):
        conn = sqlite3.connect('sleep.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sleep 
            (id, gender, age, occupation, sleep_duration, quality_of_sleep, physical_activity_level, stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, sleep_disorder)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.id,
            self.gender,
            self.age,
            self.occupation,
            self.sleep_duration,
            self.quality_of_sleep,
            self.physical_activity_level,
            self.stress_level,
            self.bmi_category,
            self.blood_pressure,
            self.heart_rate,
            self.daily_steps,
            self.sleep_disorder
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def read_all():
        conn = sqlite3.connect('sleep.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sleep')
        rows = cursor.fetchall()
        conn.close()
        sleeps = []
        for row in rows:
            sleep = Sleep(*row)
            sleeps.append(sleep)
        return sleeps

    def update(self):
        conn = sqlite3.connect('sleep.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE sleep SET 
            gender=?, 
            age=?, 
            occupation=?, 
            sleep_duration=?, 
            quality_of_sleep=?, 
            physical_activity_level=?, 
            stress_level=?, 
            bmi_category=?, 
            blood_pressure=?, 
            heart_rate=?, 
            daily_steps=?, 
            sleep_disorder=?
            WHERE id=?
        ''', (
            self.gender,
            self.age,
            self.occupation,
            self.sleep_duration,
            self.quality_of_sleep,
            self.physical_activity_level,
            self.stress_level,
            self.bmi_category,
            self.blood_pressure,
            self.heart_rate,
            self.daily_steps,
            self.sleep_disorder,
            self.id
        ))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('sleep.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sleep WHERE id=?', (self.id,))
        conn.commit()
        conn.close()

# Initialize the sleep table with data from the CSV file
def init_sleep():
    conn = sqlite3.connect('sleep.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sleep (
            id INTEGER PRIMARY KEY, 
            gender TEXT,
            age INTEGER,
            occupation TEXT,
            sleep_duration REAL,
            quality_of_sleep INTEGER,
            physical_activity_level INTEGER,
            stress_level INTEGER,
            bmi_category TEXT,
            blood_pressure TEXT,
            heart_rate INTEGER,
            daily_steps INTEGER,
            sleep_disorder TEXT
        )
    ''')

    with open(' sleep.csv', 'r', newline='') as csv_file: 
        reader = csv.DictReader(csv_file)
        for row in reader:
            sleep = Sleep(
                int(row['ID']),
                row['Gender'],
                int(row['Age']),
                row['Occupation'],
                float(row['Sleep Duration']),
                int(row['Quality of Sleep']),
                int(row['Physical Activity Level']),
                int(row['Stress Level']),
                row['BMI Category'],
                row['Blood Pressure'],
                int(row['Heart Rate']),
                int(row['Daily Steps']),
                row['Sleep Disorder']
            )
            sleep.create()

    conn.commit()
    conn.close()

# Call the function to initialize the sleep table with data from the CSV file
init_sleep()
