from flask import Blueprint
from .services import add_userBMI_service, get_userBMI_by_userName_service, get_all_userBMI_service, \
    get_userBMI_by_id_service, update_userBMI_by_id_service, delete_userBMI_by_id_service
from flasgger import swag_from

userBMI = Blueprint("userBMI", __name__, url_prefix="/api/userBMI-management")


@userBMI.route("/userBMI", methods=["POST"])
@swag_from("docs/add_userBMI.yaml")
def add_userBMI():
    return add_userBMI_service()


@userBMI.route("/userBMIs", methods=["GET"])
@swag_from("docs/get_all_userBMI.yaml")
def get_all_userBMI():
    return get_all_userBMI_service()


@userBMI.route("/userBMI/<string:userName>", methods=["GET"])
@swag_from("docs/get_userBMI_by_userName.yaml")
def get_userBMI_by_userName(userName):
    return get_userBMI_by_userName_service(userName)


@userBMI.route("/userBMI/<int:id>", methods=["GET"])
@swag_from("docs/get_userBMI_by_id.yaml")
def get_userBMI_by_id(id):
    return get_userBMI_by_id_service(id)


@userBMI.route("/userBMI/<int:id>", methods=["PUT"])
@swag_from("docs/update_userBMI_by_id.yaml")
def update_userBMI_by_id(id):
    return update_userBMI_by_id_service(id)


@userBMI.route("/userBMI/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_userBMI_by_id.yaml")
def delete_userBMI_by_id(id):
    return delete_userBMI_by_id_service(id)
