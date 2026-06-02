from src.db.client import db

def get_users():
    return db.user.find_many()


def new_user(data):

    try:
        if not data.get("email") or not data.get("password") or not data.get("username"):
            return {"error": "Missing required information"}, 400

        user = db.user.find_first(
            where={
                "OR": [
                    {"email": data["email"]},
                    {"username": data["username"]}
                ]
            }
        )

        if user:
            if user.email == data["email"]:
                return {"error": "This email is already registered"}, 409

            if user.username == data["username"]:
                return {"error": "This username is already taken"}, 409

        new_user = db.user.create(
            data={
                "email": data["email"].strip().lower(),
                "username": data["username"]
            }
        )

        return new_user, 201

    except Exception as e:
        return {"error": str(e)}, 500