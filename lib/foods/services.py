from flask import request, jsonify
from sqlalchemy import event
from sqlalchemy.sql import func
from ..model import db, Foods, FoodNutrient
from ..food_nutrition_ma import FoodsSchema

food = FoodsSchema()
foods = FoodsSchema(many=True)


def add_foods_service():
    data = request.json
    if data and all(key in data for key in ('foodName', 'image', 'nutritionValue', 'preservation', 'note')) \
        and data['foodName'] and data['nutritionValue'] and data['foodName'] != "" and data['nutritionValue'] != "":
        foodName = data['foodName']
        image = data['image'] if data['image'] else None
        nutritionValue = data['nutritionValue']
        preservation = data['preservation'] if data['preservation'] else None
        note = data['note'] if data['note'] else None
        try:
            new_food = Foods(foodName=foodName, image=image, nutritionValue=nutritionValue,
                             preservation=preservation, note=note)
            db.session.add(new_food)
            db.session.commit()

            return jsonify({
                "foodID": new_food.foodID,
                "foodName": new_food.foodName,
                "image": new_food.image if new_food.image else None,
                "nutritionValue": new_food.nutritionValue,
                "preservation": new_food.preservation if new_food.preservation else None,
                "note": new_food.note if new_food.note else None,
                "created_date": new_food.created_date.strftime("%Y-%m-%d"),
                "modified_date": new_food.modified_date.strftime("%Y-%m-%d") if new_food.modified_date else None
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add food!"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_food_by_id_service(id):
    try:
        food = Foods.query.get(id)
        if food:
            return jsonify({
                "foodID": food.foodID,
                "foodName": food.foodName,
                "image": food.image if food.image else None,
                "nutritionValue": food.nutritionValue,
                "preservation": food.preservation if food.preservation else None,
                "note": food.note if food.note else None,
                "created_date": food.created_date.strftime("%Y-%m-%d"),
                "modified_date": food.modified_date.strftime("%Y-%m-%d") if food.modified_date else None
            }), 200
        else:
            return jsonify({"message": "Not found food!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_all_foods_service():
    try:
        foods = Foods.query.all()
        if foods:
            list_foods = []
            for food in foods:
                list_foods.append({
                    "foodID": food.foodID,
                    "foodName": food.foodName,
                    "image": food.image if food.image else None,
                    "nutritionValue": food.nutritionValue,
                    "preservation": food.preservation if food.preservation else None,
                    "note": food.note if food.note else None,
                    "created_date": food.created_date.strftime("%Y-%m-%d"),
                    "modified_date": food.modified_date.strftime("%Y-%m-%d") if food.modified_date else None
                })
            return jsonify(list_foods), 200
        else:
            return jsonify({"message": "Not found list of foods!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_food_by_id_service(id):
    try:
        food = Foods.query.get(id)
        data = request.json
        if food:
            if data and all(key in data for key in ('foodName', 'image', 'nutritionValue', 'preservation', 'note')) \
                    and data['foodName'] and data['nutritionValue'] \
                    and data['foodName'] != "" and data['nutritionValue'] != "":
                try:
                    food.foodName = data['foodName']
                    food.image = data['image'] if data['image'] else None
                    food.nutritionValue = data['nutritionValue']
                    food.preservation = data['preservation'] if data['preservation'] else None
                    food.note = data['note'] if data['note'] else None

                    db.session.commit()

                    return jsonify({
                        "foodID": food.foodID,
                        "foodName": food.foodName,
                        "image": food.image if food.image else none,
                        "nutritionValue": food.nutritionValue,
                        "preservation": food.preservation if food.preservation else None,
                        "note": food.note if food.note else None,
                        "created_date": food.created_date.strftime("%Y-%m-%d"),
                        "modified_date": food.modified_date.strftime("%Y-%m-%d")
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update food!"}), 400
        else:
            return jsonify({"message": "Not found food!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Sử dụng sự kiện before_delete để xóa tất cả các đối tượng FoodNutrient liên quan trước khi xóa đối tượng Foods
@event.listens_for(Foods, 'before_delete')
def delete_related_foodNutrient(mapper, connection, target):
    try:
        FoodNutrient.query.filter_by(foodID=target.foodID).delete()
        return True
    except Exception as e:
        db.session.rollback()
        return False, str(e)


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
