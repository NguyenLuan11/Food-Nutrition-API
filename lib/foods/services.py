from flask import request, jsonify, send_from_directory, abort
from sqlalchemy import event
from sqlalchemy.sql import func
from ..model import db, Foods, FoodNutrient
from ..food_nutrition_ma import FoodsSchema
from werkzeug.utils import secure_filename
import os
from ..config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_FOODS
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

food = FoodsSchema()
foods = FoodsSchema(many=True)

UPLOAD_FOLDER_FOODS = os.path.join(os.getcwd(), UPLOAD_FOLDER_FOODS)


# Filter BMI
def determine_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 24.9:
        return "normal"
    elif 25 <= bmi < 29.9:
        return "overweight"
    else:
        return "obese"


def food_to_dict(food):
    return {
        "foodID": food.foodID,
        "foodName": food.foodName,
        "image": food.image or None,
        "nutritionValue": food.nutritionValue,
        # "preservation": food.preservation or None,
        # "note": food.note or None,
        "kcalOn100g": food.kcalOn100g,
        # "proteinOn100g": food.proteinOn100g,
        # "carbsOn100g": food.carbsOn100g,
        # "fatOn100g": food.fatOn100g,
        # "fiberOn100g": food.fiberOn100g,
        # "omega3On100g": food.omega3On100g,
        # "sugarOn100g": food.sugarOn100g,
        # "created_date": food.created_date.strftime("%Y-%m-%d"),
        # "modified_date": food.modified_date.strftime("%Y-%m-%d") if food.modified_date else None
    }


# RECOMMEND FOODS
def recommend_foods_by_bmi_service(BMI):
    try:
        # Filter BMI
        categoryBMI = determine_bmi_category(BMI)

        # Get all foods from db
        foods = Foods.query.all()

        food_items = []
        food_ids = []
        food_features = []

        for food in foods:
            food_ids.append(food.foodID)
            food_items.append(food.foodName)
            # Get nutrition components (kcal, protein, carbs, fat, fiber, omega3, sugar)
            food_features.append([
                food.kcalOn100g,
                food.proteinOn100g,
                food.carbsOn100g,
                food.fatOn100g,
                food.fiberOn100g,
                food.omega3On100g,
                food.sugarOn100g
            ])

        # Get user_requirements by BMI
        if categoryBMI == "underweight":
            filtered_foods = [features for features in food_features if features[0] >= 180]
        elif categoryBMI == "normal":
            filtered_foods = [features for features in food_features if 150 <= features[0] <= 250]
        else:
            filtered_foods = [features for features in food_features if features[0] <= 150]

        if not filtered_foods:
            return jsonify({"message": "No foods found that match the BMI category!"}), 404

        user_requirements = filtered_foods[0]
        # print(user_requirements)

        # Calculate the cosine similarity between user requests and foods
        food_features_array = np.array(food_features)
        similarities = cosine_similarity([user_requirements], food_features_array)[0]

        # Sort foods by similarity
        sorted_foods = sorted(zip(food_ids, food_items, similarities), key=lambda x: x[2], reverse=True)

        # Take 2/3 of the sorted list
        total_foods = len(sorted_foods)
        top_foods = sorted_foods[:int(2 * total_foods / 3)]

        # Create recommended foods with similarity
        recommended_foods = [{"foodID": id, "foodName": food, "similarity": score} for id, food, score in top_foods]
        # print(recommended_foods)

        # Get list recommended foods
        list_recommended_foods = []
        for food in foods:
            for f in recommended_foods:
                if food.foodID == f['foodID']:
                    list_recommended_foods.append(food_to_dict(food))

        return jsonify(list_recommended_foods), 200

    except Exception as e:
        return jsonify({"message": f"Request error: {str(e)}"}), 400


