from flask import Blueprint, abort, redirect, render_template, session, url_for
from flask_login import login_required


app_page = Blueprint("page", __name__, url_prefix="/page")


@app_page.route("/home")
@login_required
def home():
    return render_template(
        "pages/home.html",
    )
