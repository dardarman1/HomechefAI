import uuid
import os
import threading
import firebase_admin
import re
import base64
import logging
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, Blueprint, current_app
from flask_cors import CORS
from .vision_service import VisionService
from .functions import get_api_key

# Initialize Firebase
#cred = credentials.Certificate("/Users/sidkas484/Downloads/homechefai-41cf6-firebase-adminsdk-fbsvc-3dc3aaeadf.json")
#firebase_admin.initialize_app(cred)
if not firebase_admin._apps:
    firebase_admin.initialize_app()
db = firestore.client()

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend requests

sessions_bp = Blueprint('sessions', __name__)

# logger = logging.getLogger(__name__)

@sessions_bp.route('/test', methods=['GET'])
def test():
    return "OK", 200

@sessions_bp.route('/start_session', methods=['GET'])
def start_session():
    """Creates a new session with a unique ID and stores it in Firestore."""
    session_id = str(uuid.uuid4())
    db.collection("sessions").document(session_id).set({"ingredients": []})
    print(jsonify({"session_id": session_id}))
    return jsonify({"session_id": session_id})

@sessions_bp.route('/get_ingredients', methods=['POST'])
def get_ingredients():
    """Extracts ingredients from an uploaded image and stores them in Firestore."""
    """session_id = request.form.get("session_id")
    if not session_id or "image" not in request.files:
        return jsonify({"error": "Missing session_id or image"}), 400

    # Retrieve session data from Firestore
    session_ref = db.collection("sessions").document(session_id)
    session = session_ref.get()
    
    if not session.exists:
        return jsonify({"error": "Session not found"}), 404

    image_file = request.files["image"]
    temp_image_path = "/Users/sidkas484/Documents/GitHub/BoilerMake/backend/src/test.jpg"
    image_file.save(temp_image_path)

    vision_service = VisionService()
    extracted_ingredients = vision_service.extract_ingredients_from_image(temp_image_path)

    # Clean up temp file
    #if os.path.exists(temp_image_path):
    #    os.remove(temp_image_path)

    if extracted_ingredients is None:
        return jsonify({"error": "Failed to extract ingredients"}), 500

    # Update session in Firestore
    session_ref.update({"ingredients": firestore.ArrayUnion(extracted_ingredients)})
    
    return jsonify({"message": "Ingredients extracted", "ingredients": extracted_ingredients})"""
    """Extracts ingredients from an uploaded image and stores them in Firestore."""
    current_app.logger.info("🔹 Received request to /get_ingredients")
    
    data = request.get_json()
    if not data:
        current_app.logger.error("🔴 Error: No JSON data received")
        return jsonify({"error": "No JSON data received"}), 400
    # session_id = data.get("session_id")
    image_str = data.get("image")
    # current_app.logger.info(f"🔹 Session ID received: {session_id}")

    # if not session_id or not image_str:
    #     current_app.logger.error("🔴 Error: Missing session_id or image")
    #     return jsonify({"error": "Missing session_id or image"}), 400
    
    #  # Remove data URI scheme if present
    # match = re.match(r"^data:image\/[a-zA-Z]+;base64,", image_str)
    # if match:
    #     image_str = image_str[match.end():]

    # try:
    #     image_data = base64.b64decode(image_str)
    # except Exception as e:
    #     current_app.logger.error("🔴 Error: Invalid image data")
    #     return jsonify({"error": "Invalid image data", "details": str(e)}), 400
    # temp_image_path = "/tmp/test.jpg"
    # try:
    #     with open(temp_image_path, "wb") as f:
    #         f.write(image_data)
    # except Exception as e:
    #     current_app.logger.error(f"🔴 Error saving image: {e}")
    #     return jsonify({"error": "Failed to save image", "details": str(e)}), 500
    
    # Retrieve session data from Firestore
    # session_ref = db.collection("sessions").document(session_id)
    # session = session_ref.get()
    
    # if not session.exists:
    #     print(f"🔴 Error: Session {session_id} not found in Firestore")
    #     return jsonify({"error": "Session not found"}), 404

    # image_file = request.files["image"]
    # temp_image_path = "/Users/sidkas484/Documents/GitHub/BoilerMake/backend/src/test.jpg"
    
    # try:
    #     image_file.save(temp_image_path)
    #     print(f"✅ Image saved at {temp_image_path}")
    # except Exception as e:
    #     print(f"🔴 Error saving image: {e}")
    #     return jsonify({"error": "Failed to save image"}), 500

    vision_service = VisionService()
    extracted_ingredients = vision_service.extract_ingredients_from_image(image_str)

    print(f"🔹 VisionService output: {extracted_ingredients}")

    # Clean up temp file
    #if os.path.exists(temp_image_path):
    #    print(f"🗑️ Deleting temporary image file: {temp_image_path}")
    #    os.remove(temp_image_path)
    return extracted_ingredients
    # if extracted_ingredients is None:
    #     print("🔴 Error: VisionService failed to extract ingredients")
    #     return jsonify({get_api_key()}), 500
        # return jsonify({"error": "Failed to extract ingredients"}), 500

    # Update session in Firestore
    try:
        session_ref.update({"ingredients": firestore.ArrayUnion(extracted_ingredients)})
        print(f"✅ Firestore updated with ingredients: {extracted_ingredients}")
    except Exception as e:
        print(f"🔴 Error updating Firestore: {e}")
        return jsonify({"error": "Failed to update Firestore"}), 500
    
    print(jsonify({"message": "Ingredients extracted", "ingredients": extracted_ingredients}))
    return jsonify({"message": "Ingredients extracted", "ingredients": extracted_ingredients})

@sessions_bp.route('/get_recipes', methods=['POST'])
def get_recipes():
    """Fetches recipes based on stored ingredients in Firestore."""
    
    
    data = request.get_json()
    if not data:
        current_app.logger.error("🔴 Error: No JSON data received")
        return jsonify({"error": "No JSON data received"}), 400
    session_id = data.get("session_id")
    image_str = data.get("image")
    current_app.logger.info(f"🔹 Session ID received: {session_id}")

    if not session_id or not image_str:
        current_app.logger.error("🔴 Error: Missing session_id or image")
        return jsonify({"error": "Missing session_id or image"}), 400
    
    
    # Retrieve session data from Firestore
    session_ref = db.collection("sessions").document(session_id)
    session = session_ref.get()
    
    if not session.exists:
        print(f"🔴 Error: Session {session_id} not found in Firestore")
        return jsonify({"error": "Session not found"}), 404
    
    ingredients = session.to_dict().get("ingredients", [])

    if not ingredients:
        return jsonify({"error": "No ingredients found in session"}), 404

    vision_service = VisionService()
    recipes = vision_service.get_recipes_from_ingredients(ingredients)
    
    if recipes is None:
        return jsonify({"error": "Failed to fetch recipes"}), 500
    return recipes

    session_id = request.json.get("session_id")
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    session_ref = db.collection("sessions").document(session_id)
    session = session_ref.get()

    if not session.exists:
        return jsonify({"error": "Session not found"}), 404

    ingredients = session.to_dict().get("ingredients", [])

    if not ingredients:
        return jsonify({"error": "No ingredients found in session"}), 404

    # Call VisionService to get recipe suggestions
    vision_service = VisionService()
    recipes = vision_service.get_recipes_from_ingredients(ingredients)

    if recipes is None:
        return jsonify({"error": "Failed to fetch recipes"}), 500

    return jsonify({"recipes": recipes})

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 8080))
#     app.run(host='0.0.0.0', port=port)