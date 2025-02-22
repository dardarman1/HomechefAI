from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.services.recipe_service import get_recipes_for_ingredients
from app.services.vision_service import process_image_for_ingredients
from app.utils.helpers import allowed_file

api = Blueprint('api', __name__)

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@api.route('/recipes/by-ingredients', methods=['GET'])
def get_recipes_by_ingredients():
    try:
        ingredients = request.args.getlist('ingredients')
        
        if not ingredients:
            return jsonify({
                'status': 'error',
                'message': 'No ingredients provided'
            }), 400

        recipes = get_recipes_for_ingredients(ingredients)
        
        return jsonify({
            'status': 'success',
            'recipes': recipes
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/recipes/by-image', methods=['POST'])
def get_recipes_by_image():
    try:
        if 'image' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No image file provided'
            }), 400

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No selected file'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'File type not allowed'
            }), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process image to detect ingredients
        detected_ingredients = process_image_for_ingredients(filepath)
        
        # Get recipes based on detected ingredients
        recipes = get_recipes_for_ingredients(detected_ingredients)

        # Clean up uploaded file
        os.remove(filepath)

        return jsonify({
            'status': 'success',
            'detected_ingredients': detected_ingredients,
            'recipes': recipes
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 