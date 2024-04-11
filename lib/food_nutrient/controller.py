from flask import Blueprint
from .services import add_foodNutrient_service, get_all_foodNutrient_service, get_foodNutrient_by_foodID_service, \
    get_foodNutrient_by_nutrientID_service, update_foodNutrient_service, delete_foodNutrient_service
from flasgger import swag_from

foodNutrient = Blueprint("foodNutrient", __name__, url_prefix="/api/foodNutrient-management")


@foodNutrient.route("/foodNutrient", methods=["POST"])
@swag_from("docs/add_foodNutrient.yaml")
def add_foodNutrient():
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
@swag_from("docs/update_foodNutrient.yaml")
def update_foodNutrient(foodID, nutrientID):
    return update_foodNutrient_service(foodID, nutrientID)


@foodNutrient.route("/foodNutrient/<int:foodID>/<int:nutrientID>", methods=["DELETE"])
@swag_from("docs/delete_foodNutrient.yaml")
def delete_foodNutrient(foodID, nutrientID):
    return delete_foodNutrient_service(foodID, nutrientID)
