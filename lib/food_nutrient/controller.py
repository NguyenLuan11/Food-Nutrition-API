from flask import Blueprint, jsonify
from .services import add_foodNutrient_service, get_all_foodNutrient_service, get_foodNutrient_by_foodID_service, \
    get_foodNutrient_by_nutrientID_service, update_foodNutrient_service, delete_foodNutrient_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt

foodNutrient = Blueprint("foodNutrient", __name__, url_prefix="/api/foodNutrient-management")


@foodNutrient.route("/foodNutrient", methods=["POST"])
@jwt_required()
@swag_from("docs/add_foodNutrient.yaml")
def add_foodNutrient():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return add_foodNutrient_service()


@foodNutrient.route("/foodNutrients", methods=["GET"])
@swag_from("docs/get_all_foodNutrient.yaml")
def get_all_foodNutrient():
    return get_all_foodNutrient_service()


@foodNutrient.route("/foodNutrient/<int:foodID>", methods=["GET"])
@swag_from("docs/get_foodNutrient_by_foodID.yaml")
def get_foodNutrient_by_foodID(foodID):
    return get_foodNutrient_by_foodID_service(foodID)


@foodNutrient.route("/foodNutrient/<int:nutrientID>", methods=["GET"])
@swag_from("docs/get_foodNutrient_by_nutrientID.yaml")
def get_foodNutrient_by_nutrientID(nutrientID):
    return get_foodNutrient_by_nutrientID_service(nutrientID)


@foodNutrient.route("/foodNutrient/<int:foodID>/<int:nutrientID>", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_foodNutrient.yaml")
def update_foodNutrient(foodID, nutrientID):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return update_foodNutrient_service(foodID, nutrientID)


@foodNutrient.route("/foodNutrient/<int:foodID>/<int:nutrientID>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/delete_foodNutrient.yaml")
def delete_foodNutrient(foodID, nutrientID):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return delete_foodNutrient_service(foodID, nutrientID)
