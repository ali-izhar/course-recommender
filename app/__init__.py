from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import secrets

db = SQLAlchemy()
DB_NAME="database.db"


app = Flask(__name__, template_folder = 'templates')
app.config['SECRET_KEY'] = secrets.token_hex(16)
db_path = path.join(app.instance_path, DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

# avoid circular import
from app import routes
from app.models import User, Note

def create_database(app):
    with app.app_context():
        db.create_all()
    print('Created Database!')

create_database(app)

login_manager = LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
