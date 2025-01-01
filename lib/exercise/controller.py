from flask import Blueprint, jsonify
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt
from .services import add_exercise_service, update_exercise_by_id_service, get_all_exercises_service, \
    get_exercise_by_id_service, delete_exercise_by_id_service


exercise = Blueprint("exercise", __name__, url_prefix="/api/exercise-management")

@exercise.route("/exercise", methods=["POST"])
@jwt_required()
def add_exercise():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({"message": "Permission denied"}), 403

    return add_exercise_service()


@exercise.route("/exercise/<int:id>", methods=["PUT"])
@jwt_required()
def update_exercise_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({"message": "Permission denied"}), 403

    return update_exercise_by_id_service(id)


@exercise.route("/exercise/<int:id>", methods=["GET"])
def get_exercise_by_id(id):
    return get_exercise_by_id_service(id)


@exercise.route("/exercises", methods=["GET"])
def get_all_exercises():
    return get_all_exercises_service()


@exercise.route("/exercise/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_exercise_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({"message": "Permission denied"}), 403

    return delete_exercise_by_id_service(id)