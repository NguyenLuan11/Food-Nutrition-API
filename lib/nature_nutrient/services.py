from flask import jsonify, request
from ..food_nutrition_ma import NatureNutrientSchema
from ..model import db, NatureNutrient, Nutrients
from sqlalchemy import event


natureNutrient_schema = NatureNutrientSchema()
natureNutrients_schema = NatureNutrientSchema(many=True)


def add_natureNutrient_service():
    data = request.json
    if data and ('natureName' in data) and data['natureName'] and data['natureName'] != "":
        natureName = data['natureName']
        try:
            new_natureNutrient = NatureNutrient(natureName=natureName)

            db.session.add(new_natureNutrient)
            db.session.commit()

            return jsonify({
                "natureID": new_natureNutrient.natureID,
                "natureName": new_natureNutrient.natureName
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add nature nutrient!"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_natureNutrient_by_id_service(id):
    try:
        natureNutrient = NatureNutrient.query.get(id)
        if natureNutrient:
            return jsonify({
                "natureID": natureNutrient.natureID,
                "natureName": natureNutrient.natureName
            }), 200
        else:
            return jsonify({"message": "Not found nature nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_all_natureNutrient_service():
    try:
        natureNutrients = NatureNutrient.query.all()
        if natureNutrients:
            list_natureNutrient = []
            for natureNutrient in natureNutrients:
                list_natureNutrient.append({
                    "natureID": natureNutrient.natureID,
                    "natureName": natureNutrient.natureName
                })

            return jsonify(list_natureNutrient), 200
        else:
            return jsonify({"message": "Not found list of nature nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_natureNutrient_by_id_service(id):
    try:
        natureNutrient = NatureNutrient.query.get(id)
        data = request.json
        if natureNutrient:
            if data and ('natureName' in data) and data['natureName'] and data['natureName'] != "":
                try:
                    natureNutrient.natureName = data['natureName']

                    db.session.commit()

                    return jsonify({
                        "natureID": natureNutrient.natureID,
                        "natureName": natureNutrient.natureName
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update nature nutrient!"}), 400
        else:
            return jsonify({"message": "Not found nature nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Sử dụng sự kiện before_delete để xóa tất cả các đối tượng Nutrients liên quan trước khi xóa đối tượng NatureNutrient
@event.listens_for(NatureNutrient, 'before_delete')
def delete_related_nutrients(mapper, connection, target):
    try:
        Nutrients.query.filter_by(natureID=target.natureID).delete()
        return True
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def delete_natureNutrient_by_id_service(id):
    try:
        natureNutrient = NatureNutrient.query.get(id)
        if natureNutrient:
            try:
                db.session.delete(natureNutrient)
                db.session.commit()
                return jsonify({"message": "Nature nutrient deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete nature nutrient!"}), 400
        else:
            return jsonify({"message": "Not found nature nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
