import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class Fitness(db.Model):
    __tablename__ = 'exercises'

    _exerciseName = db.Column(db.String(255), primary_key=True)
    _calories_burned = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, exerciseName, calories_burned):
        self._exerciseName = exerciseName
        self._calories_burned = calories_burned

    @property
    def exerciseName(self):
        return self._exerciseName
    
    @exerciseName.setter
    def exerciseName(self, exerciseName):
        self._exerciseName = exerciseName
    
    @property
    def calories_burned(self):
        return self._calories_burned
    
    @calories_burned.setter
    def calories_burned(self, calories_burned):
        self._calories_burned = calories_burned
          
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
            "exerciseName": self.exerciseName,
            "calories_burned": self.calories_burned
        }

    def update(self, exerciseName="", calories_burned=0):
        if len(exerciseName) > 0:
            self.exerciseName = exerciseName
        if calories_burned >= 0:
            self.calories_burned = calories_burned
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

"""Database Creation and Testing """

def initFitnessy():
    with app.app_context():
        """Create database and tables"""
        db.create_all()

        fitnessytoadd = []
        try:
            with open(r'fitness.json','r') as json_file:
                data = json.load(json_file)
        except Exception as error:
            print("failed")

        for item in data:
            e_toadd = Fitness(exerciseName=item['activity'],calories_burned=item['calories_burned_per_hour']
            )
            fitnessytoadd.append(e_toadd)

        """Builds sample exercise data"""
        for e in fitnessytoadd:
            try:
                e.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate or error: {e.fitnessyName}")
