from flask import Blueprint
from .services import add_admin_service, get_admin_by_id_service, get_all_admin_service, update_admin_by_id_service, \
    delete_admin_by_id_service, login_admin_service
from flasgger import swag_from

admin = Blueprint("admin", __name__, url_prefix="/api/admin-management")


@admin.route("/login", methods=["POST"])
@swag_from("docs/login_admin.yaml")
def login_admin():
    return login_admin_service()


# ADD NEW ADMIN
@admin.route("/admin", methods=["POST"])
@swag_from("docs/add_admin.yaml")
def add_admin():
    return add_admin_service()


# UPDATE ADMIN BY ID
@admin.route("/admin/<int:id>", methods=["PUT"])
@swag_from("docs/update_admin_by_id.yaml")
def update_admin_by_id(id):
    return update_admin_by_id_service(id)


# GET ADMIN BY ID
@admin.route("/admin/<int:id>", methods=["GET"])
@swag_from("docs/get_admin_by_id.yaml")
def get_admin_by_id(id):
    return get_admin_by_id_service(id)


# GET ALL ADMIN
@admin.route("/admins", methods=["GET"])
@swag_from("docs/get_all_admin.yaml")
def get_all_admin():
    return get_all_admin_service()


# DELETE ADMIN BY ID
@admin.route("/admin/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_admin_by_id.yaml")
def delete_admin_by_id(id):
    return delete_admin_by_id_service(id)
