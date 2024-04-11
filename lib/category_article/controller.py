from flask import Blueprint
from .services import add_categoryArticle_service, get_all_categoryArticle_service, get_categoryArticle_by_id_service, \
    update_categoryArticle_by_id_service, delete_categoryArticle_by_id_service
from flasgger import swag_from

categoryArticle = Blueprint("categoryArticle", __name__, url_prefix="/api/categoryArticle-management")


@categoryArticle.route("/categoryArticle", methods=["POST"])
@swag_from("docs/add_categoryArticle.yaml")
def add_categoryArticle():
    return add_categoryArticle_service()


@categoryArticle.route("/categoryArticle/<int:id>", methods=["GET"])
@swag_from("docs/get_categoryArticle_by_id.yaml")
def get_categoryArticle_by_id(id):
    return get_categoryArticle_by_id_service(id)


@categoryArticle.route("/categoriesArticle", methods=["GET"])
@swag_from("docs/get_all_categoryArticle.yaml")
def get_all_categoryArticle():
    return get_all_categoryArticle_service()


@categoryArticle.route("/categoryArticle/<int:id>", methods=["PUT"])
@swag_from("docs/update_categoryArticle_by_id.yaml")
def update_categoryArticle_by_id(id):
    return update_categoryArticle_by_id_service(id)


@categoryArticle.route("/categoryArticle/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_categoryArticle_by_id.yaml")
def delete_categoryArticle_by_id(id):
    return delete_categoryArticle_by_id_service(id)

