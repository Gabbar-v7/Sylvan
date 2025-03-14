from os import environ
from prometheus_flask_exporter import PrometheusMetrics
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os.path import abspath, join, dirname

root_path = abspath(join(dirname(__file__), "../../"))

metrics = PrometheusMetrics.for_app_factory()
jwt = JWTManager()
oauth = OAuth()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20000/day", "20/minute"],
    storage_uri=environ.get("LIMITER_DATABASE_URI"),
)
