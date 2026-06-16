from src.app import create_app
from src.db.client import db

def main():
    db.connect()   
    app = create_app()
    app.run(host="0.0.0.0", port=5001)

if __name__ == "__main__":
    main()