from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_cors import CORS, cross_origin
from keys import FLASK_SESSION_KEY
from src.dbHandler import User, dbSession
from src.security.oneway import hash

app_login = Blueprint("session", __name__, url_prefix="/session")


@app_login.route("/")
def index():
    if session.get("id"):
        return redirect("/")
    else:
        return redirect(url_for("session.login"))


@app_login.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("session/login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        password = hash(password)
        dbsession = dbSession()
        user = (
            dbsession.query(User)
            .filter(User.email == email, User.password == password)
            .first()
        )
        if user:
            session["user_id"] = user.id
            return redirect(url_for("page.home"))
        else:
            flash("Error: Email or password did not match", "warning")
            return redirect(url_for("session.login"))


@app_login.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("session/sign_up.html")
    else:
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm")

        if (
            not firstName
            or not lastName
            or not phone
            or not email
            or not password
            or not confirm_pass
        ):
            flash("All fields are required.", "info")
            return redirect(url_for("session.sign_up"))

        # Check if password and confirm password match
        if password != confirm_pass:
            flash("Passwords do not match.", "info")
            return redirect(url_for("session.sign_up"))

        # Check if password meets certain criteria (e.g., minimum length)
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "info")
            return redirect(url_for("session.sign_up"))

        if len(phone) != 10:
            flash("Enter a valid phone number", "warning")
            return redirect(url_for("session.sign_up"))

        dbsession = dbSession()
        if dbsession.query(User).filter_by(email=email, phone=phone).first():
            flash("Email or phone already exists", "warning")
            return redirect(url_for("session.login"))

        try:
            user = User(firstName, lastName, email, phone, hash(password))
            dbsession.add(user)
            dbsession.commit()
            flash("Successfully registered", "success")
        except Exception as e:
            flash("Internal server error", "warning")
            print(e)

        return redirect(url_for("session.index"))


@app_login.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("session.login"))
