from flask import Blueprint, render_template

app_index = Blueprint("index", __name__)


@app_index.route("/")
def index():
    return render_template("index.html")


@app_index.route("/chat")
def chat():
    return render_template("components/chat.html")
