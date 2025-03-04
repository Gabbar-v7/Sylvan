from flask import Blueprint, current_app, jsonify, make_response, redirect, request, session, abort, url_for
from sqlalchemy.exc import IntegrityError
from src.dbModels import User, dbSession
from src.security.oneway import generate_secure_hash
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from .fetch.user import get_complete_user
from src.utils.pre_loader import config

# Create a Blueprint for session-related routes
app_session = Blueprint("session", __name__, url_prefix="/session")


@app_session.route("/login", methods=["POST"])
def login():
    """
    Handle user login.
    Expects email and password in the form data.
    Returns user details, access token, and refresh token if credentials are valid.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Hash the password for comparison
    password_hash = generate_secure_hash(password)

    try:
        with dbSession() as dbsession:
            user = dbsession.query(User).filter(
                User.email == email, User.password == password_hash
            ).first()

        if user:
            user_details = get_complete_user(
                user.id)  # Fetch complete user details
            access_token = create_access_token(
                identity=user_details.get('id'), fresh=True)
            refresh_token = create_refresh_token(
                identity=user_details.get('id'))
            return jsonify(user=user_details, access_token=access_token, refresh_token=refresh_token), 200
        else:
            return jsonify({"msg": "Invalid credentials"}), 401
    except Exception as e:
        current_app.logger.error(f"Login failed: {str(e)}", exc_info=True)
        return jsonify({"msg": "Internal server error"}), 500


@app_session.route("/register", methods=["POST"])
def register():
    """
    Handle user registration.
    Expects firstName, lastName, email, phone, and password in the form data.
    Returns user details, access token, and refresh token upon successful registration.
    """
    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    if not all([first_name, last_name, email, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    # Hash the password before storing
    password_hash = generate_secure_hash(password)

    try:
        user = User(first_name, last_name, "patient",
                    email, phone, password_hash)
        with dbSession() as dbsession:
            dbsession.add(user)
            dbsession.commit()
            dbsession.refresh(user)

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(user=user.as_dict(), access_token=access_token, refresh_token=refresh_token), 201
    except IntegrityError as e:
        current_app.logger.error(
            f"Registration failed: {str(e)}", exc_info=True)
        if "email" in str(e.orig):
            return jsonify({"msg": "Email already exists"}), 409
        elif "phone" in str(e.orig):
            return jsonify({"msg": "Phone number already exists"}), 409
        else:
            return jsonify({"msg": "Data integrity error"}), 400
    except Exception as e:
        current_app.logger.error(
            f"Registration failed: {str(e)}", exc_info=True)
        return jsonify({"msg": "Internal server error"}), 500


@app_session.route("/get_token")
def get_token():
    """
    Retrieve the access and refresh tokens from the session.
    Returns user details and tokens if they exist in the session.
    """
    access_token = request.cookies.get('access_token')

    if not access_token:
        return jsonify({"msg": "Token not found"}), 404

    try:
        decoded_token = decode_token(access_token)
        user_id = decoded_token.get("sub")  # "sub" contains the identity
        user = get_complete_user(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user_id)
        response = make_response(jsonify(
            {'user': user, 'access_token': access_token, 'refresh_token': refresh_token}))
        response.delete_cookie('access_token')
        return response, 200
    except Exception as e:
        current_app.logger.error(
            f"Token retrieval failed: {str(e)}")
        return jsonify({"msg": "Invalid token"}), 400


@app_session.route("/oauth/register/<string:platform>")
def oauth_register(platform: str):
    """
    Initiate OAuth registration for the specified platform.
    Redirects to the platform's authorization page.
    """
    oauth_client = getattr(current_app.oauth, platform, None)
    next_page = request.args.get("next")
    error_page = request.args.get("error_page")

    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400
    elif not (next_page and error_page):
        return jsonify({"msg": "Missing success and fail redirect URLs"}), 400

    try:
        session["nextPage"] = next_page
        session["errorPage"] = error_page
        return oauth_client.authorize_redirect(url_for("session.callback_register", platform=platform, _external=True))
    except Exception as e:
        current_app.logger.error(
            f"OAuth registration failed: {str(e)}")
        return redirect(error_page), 500


@app_session.route("/oauth/register/callback/<string:platform>")
def callback_register(platform: str):
    """
    Handle the callback from the OAuth provider after registration.
    Creates a new user with the information provided by the OAuth provider.
    """
    oauth_client = getattr(current_app.oauth, platform, None)
    next_page = session.get("nextPage")
    error_page = session.get("errorPage")

    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400
    elif not (next_page and error_page ):
        return jsonify({"msg": "Missing session data"}), 400

    try:
        oauth_client.authorize_access_token()
        user_info = fetch_user_info(oauth_client, platform)

        if not user_info.get("email") or not user_info.get("first_name"):
            return jsonify({"msg": "Incomplete user info from OAuth provider"}), 400

        email = user_info["email"]
        first_name = user_info["first_name"]
        last_name = user_info.get("last_name", "")

        user = User(first_name, last_name, "patient",
                    email, "", "")  # Create a new user
        with dbSession() as dbsession:
            dbsession.add(user)
            dbsession.commit()
            dbsession.refresh(user)

        response = make_response(redirect(next_page))
        response.set_cookie(
            'access_token', create_access_token(identity=str(user.id)), httponly=False,
            secure=True, samesite="None")
        return response, 200
    except IntegrityError:
        return jsonify({"msg": "User already exists"}), 409
    except Exception as e:
        current_app.logger.error(
            f"OAuth registration failed: {str(e)}", exc_info=True)
        return redirect(error_page), 400


@app_session.route("/oauth/login/<string:platform>")
def oauth_login(platform: str):
    """
    Initiate OAuth login for the specified platform.
    Redirects to the platform's authorization page.
    """
    oauth_client = getattr(current_app.oauth, platform, None)
    next_page = request.args.get("next")
    error_page = request.args.get("error_page")

    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400
    elif not (next_page and error_page):
        return jsonify({"msg": "Missing success and fail redirect URLs"}), 400

    try:
        session['nextPage'] = next_page
        session['errorPage'] = error_page
        return oauth_client.authorize_redirect(url_for("session.callback_login", platform=platform, _external=True))
    except Exception as e:
        current_app.logger.error(
            f"OAuth login failed: {str(e)}", exc_info=True)
        return jsonify({"msg": "OAuth authorization failed"}), 500


@app_session.route("/oauth/login/callback/<string:platform>")
def callback_login(platform: str):
    """
    Handle the callback from the OAuth provider after login.
    Logs the user in if they exist, otherwise redirects to the error page.
    """
    oauth_client = getattr(current_app.oauth, platform, None)
    next_page = session.get("nextPage")
    error_page = session.get("errorPage")

    if oauth_client is None:
        return jsonify({"msg": f"Unsupported platform: {platform}"}), 400
    elif not (next_page and error_page):
        return jsonify({"msg": "Missing session data"}), 400

    try:
        oauth_client.authorize_access_token()
        user_info = fetch_user_info(oauth_client, platform)
        email = user_info["email"]

        with dbSession() as dbsession:
            user = dbsession.query(User).filter(User.email == email).first()
            if not user:
                return redirect(error_page), 404

        response = make_response(redirect(next_page))
        response.set_cookie(
            'access_token', create_access_token(identity=str(user.id)), httponly=False,
            secure=True, samesite="None")
        return response, 200
    except Exception as e:
        current_app.logger.error(
            f"OAuth login failed: {str(e)}", exc_info=True)
        return redirect(error_page), 500


def fetch_user_info(oauth_client, platform):
    """
    Helper function to fetch user information based on the platform.
    Currently supports Google OAuth.
    """
    if platform == "google":
        user_info = oauth_client.get("userinfo").json()
        return {
            "email": user_info["email"],
            "first_name": user_info.get("given_name", ""),
            "last_name": user_info.get("family_name", ""),
        }
    raise ValueError(f"Unsupported platform: {platform}")
