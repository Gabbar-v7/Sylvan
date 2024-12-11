from flask import Flask
from flask_login import LoginManager

from src.dbModels import dbSession, User
from src.flasky.session import app_session
from src.flasky.page import app_page
from src.flasky.errors import app_error
from src.flasky.index import app_index
from keys import FLASK_SESSION_KEY


def create_app():
    app = Flask(__name__)
    app.secret_key = FLASK_SESSION_KEY

    # Register blueprints
    app.register_blueprint(app_session)
    app.register_blueprint(app_page)
    app.register_blueprint(app_error)
    app.register_blueprint(app_index)

    # Flask-Login initialization
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Configure the login view for Flask-Login
    login_manager.login_view = "session.login"

    @login_manager.user_loader
    def load_user(user_id):
        # Query the database for a user by ID
        with dbSession() as dbsession:
            user = dbsession.query(User).filter(User.id == user_id).first()
        return user

    return app
