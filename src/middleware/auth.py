import requests
from functools import wraps
from flask import request, jsonify, g

SUPABASE_URL = "https://frslnnszwxmdqqbqhuin.supabase.co"

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing token"}), 401

        token = auth_header.replace("Bearer ", "")

        res = requests.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={"Authorization": f"Bearer {token}"}
        )

        if res.status_code != 200:
            return jsonify({
                "error": "Invalid token",
                "detail": res.text
            }), 401

        g.user = res.json()

        return f(*args, **kwargs)

    return wrapper