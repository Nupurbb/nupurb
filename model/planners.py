from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, note, image):
        self.note = note
        self.image = image

    def __repr__(self):
        return f"Post(id={self.id}, note={self.note}, image={self.image}, userID={self.userID})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        with open(file, 'rb') as file_text:
            file_read = file_text.read()
            file_encode = base64.encodebytes(file_read).decode('utf-8')

        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": file_encode
        }
