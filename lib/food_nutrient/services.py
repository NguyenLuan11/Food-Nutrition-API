from flask import request, jsonify
from ..model import db, FoodNutrient, Foods, Nutrients
from ..food_nutrition_ma import FoodNutrientSchema
from sqlalchemy.sql import func

foodNutrient = FoodNutrientSchema()
foodNutrients = FoodNutrientSchema(many=True)


def add_foodNutrient_service():
    data = request.json
    if data and all(key in data for key in ('foodID', 'nutrientID')) and data['foodID'] and data['nutrientID']:
        foodID = data['foodID']
        nutrientID = data['nutrientID']
        try:
            new_foodNutrient = FoodNutrient(foodID=foodID, nutrientID=nutrientID)

            db.session.add(new_foodNutrient)
            db.session.commit()

            return jsonify({
                "foodID": new_foodNutrient.foodID,
                "nutrientID": new_foodNutrient.nutrientID
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add food's nutrient"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_all_foodNutrient_service():
    try:
        foodNutrients = FoodNutrient.query.all()
        if foodNutrients:
            list_foodNutrients = []
            for foodNutrient in foodNutrients:
                list_foodNutrients.append({
                    "foodID": foodNutrient.foodID,
                    "nutrientID": foodNutrient.nutrientID
                })
            return jsonify(list_foodNutrients), 200
        else:
            return jsonify({"message": "Not found list of food's nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_foodNutrient_by_foodID_service(foodID):
    try:
        foodNutrients = FoodNutrient.query.join(Foods, FoodNutrient.foodID == Foods.foodID)\
            .filter(Foods.foodID == foodID).all()
        if foodNutrients:
            list_foodNutrients = []
            for foodNutrient in foodNutrients:
                list_foodNutrients.append({
                    "foodID": foodNutrient.foodID,
                    "nutrientID": foodNutrient.nutrientID
                })
            return jsonify(list_foodNutrients), 200
        else:
            return jsonify({"message": "Not found list of food's nutrient by food's ID!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_foodNutrient_by_nutrientID_service(nutrientID):
    try:
        foodNutrients = FoodNutrient.query.join(Nutrients, FoodNutrient.nutrientID == Nutrients.nutrientID)\
            .filter(Nutrients.nutrientID == nutrientID).all()
        if foodNutrients:
            list_foodNutrients = []
            for foodNutrient in foodNutrients:
                list_foodNutrients.append({
                    "foodID": foodNutrient.foodID,
                    "nutrientID": foodNutrient.nutrientID
                })
            return jsonify(list_foodNutrients), 200
        else:
            return jsonify({"message": "Not found list of food's nutrient by food's ID!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_foodNutrient_service(foodID, nutrientID):
    try:
        foodNutrient = FoodNutrient.query.filter_by(foodID=foodID, nutrientID=nutrientID).first()
        data = request.json
        if foodNutrient:
            if data and all(key in data for key in ('foodID', 'nutrientID')) and data['foodID'] and data['nutrientID']:
                try:
                    foodNutrient.foodID = data['foodID']
                    foodNutrient.nutrientID = data['nutrientID']

                    db.session.commit()

                    return jsonify({
                        "foodID": foodNutrient.foodID,
                        "nutrientID": foodNutrient.nutrientID
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update food's nutrient"}), 400
        else:
            return jsonify({"message": "Not found food's nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def delete_foodNutrient_service(foodID, nutrientID):
    try:
        foodNutrient = FoodNutrient.query.filter_by(foodID=foodID, nutrientID=nutrientID).first()
        if foodNutrient:
            try:
                db.session.delete(foodNutrient)
                db.session.commit()
                return jsonify({"message": "Food's nutrient deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete food's nutrient"}), 400
        else:
            return jsonify({"message": "Not found food's nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
