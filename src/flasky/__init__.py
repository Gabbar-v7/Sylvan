from os import environ
from os.path import abspath, dirname, join

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session, url_for
from flask_cors import CORS
from flask_login import LoginManager

from src.dbModels import User, dbSession
from src.flasky.errors import app_error
from src.flasky.index import app_index
from src.flasky.page import app_page
from src.flasky.session import app_session


def create_app():

    root_path = abspath(join(dirname(__file__), "../../"))

    app = Flask(
        __name__,
        template_folder=join(root_path, "templates"),
        static_folder=join(root_path, "static"),
    )
    app.secret_key = environ.get("FLASK_SESSION_KEY")
    CORS(app)

    # Register Flask Blueprints
    app.register_blueprint(app_session)
    app.register_blueprint(app_error)
    app.register_blueprint(app_index)
    app.register_blueprint(app_page)

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

    # OAuth configuration and registration
    app.oauth = OAuth(app)
    app.oauth.register(
        name="google",
        client_id=environ.get("GOOGLE_CLIENT_ID"),
        client_secret=environ.get("GOOGLE_CLIENT_SECRET"),
        access_token_url="https://accounts.google.com/o/oauth2/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",  # Include the JWK URI
        client_kwargs={"scope": "openid email profile"},
    )
    # Register Facebook OAuth in Flask
    app.oauth.register(
        name="facebook",
        client_id=environ.get("FACEBOOK_CLIENT_ID"),
        client_secret=environ.get("FACEBOOK_CLIENT_SECRET"),
        access_token_url="https://graph.facebook.com/oauth/access_token",
        authorize_url="https://www.facebook.com/dialog/oauth",
        api_base_url="https://graph.facebook.com/v12.0/",
        client_kwargs={"scope": "email public_profile"},
    )

    return app
