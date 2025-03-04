from src.dbModels import dbSession, User
from src.utils.pre_loader import config
from src.flasky.session import app_session
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from os import environ
from src.flasky.fetch.user import app_fetch
import logging


class CustomLogger(logging.Logger):
    """Custom logger that automatically includes exc_info for all log levels based on a global flag."""

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.enable_traceback = config.getboolean(
            'application', 'enable_traceback')

    def _log_with_exc_info(self, level, msg, args, exc_info, **kwargs):
        """Helper method to add exc_info automatically if not explicitly set."""
        if exc_info is None:
            exc_info = self.enable_traceback
        super()._log(level, msg, args, exc_info=exc_info, **kwargs)

    def debug(self, msg, *args, exc_info=None, **kwargs):
        self._log_with_exc_info(logging.DEBUG, msg, args, exc_info, **kwargs)

    def info(self, msg, *args, exc_info=None, **kwargs):
        self._log_with_exc_info(logging.INFO, msg, args, exc_info, **kwargs)

    def warning(self, msg, *args, exc_info=None, **kwargs):
        self._log_with_exc_info(logging.WARNING, msg, args, exc_info, **kwargs)

    def error(self, msg, *args, exc_info=None, **kwargs):
        self._log_with_exc_info(logging.ERROR, msg, args, exc_info, **kwargs)

    def critical(self, msg, *args, exc_info=None, **kwargs):
        self._log_with_exc_info(logging.CRITICAL, msg,
                                args, exc_info, **kwargs)


# Register the custom logger
logging.setLoggerClass(CustomLogger)
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.NOTSET,
    # Format only up to seconds
    format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


def create_app():
    """
    Factory function to create and configure the Flask app.
    Sets up JWT, OAuth, and registers blueprints.
    """
    app = Flask(__name__)
    app.secret_key = environ.get("FLASK_SESSION_KEY")
    if not app.secret_key:
        raise ValueError("FLASK_SESSION_KEY environment variable is missing.")

    # Enable CORS with credentials support
    CORS(app, supports_credentials=True)

    # Configure JWT
    app.config["JWT_SECRET_KEY"] = app.secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        """Return the identity of the user for JWT token creation."""
        return identity

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Fetch the user from the database based on the JWT identity."""
        identity = jwt_data["sub"]
        with dbSession() as dbsession:
            user = dbsession.query(User).filter(
                User.id == identity).one_or_none()
            if not user:
                return None
        return user

    # Register Flask Blueprints
    app.register_blueprint(app_session)
    app.register_blueprint(app_fetch)

    # Configure OAuth
    app.oauth = OAuth(app)

    # Register Google OAuth
    app.oauth.register(
        name="google",
        client_id=environ.get("GOOGLE_CLIENT_ID"),
        client_secret=environ.get("GOOGLE_CLIENT_SECRET"),
        access_token_url="https://accounts.google.com/o/oauth2/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        client_kwargs={"scope": "openid email profile"},
    )

    # Register Facebook OAuth
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
