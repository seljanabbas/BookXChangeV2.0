from flask import Flask
import os

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_pyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.py'))

    # Import and register blueprints (if any)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
