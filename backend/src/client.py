import requests
import os 
API_BASE = "http://127.0.0.1:8080"

def start_session():
    """Start a new session and return the session ID."""
    response = requests.get(f"{API_BASE}/start_session")
    if response.status_code == 200:
        session_id = response.json().get("session_id")
        print(f"Session started: {session_id}")
        return session_id
    else:
        print("Error starting session:", response.text)
        return None

def upload_image(session_id, image_path):
    """Upload an image to extract ingredients for a given session."""
    if not os.path.exists(image_path):
        print(f"🔴 Error: Image file {image_path} not found")
        return None

    print(f"🔹 Uploading image: {image_path}")
    print(f"🔹 Sending session ID: {session_id}")

    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        data = {"session_id": session_id}
        
        response = requests.post(f"{API_BASE}/get_ingredients", files=files, data=data)

    print(f"🔹 Response status code: {response.status_code}")
    print(f"🔹 Response content: {response.text}")

    if response.status_code == 200:
        ingredients = response.json().get("ingredients")
        print(f"✅ Extracted Ingredients: {ingredients}")
        return ingredients
    else:
        print(f"🔴 Error extracting ingredients: {response.text}")
        return None

def fetch_recipes(session_id):
    """Fetch recipes based on the extracted ingredients in a session."""
    payload = {"session_id": session_id}
    response = requests.post(f"{API_BASE}/get_recipes", json=payload)

    if response.status_code == 200:
        recipes = response.json().get("recipes")
        print("Suggested Recipes:", recipes)
        return recipes
    else:
        print("Error fetching recipes:", response.text)
        return None

if __name__ == "__main__":
    # Start a new session
    session_id = start_session()
    print("Session started")
    
    if not session_id:
        exit(1)

    # Upload an image (Replace 'test_image.jpg' with your actual image file)
    image_path = "test.jpg"
    upload_image(session_id, image_path)

    # Get recipes based on extracted ingredients
    fetch_recipes(session_id)
