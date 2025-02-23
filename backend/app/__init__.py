from flask import Flask
from flask_cors import CORS
from config import Config
import os
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,  # Set logging level to DEBUG
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Now you can use logging.debug(), logging.info(), etc.
    app.logger.debug("Flask app initialized in debug mode.")
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from backend.src.sessions import sessions_bp
    app.register_blueprint(sessions_bp)

    return app 