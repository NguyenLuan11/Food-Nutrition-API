from flask import Blueprint, jsonify
from .services import register_user_service, get_all_user_service, get_user_by_id_service, \
    update_user_by_id_service, delete_user_by_id_service, login_user_service, refresh_token_service, \
    update_image_avt_user_by_id_service, update_state_user_by_id_service, get_user_by_name_service, get_user_by_email_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt

user = Blueprint("user", __name__, url_prefix="/api/user-management")


@user.route("/login", methods=["POST"])
@swag_from("docs/login_user.yaml")
def login_user():
    return login_user_service()


@user.route("/refresh-token", methods=["POST"])
@jwt_required(refresh=True)
@swag_from("docs/refresh_token.yaml")
def refresh_token():
    current_user_role = get_jwt().get('role')
    if current_user_role != 'user':
        return jsonify({'message': 'Permission denied'}), 403

    return refresh_token_service()


@user.route("/register", methods=["POST"])
@swag_from("docs/register_user.yaml")
def register_user():
    return register_user_service()


@user.route("/upload-avt", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_image_avt_user_by_id.yaml")
def update_image_avt_user_by_id(id):
    current_user_role = get_jwt().get('role')
    if current_user_role != 'user':
        return jsonify({'message': 'Permission denied'}), 403

    return update_image_avt_user_by_id_service(id)


@user.route("/user/state/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_state_user_by_id.yaml")
def update_state_user_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return update_state_user_by_id_service(id)


@user.route("/user/<int:id>", methods=["GET"])
@swag_from("docs/get_user_by_id.yaml")
def get_user_by_id(id):
    return get_user_by_id_service(id)


@user.route("/user/<string:userName>", methods=["GET"])
@swag_from("docs/get_user_by_name.yaml")
def get_user_by_name(userName):
    return get_user_by_name_service(userName)


@user.route("/user/<string:email>", methods=["GET"])
@swag_from("docs/get_user_by_email.yaml")
def get_user_by_email(email):
    return get_user_by_email_service(email)


@user.route("/users", methods=["GET"])
@jwt_required()
@swag_from("docs/get_all_users.yaml")
def get_all_users():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return get_all_user_service()


@user.route("/user/<int:id>", methods=["PUT"])
@swag_from("docs/update_user_by_id.yaml")
def update_user_by_id(id):
    return update_user_by_id_service(id)


@user.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/delete_user_by_id.yaml")
def delete_user_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return delete_user_by_id_service(id)
