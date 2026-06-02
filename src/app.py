from flask import Flask

from src.routes.health import health_bp
from src.routes.user import user_bp
from src.routes.root import root_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(root_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp, url_prefix="/auth")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)