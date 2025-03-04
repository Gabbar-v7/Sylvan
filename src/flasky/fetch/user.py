from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from src.dbModels import User, dbSession

app_fetch = Blueprint("fetch", __name__, url_prefix="/fetch/user")


def get_complete_user(user_id: int) -> dict:
    """
    Fetch complete user details including related entities (details, medications, preferences).
    """
    with dbSession() as dbsession:
        user = dbsession.query(User).options(
            joinedload(User.preferences)
        ).filter(User.id == user_id).one_or_none()
    return user.as_dict() if user else {}


@app_fetch.route("/")
@jwt_required()
def fetch_user():
    """
    Fetch and return the complete details of the currently authenticated user.
    """
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    return jsonify(get_complete_user(user_id)), 200
