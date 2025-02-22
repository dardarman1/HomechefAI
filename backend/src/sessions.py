import uuid
import threading
from flask import Flask, request, jsonify
import connect_to_supercook as sp  #module that handles recipe fetching

app = Flask(__name__)

# Global in-memory session store. Each session ID maps to a list of ingredients.
session_store = {}
session_lock = threading.Lock()

@app.route('/start_session', methods=['POST'])
def start_session():
    """
    Create a new session by generating a unique session_id.
    """
    session_id = str(uuid.uuid4())
    with session_lock:
        session_store[session_id] = []
    return jsonify({"session_id": session_id})

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    """
    Add an ingredient to the given session.
    Expects JSON with 'session_id' and 'ingredient'.
    """
    data = request.get_json()
    session_id = data.get("session_id")
    ingredient = data.get("ingredient")
    
    if not session_id or not ingredient:
        return jsonify({"error": "Missing session_id or ingredient"}), 400

    with session_lock:
        if session_id not in session_store:
            return jsonify({"error": "Session not found"}), 404
        session_store[session_id].append(ingredient)
        current_ingredients = session_store[session_id]
        
    return jsonify({
        "message": "Ingredient added",
        "ingredients": current_ingredients
    })

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    """
    Fetch recipes based on the ingredients collected for the session.
    Expects JSON with 'session_id'.
    """
    data = request.get_json()
    session_id = data.get("session_id")
    
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    with session_lock:
        if session_id not in session_store:
            return jsonify({"error": "Session not found"}), 404
        ingredients = session_store[session_id]
    
    # Use your module to get recipes based on the ingredients.
    recipes = sp.get_ingredients_for_supercook(ingredients)
    return jsonify({"recipes": recipes})

if __name__ == '__main__':
    # Run the Flask development server. Use a production-ready server (e.g. Gunicorn) for real deployments.
    app.run(debug=True)
