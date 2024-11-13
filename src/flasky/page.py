from flask import Blueprint, abort, redirect, render_template, session, url_for

app_page = Blueprint("page", __name__, url_prefix="/page")


@app_page.route("/home")
def home():
    if not session.get("user_id"):
        abort(401)
    return render_template(
        "pages/home.html",
    )
