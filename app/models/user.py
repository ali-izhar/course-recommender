import json
from flask_login import UserMixin
from .. import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    @property
    def is_active(self):
        return True

    def __repr__(self):
        return f'<User {self.email}>'

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
        return f'<CourseEmbedding {self.course_name}>'