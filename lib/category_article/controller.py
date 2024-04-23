from flask import Blueprint, jsonify
from .services import add_categoryArticle_service, get_all_categoryArticle_service, get_categoryArticle_by_id_service, \
    update_categoryArticle_by_id_service, delete_categoryArticle_by_id_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt

categoryArticle = Blueprint("categoryArticle", __name__, url_prefix="/api/categoryArticle-management")


@categoryArticle.route("/categoryArticle", methods=["POST"])
@jwt_required()
@swag_from("docs/add_categoryArticle.yaml")
def add_categoryArticle():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

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
@jwt_required()
@swag_from("docs/update_categoryArticle_by_id.yaml")
def update_categoryArticle_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return update_categoryArticle_by_id_service(id)


@categoryArticle.route("/categoryArticle/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/delete_categoryArticle_by_id.yaml")
def delete_categoryArticle_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return delete_categoryArticle_by_id_service(id)

