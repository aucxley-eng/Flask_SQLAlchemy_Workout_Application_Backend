from flask import Flask, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from .models import db
from .routes.workout_routes import workout_bp
from .routes.exercise_routes import exercise_bp

def create_app():
    """
    App Factory: Creates and configures the Flask application.
    Initializes extensions and registers blueprints.
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Global Error Handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handle Marshmallow validation errors."""
        return jsonify(errors=e.messages), 400

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        """Handle SQLAlchemy model validation errors."""
        return jsonify(errors={"message": str(e)}), 400

    # Register Blueprints (Modular Routes)
    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)

    return app
