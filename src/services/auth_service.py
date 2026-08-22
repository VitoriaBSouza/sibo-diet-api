from src.db.client import db
from supabase import create_client
from prisma import Prisma
import os
import logging
import traceback
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

supabase_admin = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


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
    try:
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        if not email or not username or not password:
            return {"error": "Missing fields"}, 400

        email = email.strip().lower()

        # 1. Supabase
        auth = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if not auth.user:
            return {"error": "Supabase signup failed"}, 400

        user_id = auth.user.id

        # 2. Prisma
        async def create_user():
            prisma = Prisma()

            await prisma.connect()

            try:
                return await prisma.user.create(
                    data={
                        "email": email,
                        "username": username,
                        "supabaseId": user_id
                    }
                )
            finally:
                await prisma.disconnect()

        user_db = asyncio.run(create_user())

        return {
            "message": "User created",
            "user": {
                "id": user_db.id,
                "email": user_db.email,
                "username": user_db.username,
                "supabaseId": user_db.supabaseId
            }
        }, 201

    except Exception as e:
        logger.error("SIGNUP FAILED")
        logger.error(traceback.format_exc())

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

def delete_account(access_token):
    try:
        # 1. Get authenticated user from token
        auth = supabase.auth.get_user(access_token)

        if not auth.user:
            return {"error": "Invalid token"}, 401

        user_id = auth.user.id

        # 2. Delete and verify in Prisma
        async def delete_from_prisma():
            prisma = Prisma()

            await prisma.connect()

            try:
                await prisma.user.delete(
                    where={
                        "supabaseId": user_id
                    }
                )

                # Confirm deletion
                user_exists = await prisma.user.find_first(
                    where={
                        "supabaseId": user_id
                    }
                )

                return user_exists

            finally:
                await prisma.disconnect()

        user_exists = asyncio.run(delete_from_prisma())

        # 3. Confirm Prisma deletion
        if user_exists:
            return {
                "error": "User was not deleted from database"
            }, 500

        # 4. Only now delete from Supabase
        supabase_admin.auth.admin.delete_user(user_id)

        return {
            "message": "Account deleted"
        }, 200

    except Exception as e:
        logger.error("DELETE ACCOUNT FAILED")
        logger.error(traceback.format_exc())

        return {"error": str(e)}, 500