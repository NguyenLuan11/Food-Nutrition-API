from flask import request, jsonify, send_from_directory, abort
from sqlalchemy import event
from sqlalchemy.sql import func
from ..model import db, Foods, FoodNutrient
from ..food_nutrition_ma import FoodsSchema
from werkzeug.utils import secure_filename
import os
from ..config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_FOODS

food = FoodsSchema()
foods = FoodsSchema(many=True)

UPLOAD_FOLDER_FOODS = os.path.join(os.getcwd(), UPLOAD_FOLDER_FOODS)


# Hàm phân loại BMI
def determine_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 24.9:
        return "normal"
    elif 25 <= bmi < 29.9:
        return "overweight"
    else:
        return "obese"


def recommend_foods_by_bmi_service(BMI):
    try:
        # Phân loại BMI
        categoryBMI = determine_bmi_category(BMI)

        list_recommend_foods = []

        # Lọc thực phẩm theo loại
        if categoryBMI == "underweight":
            recommend_foods = Foods.query.filter(Foods.kcalOn100g > 150).all()
        elif categoryBMI == "normal":
            recommend_foods = Foods.query.filter(Foods.kcalOn100g <= 250).all()
        elif categoryBMI == "overweight":
            recommend_foods = Foods.query.filter(Foods.kcalOn100g < 150).all()
        else:  # obese
            recommend_foods = Foods.query.filter(Foods.kcalOn100g < 150).all()

        if recommend_foods:
            for food in recommend_foods:
                list_recommend_foods.append({
                    "foodID": food.foodID,
                    "foodName": food.foodName,
                    "image": food.image or None,
                    "kcalOn100g": food.kcalOn100g,
                    "nutritionValue": food.nutritionValue,
                    "preservation": food.preservation or None,
                    "note": food.note or None,
                    "created_date": food.created_date.strftime("%Y-%m-%d"),
                    "modified_date": food.modified_date.strftime("%Y-%m-%d") or None
                })
            return jsonify(list_recommend_foods), 200
        else:
            return jsonify({"message": "Haven't list recommend foods!"}), 404

    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Hàm kiểm tra định dạng file hợp lệ
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

                # Kiểm tra nếu file không có tên
                if file.filename == '':
                    return jsonify({"message": "No selected file"}), 400

                # Kiểm tra loại file
                if file and allowed_file(file.filename):
                    fileName = secure_filename(file.filename)  # Đảm bảo tên file an toàn
                    file_path = os.path.join(UPLOAD_FOLDER_FOODS, fileName)

                    # Lưu file vào thư mục
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
    if data and all(key in data for key in ('foodName', 'kcalOn100g', 'proteinOn100g', 'carbsOn100g', 'fatOn100g',
    'fiberOn100g', 'omega3On100g', 'sugarOn100g', 'nutritionValue', 'preservation', 'note')) \
        and data['foodName'] and data['kcalOn100g'] and data['proteinOn100g'] and data['carbsOn100g'] \
            and data['fatOn100g'] and data['fiberOn100g'] and data['omega3On100g'] and data['sugarOn100g'] \
            and data['nutritionValue'] and data['foodName'] != "" and data['nutritionValue'] != "":
        foodName = data['foodName']
        kcalOn100g = data['kcalOn100g']
        proteinOn100g = data['proteinOn100g']
        carbsOn100g = data['carbsOn100g']
        fatOn100g = data['fatOn100g']
        fiberOn100g = data['fiberOn100g']
        omega3On100g = data['omega3On100g']
        sugarOn100g = data['sugarOn100g']
        nutritionValue = data['nutritionValue']
        preservation = data['preservation'] if data['preservation'] else None
        note = data['note'] if data['note'] else None

        try:
            new_food = Foods(foodName=foodName, kcalOn100g=kcalOn100g, nutritionValue=nutritionValue,
                             preservation=preservation, note=note, proteinOn100g=proteinOn100g, carbsOn100g=carbsOn100g,
                             fatOn100g=fatOn100g, fiberOn100g=fiberOn100g, omega3On100g=omega3On100g, sugarOn100g=sugarOn100g)
            db.session.add(new_food)
            db.session.commit()

            return jsonify({
                "foodID": new_food.foodID,
                "foodName": new_food.foodName,
                "image": new_food.image if new_food.image else None,
                "kcalOn100g": new_food.kcalOn100g,
                # "proteinOn100g": new_food.proteinOn100g,
                # "carbsOn100g": new_food.carbsOn100g,
                # "fatOn100g": new_food.fatOn100g,
                # "fiberOn100g": new_food.fiberOn100g,
                # "omega3On100g": new_food.omega3On100g,
                # "sugarOn100g": new_food.sugarOn100g,
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


# GET IMG FOOD
# Tải ảnh trực tiếp từ thư mục lưu trữ
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
                "image": food.image if food.image else None,
                "kcalOn100g": food.kcalOn100g,
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
                    "image": food.image if food.image else None,
                    "kcalOn100g": food.kcalOn100g,
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


# UPDATE FOOD BY ID
def update_food_by_id_service(id):
    try:
        food = Foods.query.get(id)
        data = request.json
        if food:
            if data and all(
                    key in data for key in ('foodName', 'kcalOn100g', 'proteinOn100g', 'carbsOn100g', 'fatOn100g',
                                            'fiberOn100g', 'omega3On100g', 'sugarOn100g', 'nutritionValue',
                                            'preservation', 'note')) \
                    and data['foodName'] and data['kcalOn100g'] and data['proteinOn100g'] and data['carbsOn100g'] \
                    and data['fatOn100g'] and data['fiberOn100g'] and data['omega3On100g'] and data['sugarOn100g'] \
                    and data['nutritionValue'] and data['foodName'] != "" and data['nutritionValue'] != "":
                try:
                    food.foodName = data['foodName']
                    food.kcalOn100g = data['kcalOn100g']
                    food.proteinOn100g = data['proteinOn100g']
                    food.carbsOn100g = data['carbsOn100g']
                    food.fatOn100g = data['fatOn100g']
                    food.fiberOn100g = data['fiberOn100g']
                    food.omega3On100g = data['omega3On100g']
                    food.sugarOn100g = data['sugarOn100g']
                    food.nutritionValue = data['nutritionValue']
                    food.preservation = data['preservation'] if data['preservation'] else None
                    food.note = data['note'] if data['note'] else None

                    return jsonify({
                        "foodID": food.foodID,
                        "foodName": food.foodName,
                        "image": food.image if food.image else None,
                        "kcalOn100g": food.kcalOn100g,
                        "nutritionValue": food.nutritionValue,
                        "preservation": food.preservation if food.preservation else None,
                        "note": food.note if food.note else None,
                        "created_date": food.created_date.strftime("%Y-%m-%d"),
                        "modified_date": food.modified_date.strftime("%Y-%m-%d") if food.modified_date else None
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update food!"}), 400
        else:
            return jsonify({"message": "Not found food!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


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
