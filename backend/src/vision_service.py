from google import genai
from PIL import Image
# from google.generativeai import types
from google.genai import types
import json
import os
import io
from .functions import get_api_key
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
import requests
import time
from bs4 import BeautifulSoup

class VisionService:
    def __init__(self):
        """Initialize Google Gemini Vision AI Client."""
        api_key_data = get_api_key()
        
        if api_key_data is None:
            raise ValueError("Failed to get API key")
        
        print(f"🔹 Loaded API Key: {api_key_data}")  # Debugging

        # if api_key_data == -1:
        #     raise ValueError("Failed to get API key")

        self.client = genai.Client(api_key=api_key_data)
        print(f"✅ Successfully initialized Gemini Model: {self.client}")

    def extract_ingredients_from_image(self, image_bytes: str):
        """
        Extracts ingredients from an image using Gemini Vision AI.
        :param image_path: Path to the image file
        :return: List of extracted ingredients or None if an error occurs
        """
        try:
            prompt_text = """
            List all the ingredients in the image. Be as specific about ingredient type as possible while remaining accurate. Avoid duplicates. Output them as a JSON array.
            Example:
            ["Greek Yogurt", "Bananas", "Orange", "Red Apple", "Ground Beef"]
            """

            # ✅ Ensure this dictionary is correctly formatted
            config = {
                "temperature": 0,
                "max_output_tokens": 2048
            }

            print("🔹 Sending request to Gemini API...")

            # Correct request format
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {"role": "user", "parts": [{"text": prompt_text}]},
                    {"role": "user", "parts": [types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]},
                ],
                config=config
            )

            print(f"🔹 Gemini API Response: {response.text}")

            # Extract JSON array from the response
            response_text = response.text
            json_str = response_text[response_text.find("["):response_text.rfind("]") + 1]
            ingredients = json.loads(json_str)

            print(f"✅ Extracted Ingredients: {ingredients}")
            return ingredients
            # return ingredients

        except Exception as e:
            print(f"🔴 Error processing image: {e}")
            return None

    def get_recipes_from_ingredients(self, ingredients):
        """
        Fetches up to 5 valid recipes based on a list of ingredients using DuckDuckGo search and Gemini AI.
        :param ingredients: List of ingredients
        :return: List of recipes in JSON format or None if no valid recipes are found
        """
        try:
            print(f"🔹 Fetching recipes for ingredients: {ingredients}")

            # Convert ingredient list into a search-friendly query
            query = f"Recipe with {' '.join(ingredients)}"
            print(f"🔹 Searching DuckDuckGo for: {query}")

            while True:
                try:
                    results = DDGS().text(query, max_results=30)  # Fetch more results to find valid recipes
                    break
                except DuckDuckGoSearchException:
                    print("🔴 DuckDuckGo search failed, retrying...")
                    time.sleep(1)

            # If no results found, return an error
            if not results:
                print("🔴 No search results found.")
                return None

            valid_recipes = []
            counter = 0
            # Try multiple search results until we get up to 5 valid recipes
            for result in results:  # Check up to 10 results to find 5 good ones
                if (len(valid_recipes) >= 5 or counter >= 10):
                    break
                counter += 1
                try:
                    print(f"🔹 Fetching recipe from: {result['href']}")
                    
                    # 🔹 Fetch the recipe page
                    response = requests.get(result['href'])

                    # 🔴 Skip invalid responses
                    if response.status_code != 200:
                        print(f"🔴 Skipping {result['href']} - HTTP {response.status_code}")
                        continue

                    content_text = response.text.strip()

                    # 🔴 Skip empty pages
                    if not content_text:
                        print(f"🔴 Skipping {result['href']} - Empty page")
                        continue

                    # 🔹 Parse content with BeautifulSoup
                    soup = BeautifulSoup(content_text, 'html.parser')
                    content_text = soup.get_text()

                    # 🔹 Try extracting "Ingredients" section
                    if "Ingredients" not in content_text:
                        print(f"🔴 Skipping {result['href']} - No ingredients found")
                        continue

                    print("🔹 Extracting recipe details using Gemini AI...")

                    # 🔹 Gemini AI prompt with example format
                    prompt_text = """
                    Extract a recipe from the following text. Output the result in clean JSON format.
                    If there are no directions or recipes, and either or are empty, then do not output and instead output a
                    statement saying that either the directions or recipes are missing, or even both if that is the case.
                    Ensure the structure is:
                    {
                        "recipe_name": "Recipe Name",
                        "ingredients": ["Ingredient 1", "Ingredient 2", "Ingredient 3"],
                        "directions": ["Step 1", "Step 2", "Step 3"]
                    }
                    
                    Example:
                    {
                        "recipe_name": "Spaghetti Carbonara",
                        "ingredients": ["Spaghetti", "Eggs", "Parmesan Cheese", "Pancetta", "Salt", "Pepper"],
                        "directions": [
                            "Cook spaghetti in boiling salted water.",
                            "Fry pancetta until crispy.",
                            "Mix eggs and Parmesan cheese together.",
                            "Combine pasta with egg mixture and pancetta.",
                            "Serve immediately."
                        ]
                    }

                    Now extract the recipe from this text:
                    """ + content_text
                    # 🔹 Send to Gemini AI
                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[{"role": "user", "parts": [{"text": prompt_text}]}],
                        config={"temperature": 0, "max_output_tokens": 2048}
                    )

                    print(f"🔹 Gemini API Response: {response.text}")

                    # Validate Gemini AI response
                    response_text = response.text.strip()

                    if not response_text or "{" not in response_text:
                        print(f"🔴 Skipping {result['href']} - Invalid Gemini response")
                        continue

                    recipe_json = json.loads(response_text[response_text.find('{'):response_text.rfind('}') + 1])
                    
                    recipe_json["url"] = result["href"]  # Add the URL to the recipe JSON
                    print(recipe_json)

                    # Ensure proper structure and filter out empty recipes
                    if (
                        recipe_json.get("recipe_name") 
                        and recipe_json.get("ingredients") 
                        and recipe_json.get("directions") 
                        and recipe_json["ingredients"] != [] 
                        and recipe_json["directions"] != []
                    ):
                        valid_recipes.append(recipe_json)
                        yield json.dumps(recipe_json) + "\n"
                        print(f"✅ Valid recipe found: {recipe_json['recipe_name']}")
                    else:
                        print(f"🔴 Skipping {result['href']} - Empty or incomplete recipe")
                except Exception as e:
                    print(f"🔴 Error processing recipe page: {e}")
                
            # if not valid_recipes:
            #     print("🔴 No valid recipes found after multiple attempts.")
            #     return None  # No valid recipes found

            # print(f"✅ Successfully retrieved {len(valid_recipes)} recipes.")
            # return valid_recipes  # Return list of up to 5 recipes

        except Exception as e:
            print(f"🔴 Error fetching recipes: {e}")
            return None
        

# if __name__ == '__main__':
#     vision_service = VisionService()
#     vision_service.get_recipes_from_ingredients(["Tomato", "Onion", "Garlic"])