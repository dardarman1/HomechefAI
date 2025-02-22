import json

g_ingredients_list = []

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
    g_ingredients_list = ingredients
    return ingredients
    
def main():
    while True:
        action = input("Type '1' to create a new ingredient list and 'exit' to quit: ").strip()
        
        if action == '1':
            #data = load_ingredients()
            #list_name, ingredients
            get_user_ingredients()
            #if list_name and ingredients:
                #save_ingredients(list_name, ingredients)
        elif action.lower() == 'exit':
            break
        else:
            print("Invalid choice. Please enter '1' or 'exit'.")

if __name__ == "__main__":
    main()

