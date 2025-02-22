from google import genai
from google.genai.types import GenerateContentConfig
from PIL import Image
from typing import List, Optional
from functions import get_api_key
import json

class VisionService:
    def __init__(self):
        api_key_data = get_api_key()
        if api_key_data == -1:
            raise ValueError("Failed to get API key")
        self.client = genai.Client(api_key=api_key_data['api_key'])
        
    def extract_ingredients_from_image(self, image_path: str) -> Optional[List[str]]:
        """
        Extracts ingredients from an image using Gemini Vision
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
            
            # Extract JSON array from response
            json_str = response.text[response.text.find("["):response.text.rfind("]") + 1]
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

def process_image_for_ingredients(image_path):
    """
    This is where you'll integrate with your computer vision service.
    For now, returning mock data.
    """
    # Mock response - replace with actual computer vision processing
    return ['tomato', 'onion', 'garlic'] 