# Check for valid file format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# UPLOAD IMG FOOD BY ID
def upload_img_food_by_id_service(id):
    try:
        food = Foods.query.get(id)
        uploadImg = request.files
        if food:
            if 'picFood' in uploadImg:
                file = uploadImg['picFood']

                # Check if file haven't name
                if file.filename == '':
                    return jsonify({"message": "No selected file"}), 400

                # Check kind of file
                if file and allowed_file(file.filename):
                    fileName = secure_filename(file.filename)  # Đảm bảo tên file an toàn
                    file_path = os.path.join(UPLOAD_FOLDER_FOODS, fileName)

                    # Save file into folder
                    file.save(file_path)

                    try:
                        food.image = fileName
                        db.session.commit()

                        return jsonify({
                            "image": food.image if food.image else None
                        }), 200
                    except IndentationError:
                        db.session.rollback()
                        return jsonify({"message": "Can not upload food's image!"}), 400
            else:
                return jsonify({"message": "No image provided!"}), 400
        else:
            return jsonify({"message": "Not found food!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# ADD NEW FOOD
def add_foods_service():
    data = request.json

    # Check if the data is valid
    required_fields = [
        'foodName', 'kcalOn100g', 'proteinOn100g', 'carbsOn100g', 'fatOn100g',
        'fiberOn100g', 'omega3On100g', 'sugarOn100g', 'nutritionValue', 'preservation', 'note'
    ]

    if all(key in data for key in required_fields) and data.get('foodName') and data.get('nutritionValue'):
        try:
            # Get value from request data
            foodName = data['foodName']
            kcalOn100g = data['kcalOn100g']
            proteinOn100g = data['proteinOn100g']
            carbsOn100g = data['carbsOn100g']
            fatOn100g = data['fatOn100g']
            fiberOn100g = data['fiberOn100g']
            omega3On100g = data['omega3On100g']
            sugarOn100g = data['sugarOn100g']
            nutritionValue = data['nutritionValue']
            preservation = data.get('preservation')  # Preserve None if no value
            note = data.get('note')  # Preserve None if no value

            # Create new food and add to db
            new_food = Foods(
                foodName=foodName, kcalOn100g=kcalOn100g, nutritionValue=nutritionValue,
                preservation=preservation, note=note, proteinOn100g=proteinOn100g, carbsOn100g=carbsOn100g,
                fatOn100g=fatOn100g, fiberOn100g=fiberOn100g, omega3On100g=omega3On100g, sugarOn100g=sugarOn100g,
                image=None
            )
            db.session.add(new_food)
            db.session.commit()

            return jsonify({
                "foodID": new_food.foodID,
                "foodName": new_food.foodName,
                "image": new_food.image or None,
                "kcalOn100g": new_food.kcalOn100g,
                # "proteinOn100g": new_food.proteinOn100g,
                # "carbsOn100g": new_food.carbsOn100g,
                # "fatOn100g": new_food.fatOn100g,
                # "fiberOn100g": new_food.fiberOn100g,
                # "omega3On100g": new_food.omega3On100g,
                # "sugarOn100g": new_food.sugarOn100g,
                "nutritionValue": new_food.nutritionValue,
                # "preservation": new_food.preservation or None,
                # "note": new_food.note or None,
                "created_date": new_food.created_date.strftime("%Y-%m-%d"),
                # "modified_date": new_food.modified_date.strftime("%Y-%m-%d") if new_food.modified_date else None
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Can not add food! Error: {str(e)}"}), 400
    else:
        return jsonify({"message": "Invalid data, missing required fields!"}), 400


# GET IMG FOOD
def get_image_service(fileName):
    try:
        return send_from_directory(UPLOAD_FOLDER_FOODS, fileName)
    except FileNotFoundError:
        abort(404, description="Image not found")


# GET FOOD BY ID
def get_food_by_id_service(id):
    try:
        food = Foods.query.get(id)
        if food:
            return jsonify({
                "foodID": food.foodID,
                "foodName": food.foodName,
                "image": food.image or None,
                "kcalOn100g": food.kcalOn100g,
                "proteinOn100g": food.proteinOn100g,
                "carbsOn100g": food.carbsOn100g,
                "fatOn100g": food.fatOn100g,
                "fiberOn100g": food.fiberOn100g,
                "omega3On100g": food.omega3On100g,
                "sugarOn100g": food.sugarOn100g,
                "nutritionValue": food.nutritionValue,
                "preservation": food.preservation or None,
                "note": food.note or None,
                "created_date": food.created_date.strftime("%Y-%m-%d"),
                "modified_date": food.modified_date.strftime("%Y-%m-%d") if food.modified_date else None
            }), 200
        else:
            return jsonify({"message": "Not found food!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET ALL FOODS
def get_all_foods_service():
    try:
        foods = Foods.query.all()
        if foods:
            list_foods = []
            for food in foods:
                list_foods.append({
                    "foodID": food.foodID,
                    "foodName": food.foodName,
                    "image": food.image or None,
                    "kcalOn100g": food.kcalOn100g,
                    "nutritionValue": food.nutritionValue,
                    "preservation": food.preservation or None,
                    "note": food.note or None,
                    "created_date": food.created_date.strftime("%Y-%m-%d"),
                    "modified_date": food.modified_date.strftime("%Y-%m-%d") if food.modified_date else None
                })
            return jsonify(list_foods), 200
        else:
            return jsonify({"message": "Not found list of foods!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# UPDATE FOOD BY ID
def update_food_by_id_service(id):
    try:
        food = Foods.query.get(id)
        if not food:
            return jsonify({"message": "Food not found!"}), 404

        # Get data from request
        data = request.json
        # Validate input data
        required_fields = [
            'foodName', 'kcalOn100g', 'proteinOn100g', 'carbsOn100g', 'fatOn100g',
            'fiberOn100g', 'omega3On100g', 'sugarOn100g', 'nutritionValue', 'preservation', 'note'
        ]
        if all(key in data for key in required_fields) and data['foodName'] and data['nutritionValue']:
            # Update food object with new data
            food.foodName = data['foodName']
            food.kcalOn100g = data['kcalOn100g']
            food.proteinOn100g = data['proteinOn100g']
            food.carbsOn100g = data['carbsOn100g']
            food.fatOn100g = data['fatOn100g']
            food.fiberOn100g = data['fiberOn100g']
            food.omega3On100g = data['omega3On100g']
            food.sugarOn100g = data['sugarOn100g']
            food.nutritionValue = data['nutritionValue']
            food.preservation = data.get('preservation')  # Preserve the None value if not provided
            food.note = data.get('note')

            db.session.commit()

            # Return updated food info
            return jsonify({
                "foodID": food.foodID,
                "foodName": food.foodName,
                "image": food.image or None,
                "kcalOn100g": food.kcalOn100g,
                # "proteinOn100g": food.proteinOn100g,
                # "carbsOn100g": food.carbsOn100g,
                # "fatOn100g": food.fatOn100g,
                # "fiberOn100g": food.fiberOn100g,
                # "omega3On100g": food.omega3On100g,
                # "sugarOn100g": food.sugarOn100g,
                "nutritionValue": food.nutritionValue,
                # "preservation": food.preservation or None,
                # "note": food.note or None,
                # "created_date": food.created_date.strftime("%Y-%m-%d"),
                "modified_date": food.modified_date.strftime("%Y-%m-%d") if food.modified_date else None
            }), 200
        else:
            return jsonify({"message": "Invalid data, missing required fields!"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Request error: {str(e)}"}), 400


# DELETE FOODNUTRIENT
# Sử dụng sự kiện before_delete để xóa tất cả các đối tượng FoodNutrient liên quan trước khi xóa đối tượng Foods
@event.listens_for(Foods, 'before_delete')
def delete_related_foodNutrient(mapper, connection, target):
    try:
        FoodNutrient.query.filter_by(foodID=target.foodID).delete()
        return True
    except Exception as e:
        db.session.rollback()
        return False, str(e)


# DELETE FOOD BY ID
def delete_food_by_id_service(id):
    try:
        food = Foods.query.get(id)
        if food:
            try:
                db.session.delete(food)
                db.session.commit()
                return jsonify({"message": "Food deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete food!"}), 200
        else:
            return jsonify({"message": "Not found food!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
