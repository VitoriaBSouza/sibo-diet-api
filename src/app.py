from flask import Flask

from src.routes.auth import auth_bp
from src.routes.health import health_bp
from src.routes.root import root_bp


def create_app():
    print(">>> create_app CALLED")
    app = Flask(__name__)

    app.register_blueprint(root_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    print(">>> AUTH MODULE LOADED")
    return app