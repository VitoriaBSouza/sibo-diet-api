from flask import Blueprint, request, jsonify
from src.services.auth_service import signup, login

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