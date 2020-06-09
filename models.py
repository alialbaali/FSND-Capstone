from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String

from db import db

# Models

''' Movie Model '''


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(db.String, unique=True, nullable=False)
    release_date = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, title, release_date=datetime.now()):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f"( Movie {self.id} {self.title} {self.release_date} )"

    # Insert Movie into the database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update Movie in the database
    def update(self):
        db.session.commit()

    # Delete Movie from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


''' Actor Model '''


class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(128), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(12), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"( Actor {self.id} {self.name} {self.age} {self.gender} )"

    # Insert Actor into the database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update Actor in the database
    def update(self):
        db.session.commit()

    # Delete Actor from the database database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
