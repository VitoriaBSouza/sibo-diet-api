from flask import Blueprint, request, jsonify
from src.services.auth_service import signup, login, delete_account

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    data = request.get_json()
    result, status = signup(data)
    return jsonify(result), status


@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()
    result, status = login(data)
    return jsonify(result), status

@auth_bp.route("/delete", methods=["DELETE"])
def delete_account_route():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "error": "Missing authorization token"
        }), 401

    if not auth_header.startswith("Bearer "):
        return jsonify({
            "error": "Invalid authorization format"
        }), 401

    access_token = auth_header.split(" ", 1)[1]

    result, status = delete_account(access_token)

    return jsonify(result), status