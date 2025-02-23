from flask import Flask
from flask_cors import CORS
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    from backend.src import sessions
    from backend.src.vision_service import VisionService

    return app 