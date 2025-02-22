from firebase_config import get_db
from typing import List, Dict, Optional
from datetime import datetime

class IngredientService:
    def __init__(self):
        self.db = get_db()

    def store_ingredients_list(self, user_id: str, list_name: str, ingredients: List[str]) -> int:
        """
        Stores ingredients list in Firebase with user association
        
        Args:
            user_id: The ID of the user who owns this list
            list_name: Name of the ingredients list
            ingredients: List of ingredients
        
        Returns:
            int: 0 if successful, -1 if failed
        """
        try:
            doc_ref = self.db.collection('users').document(user_id)\
                        .collection('ingredient_lists').document(list_name)
            
            doc_ref.set({
                'name': list_name,
                'ingredients': ingredients,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            })
            return 0
        except Exception as e:
            print(f"Error storing ingredients: {e}")
            return -1

    def get_ingredients_list(self, user_id: str, list_name: str) -> Optional[Dict]:
        """
        Retrieves ingredients list from Firebase
        
        Args:
            user_id: The ID of the user who owns the list
            list_name: Name of the ingredients list
        
        Returns:
            Optional[Dict]: Dictionary containing the ingredients list or None if not found
        """
        try:
            doc_ref = self.db.collection('users').document(user_id)\
                        .collection('ingredient_lists').document(list_name)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error retrieving ingredients: {e}")
            return None

    def get_all_ingredient_lists(self, user_id: str) -> List[Dict]:
        """
        Retrieves all ingredient lists for a user
        
        Args:
            user_id: The ID of the user
        
        Returns:
            List[Dict]: List of all ingredient lists
        """
        try:
            lists_ref = self.db.collection('users').document(user_id)\
                          .collection('ingredient_lists')
            docs = lists_ref.stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error retrieving all ingredients lists: {e}")
            return []

    def update_ingredients_list(self, user_id: str, list_name: str, 
                              ingredients: List[str]) -> int:
        """
        Updates an existing ingredients list
        
        Args:
            user_id: The ID of the user who owns the list
            list_name: Name of the ingredients list
            ingredients: Updated list of ingredients
        
        Returns:
            int: 0 if successful, -1 if failed
        """
        try:
            doc_ref = self.db.collection('users').document(user_id)\
                        .collection('ingredient_lists').document(list_name)
            
            doc_ref.update({
                'ingredients': ingredients,
                'updated_at': datetime.now()
            })
            return 0
        except Exception as e:
            print(f"Error updating ingredients list: {e}")
            return -1

    def delete_ingredients_list(self, user_id: str, list_name: str) -> int:
        """
        Deletes an ingredients list
        
        Args:
            user_id: The ID of the user who owns the list
            list_name: Name of the ingredients list
        
        Returns:
            int: 0 if successful, -1 if failed
        """
        try:
            doc_ref = self.db.collection('users').document(user_id)\
                        .collection('ingredient_lists').document(list_name)
            doc_ref.delete()
            return 0
        except Exception as e:
            print(f"Error deleting ingredients list: {e}")
            return -1

    def add_ingredients_from_image(self, user_id: str, list_name: str, 
                                 image_ingredients: List[str]) -> int:
        """
        Adds ingredients from image processing to an existing or new list
        
        Args:
            user_id: The ID of the user
            list_name: Name of the ingredients list
            image_ingredients: List of ingredients extracted from image
        
        Returns:
            int: 0 if successful, -1 if failed
        """
        try:
            existing_list = self.get_ingredients_list(user_id, list_name)
            
            if existing_list:
                # Combine existing ingredients with new ones, removing duplicates
                all_ingredients = list(set(existing_list['ingredients'] + image_ingredients))
                return self.update_ingredients_list(user_id, list_name, all_ingredients)
            else:
                # Create new list if it doesn't exist
                return self.store_ingredients_list(user_id, list_name, image_ingredients)
        except Exception as e:
            print(f"Error adding ingredients from image: {e}")
            return -1 