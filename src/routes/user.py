from flask import Blueprint, jsonify, request
from src.services.user_service import get_users, new_user

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def users():
    return jsonify({
        "users": [user.serialize() for user in get_users()],
        "success": True
    }), 200


@user_bp.route("/signup", methods=["POST"])
def create_user():
    data = request.get_json()
    result, status = new_user(data)

    return jsonify(result), status