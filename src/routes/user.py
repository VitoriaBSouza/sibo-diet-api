from flask import Blueprint, jsonify
from src.services.user_service import get_users

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def users():
    return jsonify({
        "users": [user.serialize() for user in get_users()],
        "success": True
    }), 200
