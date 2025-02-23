import google.generativeai as genai
from PIL import Image
import json
import os
import io
from functions import get_api_key

class VisionService:
    def __init__(self):
        """Initialize Google Gemini Vision AI Client."""
        api_key_data = get_api_key()

        print(f"🔹 Loaded API Key: {api_key_data}")  # Debugging

        if api_key_data == -1:
            raise ValueError("Failed to get API key")

        genai.configure(api_key=api_key_data)
        self.client = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Or "gemini-1.5-pro"
        print(f"✅ Successfully initialized Gemini Model: {self.client}")

    def extract_ingredients_from_image(self, image_path: str):
        """
        Extracts ingredients from an image using Gemini Vision AI.
        :param image_path: Path to the image file
        :return: List of extracted ingredients or None if an error occurs
        """
        try:
            print(f"🔹 Processing image: {image_path}")

            # Ensure file exists
            if not os.path.exists(image_path):
                print(f"🔴 ERROR: File does NOT exist: {image_path}")
                return None

            # Open image and convert to binary data
            with Image.open(image_path) as image:
                print("✅ Image successfully loaded")

                # Convert image to bytes
                image_bytes_io = io.BytesIO()
                image.save(image_bytes_io, format="JPEG")  # Save image in JPEG format
                image_bytes = image_bytes_io.getvalue()

            prompt_text = """
            Identify all food ingredients in the image. Output as a JSON array.
            Example: ["Tomato", "Onion", "Garlic"]
            """

            # ✅ Ensure this dictionary is correctly formatted
            config = {
                "temperature": 0,
                "max_output_tokens": 2048
            }

            print("🔹 Sending request to Gemini API...")

            # Correct request format
            response = self.client.generate_content(
                contents=[
                    {"role": "user", "parts": [{"text": prompt_text}]},
                    {"role": "user", "parts": [{"mime_type": "image/jpeg", "data": image_bytes}]},
                ],
                generation_config=config
            )

            print(f"🔹 Gemini API Response: {response.text}")

            # Extract JSON array from the response
            response_text = response.text
            json_str = response_text[response_text.find("["):response_text.rfind("]") + 1]
            ingredients = json.loads(json_str)

            print(f"✅ Extracted Ingredients: {ingredients}")
            return ingredients

        except Exception as e:
            print(f"🔴 Error processing image: {e}")
            return None
