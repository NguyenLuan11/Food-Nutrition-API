from flask import Blueprint
from .services import add_user_service, get_all_user_service, get_user_by_id_service, \
    update_user_by_id_service, delete_user_by_id_service, login_user_service, refresh_token_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required

user = Blueprint("user", __name__, url_prefix="/api/user-management")


@user.route("/login", methods=["POST"])
@swag_from("docs/login_user.yaml")
def login_user():
    return login_user_service()


@user.route("/refresh_token", methods=["POST"])
@jwt_required(refresh=True)
@swag_from("docs/refresh_token.yaml")
def refresh_token():
    return refresh_token_service()


@user.route("/user", methods=["POST"])
@swag_from("docs/add_user.yaml")
def add_user():
    return add_user_service()


@user.route("/user/<int:id>", methods=["GET"])
@swag_from("docs/get_user_by_id.yaml")
def get_user_by_id(id):
    return get_user_by_id_service(id)


@user.route("/users", methods=["GET"])
@swag_from("docs/get_all_users.yaml")
def get_all_users():
    return get_all_user_service()


@user.route("/user/<int:id>", methods=["PUT"])
@swag_from("docs/update_user_by_id.yaml")
def update_user_by_id(id):
    return update_user_by_id_service(id)


@user.route("/user/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_user_by_id.yaml")
def delete_user_by_id(id):
    return delete_user_by_id_service(id)
