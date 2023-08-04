import json
from flask_login import UserMixin
from .. import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    favorite_courses = db.relationship('FavoriteCourse', backref='user', lazy=True)

    @property
    def is_active(self):
        return True
    
    @property
    def courses_list(self):
        return json.loads(self.courses) if self.courses else []

    @courses_list.setter
    def courses_list(self, value):
        self.courses = json.dumps(value)

    def __repr__(self):
        return f'{self.email}'


class FavoriteCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_name = db.Column(db.String(255))
    course_url = db.Column(db.String(255))

    def __repr__(self):
        return f'{self.course_name}'


class CourseEmbedding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255))
    embedding = db.Column(db.Text, nullable=False)  # Text can store large amounts of string data

    @property
    def embedding_list(self):
        """Return the deserialized version of the embedding."""
        return json.loads(self.embedding)

    @embedding_list.setter
    def embedding_list(self, value):
        """Automatically serialize the embedding before storing it."""
        self.embedding = json.dumps(value)

    def __repr__(self):
        return f'{self.course_name}'