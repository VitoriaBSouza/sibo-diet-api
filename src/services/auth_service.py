from src.db.client import db
from supabase import create_client
import os
import logging
import traceback

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


# def signup(data):
#     logger.debug("SIGNUP ROUTE HIT")

#     try:
#         email = data.get("email")
#         password = data.get("password")
#         username = data.get("username")

#         if not email or not password or not username:
#             return {"error": "Missing fields"}, 400

#         email = email.strip().lower()

#         # -------------------------
#         # 1. SUPABASE SIGNUP
#         # -------------------------
#         auth = supabase.auth.sign_up({
#             "email": email,
#             "password": password,
#             "options": {
#                 "data": {
#                     "username": username
#                 }
#             }
#         })

#         logger.debug(f"SUPABASE RESPONSE: {auth}")

#         user = auth.user

#         if not user:
#             return {
#                 "error": "Supabase did not return user (email confirmation or duplicate)"
#             }, 400

#         # -------------------------
#         # 2. CHECK EXISTING USER (PREVENT 500)
#         # -------------------------
#         existing = db.user.find_first(
#             where={
#                 "OR": [
#                     {"email": email},
#                     {"username": username},
#                     {"supabaseId": user.id}
#                 ]
#             }
#         )

#         if existing:
#             logger.debug("USER ALREADY EXISTS → RETURN EXISTING")
#             return {
#                 "message": "User already exists",
#                 "user": existing
#             }, 200

#         # -------------------------
#         # 3. CREATE USER IN PRISMA
#         # -------------------------
#         logger.debug("CREATING USER IN PRISMA")

#         user_db = db.user.create(
#             data={
#                 "email": email,
#                 "username": username,
#                 "supabaseId": user.id
#             }
#         )

#         return {
#             "message": "User created",
#             "user": user_db
#         }, 201

#     except Exception as e:
#         logger.error("SIGNUP FAILED")
#         logger.error(traceback.format_exc())

#         return {"error": str(e)}, 500

def signup(data):
    print(">>> SIGNUP HIT")

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    print("DATA:", email, username)

    try:
        auth = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        print("SUPABASE DONE:", auth)

        # ❗ STOP HERE FIRST (REMOVE PRISMA TEMPORARILY)
        return {
            "message": "Supabase works",
            "user": str(auth.user)
        }, 200

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}, 500

def login(data):
    try:
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Missing fields"}, 400

        email = email.strip().lower()

        auth = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not auth.session:
            return {"error": "Invalid credentials"}, 401

        session = auth.session

        return {
            "message": "Login successful",
            "access_token": str(session.access_token),
            "refresh_token": str(session.refresh_token),
            "user": {
                "id": str(session.user.id),
                "email": str(session.user.email)
            }
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500