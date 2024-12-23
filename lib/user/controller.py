from flask import Blueprint, jsonify
from .services import register_user_service, get_all_user_service, get_user_by_id_service, \
    update_user_by_id_service, delete_user_by_id_service, login_user_service, refresh_token_service, \
    update_image_avt_user_by_id_service, update_state_user_by_id_service, get_user_by_name_service, \
    get_user_by_email_gg_service, add_user_service, get_image_service, check_correct_pass_by_id_service, \
    update_pass_by_id_service, send_otp_service, verify_otp_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt

user = Blueprint("user", __name__, url_prefix="/api/user-management")


@user.route('/send-otp', methods=['POST'])
def send_otp():
    return send_otp_service()

@user.route('/verify-otp', methods=['POST'])
def verify_otp():
    return verify_otp_service()


# CHECK PASS USER
@user.route('/user/checkpass/<int:id>', methods=["POST"])
def check_correct_pass_by_id(id):
    return check_correct_pass_by_id_service(id)


# UPDATE PASS USER BY ID
@user.route('/user/updatepass/<int:id>', methods=["PUT"])
def update_pass_by_id(id):
    return update_pass_by_id_service(id)


# LOGIN
@user.route("/login", methods=["POST"])
@swag_from("docs/login_user.yaml")
def login_user():
    return login_user_service()


# REFRESH TOKEN
@user.route("/refresh-token", methods=["POST"])
@jwt_required(refresh=True)
@swag_from("docs/refresh_token.yaml")
def refresh_token():
    current_user_role = get_jwt().get('role')
    if current_user_role != 'user':
        return jsonify({'message': 'Permission denied'}), 403

    return refresh_token_service()


# REGISTER
@user.route("/register", methods=["POST"])
@swag_from("docs/register_user.yaml")
def register_user():
    return register_user_service()


# ADD NEW USER
@user.route("/add", methods=["POST"])
@swag_from("docs/add_user.yaml")
def add_user():
    return add_user_service()


# UPDATE AVT USER BY ID
@user.route("/user/upload-avt/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_image_avt_user_by_id.yaml")
def update_image_avt_user_by_id(id):
    current_user_role = get_jwt().get('role')
    if current_user_role != 'user':
        return jsonify({'message': 'Permission denied'}), 403

    return update_image_avt_user_by_id_service(id)


# GET AVT USER
@user.route('/user/images/<fileName>', methods=["GET"])
def get_image(fileName):
    return get_image_service(fileName)


# UPDATE USER'S STATE BY ID
@user.route("/user/state/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_state_user_by_id.yaml")
def update_state_user_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return update_state_user_by_id_service(id)


# GET USER BY ID
@user.route("/user/<int:id>", methods=["GET"])
@swag_from("docs/get_user_by_id.yaml")
def get_user_by_id(id):
    return get_user_by_id_service(id)


# GET USER BY NAME
@user.route("/user/<string:userName>", methods=["GET"])
@swag_from("docs/get_user_by_name.yaml")
def get_user_by_name(userName):
    return get_user_by_name_service(userName)


# GET USER BY EMAIL GG
@user.route("/user/<string:userName>/<string:email>", methods=["GET"])
@swag_from("docs/get_user_by_email_gg.yaml")
def get_user_by_email_gg(userName, email):
    return get_user_by_email_gg_service(userName, email)


# GET ALL USERS
@user.route("/users", methods=["GET"])
@jwt_required()
@swag_from("docs/get_all_users.yaml")
def get_all_users():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return get_all_user_service()


# UPDATE USER BY ID
@user.route("/user/<int:id>", methods=["PUT"])
@swag_from("docs/update_user_by_id.yaml")
def update_user_by_id(id):
    return update_user_by_id_service(id)


# DELETE USER BY ID
@user.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/delete_user_by_id.yaml")
def delete_user_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return delete_user_by_id_service(id)
