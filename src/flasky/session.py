from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user, user_logged_in
from sqlalchemy.exc import IntegrityError

from src.dbModels import User, dbSession
from src.security.oneway import generate_secure_hash

app_session = Blueprint("session", __name__, url_prefix="/session")


@app_session.route("/")
def index():
    return redirect(url_for("page.home" if user_logged_in else "session.login"))


@app_session.route("/login", methods={"GET", "POST"})
def login():
    if request.method == "GET":
        return render_template("session/login.html")

    email = request.form.get("email")
    password = generate_secure_hash(request.form.get("password"))
    try:
        with dbSession() as dbsession:
            user = (
                dbsession.query(User)
                .filter(User.email == email, User.password == password)
                .first()
            )
        if user:
            login_user(user)
            flash("Successfully logged in", "success")
            return redirect(url_for("page.home"))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for("session.login"))
    except Exception as e:
        current_app.logger.error(f"Login failed: {str(e)}")
        flash("Internal server error", "error")
        return redirect(url_for("session.login"))


@app_session.route("/register", methods={"GET", "POST"})
def register():
    if request.method == "GET":
        return render_template("session/register.html")

    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    try:
        user = User(firstName, lastName, "user", email, phone, password)
        with dbSession() as dbsession:
            dbsession.add(user)
            dbsession.commit()
        flash("Successfully registered", "success")
        return redirect(url_for("session.login"))
    except IntegrityError as e:
        current_app.logger.error(f"Registration failed: {str(e)}")
        if "email" in str(e.orig):
            flash("Email already exists", "error")
        elif "phone" in str(e.orig):
            flash("Phone number already exists", "error")
        else:
            flash("Data integrity error", "error")
        return redirect(url_for("session.login"))
    except Exception as e:
        current_app.logger.error(f"Registration failed: {str(e)}")
        flash("Internal server error", "error")
        return redirect(url_for("session.login"))


@app_session.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        flash("Logout successful", "success")
        return redirect(url_for("session.login"))
    except Exception as e:
        current_app.logger.error(f"Logout failed: {str(e)}")
        flash("Logout failed", "error")
        return redirect(url_for("session.index"))


@app_session.route("/oauth/register/<string:platform>")
def oauth_register(platform: str):
    oauth_client = getattr(current_app.oauth, platform, None)

    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400

    try:
        return oauth_client.authorize_redirect(
            url_for(f"session.callback_register", platform=platform, _external=True)
        )
    except Exception as e:
        current_app.logger.error(f"OAuth registration failed: {str(e)}")
        return jsonify({"msg": "OAuth authorization failed"}), 500


@app_session.route("/oauth/register/callback/<string:platform>")
def callback_register(platform: str):
    oauth_client = getattr(current_app.oauth, platform, None)
    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400

    try:
        token = oauth_client.authorize_access_token()
        user_info = fetch_user_info(oauth_client, platform)

        email = user_info["email"]
        first_name = user_info["first_name"]
        last_name = user_info["last_name"]

        user = User(first_name, last_name, "user", email, "", "")
        with dbSession() as dbsession:
            dbsession.add(user)
            dbsession.commit()
        return jsonify({"msg": "User created successfully"}), 201
    except IntegrityError as e:
        current_app.logger.error(f"OAuth registration failed: {str(e)}")
        if "email" in str(e.orig):
            return jsonify({"msg": "Email already exists"}), 409
    except Exception as e:
        current_app.logger.error(f"OAuth registration failed: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500


@app_session.route("/oauth/login/<string:platform>")
def oauth_login(platform: str):
    oauth_client = getattr(current_app.oauth, platform, None)
    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400

    try:
        return oauth_client.authorize_redirect(
            url_for(f"session.callback_login", platform=platform, _external=True)
        )
    except Exception as e:
        current_app.logger.error(f"OAuth sign-in failed: {str(e)}")
        return jsonify({"msg": "OAuth authorization failed"}), 500


@app_session.route("/oauth/login/callback/<string:platform>")
def callback_login(platform: str):
    oauth_client = getattr(current_app.oauth, platform, None)
    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400

    try:
        token = oauth_client.authorize_access_token()
        user_info = fetch_user_info(oauth_client, platform)

        email = user_info["email"]
        with dbSession() as dbsession:
            user = dbsession.query(User).filter(User.email == email).first()
            if not user:
                return jsonify({"msg": "User not found"}), 404
            login_user(user)
            response = user.as_dict()
            response["msg"] = "Login successful"
            return jsonify(response), 200
    except Exception as e:
        current_app.logger.error(f"OAuth sign-in failed: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500


def fetch_user_info(oauth_client, platform):
    """Helper function to fetch user information based on the platform."""
    if platform == "google":
        user_info = oauth_client.get("userinfo").json()
        return {
            "email": user_info["email"],
            "first_name": user_info.get("given_name", ""),
            "last_name": user_info.get("family_name", ""),
        }
    elif platform == "github":
        user_info = oauth_client.get("user").json()
        return {
            "email": user_info["email"],
            "first_name": user_info["name"],
            "last_name": "",
        }
    elif platform == "linkedin":
        user_info = oauth_client.get(
            "me?projection=(id,localizedFirstName,localizedLastName)"
        ).json()
        email_info = oauth_client.get(
            "emailAddress?q=members&projection=(elements*(handle~))"
        ).json()
        email = email_info["elements"][0]["handle~"]["emailAddress"]
        return {
            "email": email,
            "first_name": user_info["localizedFirstName"],
            "last_name": user_info["localizedLastName"],
        }
    raise ValueError(f"Unsupported platform: {platform}")
