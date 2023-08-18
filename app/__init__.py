from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    Session(app)
    db.init_app(app)
    login_manager.init_app(app)

    from . import models

    from .views import auth_bp, main_bp, task_bp, user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('You must be logged in to view this page.')
        return redirect(url_for('auth.login'))

    # Create the user table before the first request
    @app.before_first_request
    def create_tables():
        db.create_all()

    return app