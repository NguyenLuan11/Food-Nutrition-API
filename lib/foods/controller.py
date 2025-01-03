from flask import Blueprint, jsonify
from .services import add_foods_service, get_food_by_id_service, get_all_foods_service, update_food_by_id_service, \
    delete_food_by_id_service, get_image_service, upload_img_food_by_id_service, recommend_foods_by_bmi_service, \
    generate_plan_service, get_latest_plan_by_user_id_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt

foods = Blueprint("foods", __name__, url_prefix="/api/foods-management")


# ADD NEW FOOD
@foods.route("/food", methods=["POST"])
@jwt_required()
@swag_from("docs/add_food.yaml")
def add_foods():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return add_foods_service()


# GENERATE PLAN
@foods.route('/food/generate_plan', methods=["POST"])
def generate_plan():
    return generate_plan_service()


# GET LATEST PLAN BY USERID
@foods.route('/food/get_plan/<int:userID>', methods=["GET"])
def get_latest_plan_by_user_id(userID):
    return get_latest_plan_by_user_id_service(userID)


# RECOMMEND FOODS
@foods.route('/food/recommend/<path:BMI>', methods=["GET"])
def recommend_foods_by_bmi(BMI):
    BMI = float(BMI)
    return recommend_foods_by_bmi_service(BMI)


# GET IMG FOOD
@foods.route('/food/images/<fileName>', methods=["GET"])
def get_image(fileName):
    return get_image_service(fileName)


# UPLOAD IMG FOOD BY ID
@foods.route("/food/upload-img/<int:id>", methods=["PUT"])
@jwt_required()
def upload_img_food_by_id(id):
    current_role = get_jwt().get('role')
    if current_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return upload_img_food_by_id_service(id)


# GET FOOD BY ID
@foods.route("/food/<int:id>", methods=["GET"])
@swag_from("docs/get_food_by_id.yaml")
def get_food_by_id(id):
    return get_food_by_id_service(id)


# GET ALL FOODS
@foods.route("/foods", methods=["GET"])
@swag_from("docs/get_all_foods.yaml")
def get_all_foods():
    return get_all_foods_service()


# UPDATE FOOD BY ID
@foods.route("/food/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_food_by_id.yaml")
def update_food_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return update_food_by_id_service(id)


# DELETE FOOD BY ID
@foods.route("/food/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/delete_food_by_id.yaml")
def delete_food_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return delete_food_by_id_service(id)
