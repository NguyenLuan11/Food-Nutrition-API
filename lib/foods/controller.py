from flask import Blueprint
from .services import add_foods_service, get_food_by_id_service, get_all_foods_service, update_food_by_id_service, \
    delete_food_by_id_service
from flasgger import swag_from

foods = Blueprint("foods", __name__, url_prefix="/api/foods-management")


@foods.route("/food", methods=["POST"])
@swag_from("docs/add_food.yaml")
def add_foods():
    return add_foods_service()


@foods.route("/food/<int:id>", methods=["GET"])
@swag_from("docs/get_food_by_id.yaml")
def get_food_by_id(id):
    return get_food_by_id_service(id)


@foods.route("/foods", methods=["GET"])
@swag_from("docs/get_all_foods.yaml")
def get_all_foods():
    return get_all_foods_service()


@foods.route("/food/<int:id>", methods=["PUT"])
@swag_from("docs/update_food_by_id.yaml")
def update_food_by_id(id):
    return update_food_by_id_service(id)


@foods.route("/food/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_food_by_id.yaml")
def delete_food_by_id(id):
    return delete_food_by_id_service(id)
