import uuid
import threading
import os
import json
from flask import Flask, request, jsonify
from google import genai
from google.genai.types import GenerateContentConfig
from PIL import Image
from typing import List, Optional
from functions import get_api_key

app = Flask(__name__)

# Global in-memory session store.
session_store = {}
session_lock = threading.Lock()

class VisionService:
    def __init__(self):
        api_key_data = get_api_key()
        if api_key_data == -1:
            raise ValueError("Failed to get API key")
        self.client = genai.Client(api_key=api_key_data['api_key'])
        
    def extract_ingredients_from_image(self, image_path: str) -> Optional[List[str]]:
        """
        Extracts ingredients from an image using Gemini Vision.
        """
        try:
            image = Image.open(image_path)
            
            prompt = """
            List all the ingredients in the image. Be as specific about ingredient type as possible 
            while remaining accurate. Avoid duplicates. Output them as a JSON array.
            
            Example:
            ["Greek Yogurt", "Bananas", "Orange", "Red Apple", "Ground Beef"]
            """
            
            config = GenerateContentConfig(
                temperature=0,
                max_output_tokens=2048
            )
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, image],
                config=config
            )
            
            # Extract JSON array from response.
            json_str = response.text[response.text.find("["):response.text.rfind("]") + 1]
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

@app.route('/start_session', methods=['POST'])
def start_session():
    """
    Create a new session by generating a unique session_id.
    """
    session_id = str(uuid.uuid4())
    with session_lock:
        session_store[session_id] = []
    return jsonify({"session_id": session_id})

@app.route('/get_ingredients', methods=['POST'])
def get_ingredients():
    """
    Extract ingredients from an uploaded image and add them to the session.
    Expects multipart/form-data with 'session_id' and 'image' file.
    """
    session_id = request.form.get("session_id")
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    if 'image' not in request.files:
        return jsonify({"error": "Missing image file"}), 400

    image_file = request.files['image']
    # Save the uploaded image to a temporary file.
    temp_image_path = f"/tmp/{session_id}_{image_file.filename}"
    image_file.save(temp_image_path)
    
    # Process the image to extract ingredients.
    vision_service = VisionService()
    extracted_ingredients = vision_service.extract_ingredients_from_image(temp_image_path)
    
    # Clean up the temporary file.
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)
    
    if extracted_ingredients is None:
        return jsonify({"error": "Failed to extract ingredients from image"}), 500

    with session_lock:
        if session_id not in session_store:
            return jsonify({"error": "Session not found"}), 404
        # Add the extracted ingredients to the session's list.
        session_store[session_id].extend(extracted_ingredients)
        current_ingredients = session_store[session_id]
    
    return jsonify({
        "message": "Ingredients extracted and added",
        "ingredients": current_ingredients
    })

if __name__ == '__main__':
    app.run(debug=True)