import json
import threading
import connect_to_supercook as sp

g_ingredients_list = []
ingredients_lock = threading.Lock()

def get_user_ingredients():
    global g_ingredients_list
    ingredients = []
    list_name = input("Enter a name for your ingredient list: ").strip()
    print("Enter ingredients one by one. Type 'done' when finished:")
    
    while True:
        ingredient = input("Ingredient: ").strip()
        if ingredient.lower() == 'done':
            break
        if ingredient:
            ingredients.append(ingredient)
    with ingredients_lock:
        g_ingredients_list.append({
            "list_name": list_name,
            "ingredients": ingredients
        })
    sp.get_ingredients_for_supercook(ingredients)
    print(f"Ingredient list '{list_name}' saved!")
    print(g_ingredients_list)
    
if __name__ == "__main__":
    while True:
        action = input("Type '1' to create a new ingredient list and 'exit' to quit: ").strip()
        if action == '1':
            get_user_ingredients()
        elif action.lower() == 'exit':
            break
        else:
            print("Invalid choice. Please enter '1' or 'exit'.")