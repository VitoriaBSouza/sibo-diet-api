from src.db.client import db

def get_users():
    return db.user.find_many()
