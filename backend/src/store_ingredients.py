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
    # if existing_data:
    #     use_existing = input("Would you like to pull ingredients from an existing list? (yes/no): ").strip().lower()
    #     if use_existing == 'yes':
    #         print("Available ingredient lists:")
    #         lists = list(existing_data.keys())
    #         for i, name in enumerate(lists, 1):
    #             print(f"{i}. {name}")
    #             for j, ingredient in enumerate(existing_data[name], 1):
    #                 print(f"  {j}. {ingredient}")
    #         try:
    #             choices = input("Enter numbers of items to pull from (comma-separated): ").strip()
    #             selected_lists = [lists[int(i)-1] for i in choices.split(',') if i.isdigit() and 0 < int(i) <= len(lists)]
    #             for lst in selected_lists:
    #                 ingredients.extend(existing_data[lst])
    #         except Exception:
    #             print("Invalid selection.")
    
    # save_option = input("Would you like to save this ingredient list? (yes/no): ").strip().lower()
    # if save_option == 'yes':
    #     return list_name, ingredients
    # else:
    #     print("Ingredient list discarded.")
    #     return None, None

# def save_ingredients(list_name, ingredients, filename="ingredients.json"):
#     try:
#         with open(filename, "r") as file:
#             data = json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         data = {}
    
#     data[list_name] = ingredients
    
#     with open(filename, "w") as file:
#         json.dump(data, file, indent=4)
#     print(f"Ingredients saved under '{list_name}' in {filename}")

# def load_ingredients(filename="ingredients.json"):
#     try:
#         with open(filename, "r") as file:
#             data = json.load(file)
#         return data
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {}

# def delete_ingredient_list(filename="ingredients.json"):
#     data = load_ingredients(filename)
#     if not data:
#         print("No ingredient lists to delete.")
#         return
    
#     print("Available ingredient lists:")
#     lists = list(data.keys())
#     for i, name in enumerate(lists, 1):
#         print(f"{i}. {name}")
    
#     choice = input("Enter the number of the list to delete: ").strip()
#     if choice.isdigit() and 0 < int(choice) <= len(lists):
#         del data[lists[int(choice)-1]]
#         with open(filename, "w") as file:
#             json.dump(data, file, indent=4)
#         print("Ingredient list deleted.")
#     else:
#         print("Invalid selection.")

# def view_ingredient_lists(filename="ingredients.json"):
#     data = load_ingredients(filename)
#     if not data:
#         print("No ingredient lists found.")
#         return
    
#     print("Existing ingredient lists:")
#     lists = list(data.keys())
#     for i, name in enumerate(lists, 1):
#         print(f"{i}. {name}")
    
#     choice = input("Enter the number of the list to view ingredients: ").strip()
#     if choice.isdigit() and 0 < int(choice) <= len(lists):
#         print(f"Ingredients in '{lists[int(choice)-1]}': {', '.join(data[lists[int(choice)-1]])}")
#     else:
#         print("Invalid selection.")

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

