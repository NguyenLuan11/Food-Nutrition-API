from flask import Blueprint
from .services import add_nutrient_service, get_all_nutrient_service, get_nutrient_by_id_service, \
    get_nutrients_by_natureNutrient_service, update_nutrient_by_id_service, delete_nutrient_by_id_service
from flasgger import swag_from

nutrients = Blueprint("nutrients", __name__, url_prefix="/api/nutrients-management")


@nutrients.route("/nutrient", methods=["POST"])
@swag_from("docs/add_nutrient.yaml")
def add_nutrient():
    return add_nutrient_service()


@nutrients.route("/nutrient/<int:id>", methods=["GET"])
@swag_from("docs/get_nutrient_by_id.yaml")
def get_nutrient_by_id(id):
    return get_nutrient_by_id_service(id)


@nutrients.route("/nutrients", methods=["GET"])
@swag_from("docs/get_all_nutrients.yaml")
def get_all_nutrients():
    return get_all_nutrient_service()


@nutrients.route("/nutrient/<int:id>", methods=["PUT"])
@swag_from("docs/update_nutrient_by_id.yaml")
def update_nutrient_by_id(id):
    return update_nutrient_by_id_service(id)


@nutrients.route("/nutrient/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_nutrient_by_id.yaml")
def delete_nutrient_by_id(id):
    return delete_nutrient_by_id_service(id)


@nutrients.route("/nutrient/<string:natureNutrientName>", methods=["GET"])
@swag_from("docs/get_nutrients_by_natureNutrient.yaml")
def get_nutrients_by_natureNutrient(natureNutrientName):
    return get_nutrients_by_natureNutrient_service(natureNutrientName)

