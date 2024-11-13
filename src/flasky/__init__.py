from flask import Flask

from src.dbHandler import dbSession
from src.flasky.session import app_login
from src.flasky.page import app_page
from src.flasky.errors import app_error
from src.flasky.index import app_index
from keys import FLASK_SESSION_KEY

app = Flask(__name__)
app.secret_key = FLASK_SESSION_KEY
app.register_blueprint(app_login)
app.register_blueprint(app_page)
app.register_blueprint(app_error)
app.register_blueprint(app_index)
