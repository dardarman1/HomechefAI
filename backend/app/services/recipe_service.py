from firebase_config import get_db
from typing import List, Dict, Optional

class RecipeService:
    def __init__(self):
        self.db = get_db()
    
    def store_recipe(self, recipe_name: str, ingredients: List[str], instructions: List[str]) -> int:
        """
        Stores a recipe in Firebase
        """
        try:
            doc_ref = self.db.collection('recipes').document(recipe_name)
            doc_ref.set({
                'name': recipe_name,
                'ingredients': ingredients,
                'instructions': instructions
            })
            return 0
        except Exception as e:
            print(f"Error storing recipe: {e}")
            return -1
    
    def get_recipe(self, recipe_name: str) -> Optional[Dict]:
        """
        Retrieves a recipe from Firebase
        """
        try:
            doc_ref = self.db.collection('recipes').document(recipe_name)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error retrieving recipe: {e}")
            return None

def get_recipes_for_ingredients(ingredients):
    """
    This is where you'll integrate with your friend's recipe service.
    For now, returning mock data.
    """
    # Mock response - replace with actual API call to your friend's service
    return [
        {
            'id': 1,
            'name': 'Sample Recipe 1',
            'ingredients': ingredients,
            'instructions': ['Step 1', 'Step 2', 'Step 3'],
            'cooking_time': '30 minutes'
        },
        {
            'id': 2,
            'name': 'Sample Recipe 2',
            'ingredients': ingredients,
            'instructions': ['Step 1', 'Step 2'],
            'cooking_time': '45 minutes'
        }
    ] 