import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import using the correct paths
from app.services.vision_service import VisionService
from app.services.recipe_service import RecipeService
from src.ingredient_service import IngredientService

def test_vision_service():
    try:
        vision_service = VisionService()
        # Test with a sample image
        result = vision_service.extract_ingredients_from_image('path/to/test/image.jpg')
        print("Vision Service Test Result:", result)
    except Exception as e:
        print("Vision Service Test Failed:", e)

def test_recipe_service():
    try:
        recipe_service = RecipeService()
        # Test recipe creation
        test_recipe = {
            'name': 'Test Recipe',
            'ingredients': ['ingredient1', 'ingredient2'],
            'instructions': ['step1', 'step2']
        }
        result = recipe_service.store_recipe(
            test_recipe['name'],
            test_recipe['ingredients'],
            test_recipe['instructions']
        )
        print("Recipe Service Store Test Result:", result)
        
        # Test recipe retrieval
        retrieved = recipe_service.get_recipe('Test Recipe')
        print("Recipe Service Retrieve Test Result:", retrieved)
    except Exception as e:
        print("Recipe Service Test Failed:", e)

def test_ingredient_service():
    try:
        ingredient_service = IngredientService()
        # Test ingredient list creation
        test_user_id = "test_user_123"
        test_list_name = "Test List"
        test_ingredients = ["apple", "banana", "orange"]
        
        result = ingredient_service.store_ingredients_list(
            test_user_id,
            test_list_name,
            test_ingredients
        )
        print("Ingredient Service Store Test Result:", result)
        
        # Test ingredient list retrieval
        retrieved = ingredient_service.get_ingredients_list(test_user_id, test_list_name)
        print("Ingredient Service Retrieve Test Result:", retrieved)
    except Exception as e:
        print("Ingredient Service Test Failed:", e)

if __name__ == "__main__":
    print("Testing Vision Service...")
    test_vision_service()
    
    print("\nTesting Recipe Service...")
    test_recipe_service()
    
    print("\nTesting Ingredient Service...")
    test_ingredient_service() 