from flask import request, jsonify
from ..model import db, Exercise


def add_exercise_service():
    data = request.json
    if not data or 'nameExercise' not in data or 'kind' not in data or not data['nameExercise'] or not data['kind']:
        return jsonify({"message": "Request error! Missing or invalid data!"}), 400

    nameExercise = data['nameExercise']
    kind = data['kind']

    try:
        newExercise = Exercise(nameExercise=nameExercise, kind=kind)
        db.session.add(newExercise)
        db.session.commit()

        return jsonify({
            "id": newExercise.id,
            "nameExercise": newExercise.nameExercise,
            "kind": newExercise.kind,
            "created_date": newExercise.created_date.strftime("%Y-%m-%d"),
            "modified_date": newExercise.modified_date.strftime("%Y-%m-%d") if newExercise.modified_date else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add new exercise!", "error": str(e)}), 500


def update_exercise_by_id_service(id):
    data = request.json
    if not data or 'nameExercise' not in data or 'kind' not in data or not data['nameExercise'] or not data['kind']:
        return jsonify({"message": "Request error! Missing or invalid data!"}), 400

    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"message": "Exercise not found!"}), 404

    nameExercise = data.get('nameExercise', exercise.nameExercise)
    kind = data.get('kind', exercise.kind)

    try:
        exercise.nameExercise = nameExercise
        exercise.kind = kind
        db.session.commit()

        return jsonify({
            "id": exercise.id,
            "nameExercise": exercise.nameExercise,
            "kind": exercise.kind,
            "created_date": exercise.created_date.strftime("%Y-%m-%d"),
            "modified_date": exercise.modified_date.strftime("%Y-%m-%d") if exercise.modified_date else None
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update exercise!", "error": str(e)}), 500


def get_exercise_by_id_service(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"message": "Exercise not found!"}), 404

    return jsonify({
        "id": exercise.id,
        "nameExercise": exercise.nameExercise,
        "kind": exercise.kind,
        "created_date": exercise.created_date.strftime("%Y-%m-%d"),
        "modified_date": exercise.modified_date.strftime("%Y-%m-%d") if exercise.modified_date else None
    }), 200


def get_all_exercises_service():
    try:
        exercises = Exercise.query.all()
        results = [
            {
                "id": exercise.id,
                "nameExercise": exercise.nameExercise,
                "kind": exercise.kind,
                "created_date": exercise.created_date.strftime("%Y-%m-%d"),
                "modified_date": exercise.modified_date.strftime("%Y-%m-%d") if exercise.modified_date else None
            } for exercise in exercises
        ]

        return jsonify(results), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch exercises!", "error": str(e)}), 500


def delete_exercise_by_id_service(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"message": "Exercise not found!"}), 404

    try:
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete exercise!", "error": str(e)}), 500
