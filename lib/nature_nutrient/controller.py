from flask import Blueprint, jsonify
from .services import add_natureNutrient_service, get_all_natureNutrient_service, get_natureNutrient_by_id_service, \
    update_natureNutrient_by_id_service, delete_natureNutrient_by_id_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt

natureNutrient = Blueprint("natureNutrient", __name__, url_prefix="/api/natureNutrient-management")


@natureNutrient.route("/natureNutrient", methods=["POST"])
@jwt_required()
@swag_from("docs/add_natureNutrient.yaml")
def add_natureNutrient():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return add_natureNutrient_service()


@natureNutrient.route("/natureNutrient/<int:id>", methods=["GET"])
@swag_from("docs/get_natureNutrient_by_id.yaml")
def get_natureNutrient_by_id(id):
    return get_natureNutrient_by_id_service(id)


@natureNutrient.route("/natureNutrients", methods=["GET"])
@swag_from("docs/get_all_natureNutrient.yaml")
def get_all_natureNutrient():
    return get_all_natureNutrient_service()


@natureNutrient.route("/natureNutrient/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_natureNutrient_by_id.yaml")
def update_natureNutrient_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return update_natureNutrient_by_id_service(id)


@natureNutrient.route("/natureNutrient/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/delete_natureNutrient_by_id.yaml")
def delete_natureNutrient_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return delete_natureNutrient_by_id_service(id)
