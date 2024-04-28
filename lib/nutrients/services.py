from flask import jsonify, request
from ..food_nutrition_ma import NutrientsSchema
from ..model import db, Nutrients, NatureNutrient, FoodNutrient
from sqlalchemy.sql import func
from sqlalchemy import event

nutrient = NutrientsSchema()
nutrients = NutrientsSchema(many=True)


def add_nutrient_service():
    data = request.json
    if data and all(key in data for key in('nutrientName', 'natureID', 'description', 'needed', 'function',
        'deficiencySigns', 'excessSigns', 'subjectInterest', 'shortagePrevention')) \
            and data['nutrientName'] and data['needed'] and data['function'] \
            and data['nutrientName'] != "" and data['function'] != "":
        nutrientName = data['nutrientName']
        natureID = data['natureID'] if data['natureID'] else None
        description = data['description'] if data['description'] else None
        needed = data['needed']
        function = data['function']
        deficiencySigns = data['deficiencySigns'] if data['deficiencySigns'] else None
        excessSigns = data['excessSigns'] if data['excessSigns'] else None
        subjectInterest = data['subjectInterest'] if data['subjectInterest'] else None
        shortagePrevention = data['shortagePrevention'] if data['shortagePrevention'] else None
        try:
            new_nutrient = Nutrients(nutrientName=nutrientName, natureID=natureID, description=description,
                                     needed=needed, function=function, deficiencySigns=deficiencySigns,
                                     excessSigns=excessSigns, subjectInterest=subjectInterest,
                                     shortagePrevention=shortagePrevention)

            db.session.add(new_nutrient)
            db.session.commit()

            # natureNutrient = NatureNutrient.query.get(new_nutrient.natureID)

            return jsonify({
                "nutrientID": new_nutrient.nutrientID,
                "nutrientName": new_nutrient.nutrientName,
                # "natureNutrient": natureNutrient.natureName if natureNutrient else None,
                "natureID": new_nutrient.natureID if new_nutrient.natureID else None,
                "description": new_nutrient.description if new_nutrient.description else None,
                "needed": new_nutrient.needed,
                "function": new_nutrient.function,
                "deficiencySigns": new_nutrient.deficiencySigns if new_nutrient.deficiencySigns else None,
                "excessSigns": new_nutrient.excessSigns if new_nutrient.excessSigns else None,
                "subjectInterest": new_nutrient.subjectInterest if new_nutrient.subjectInterest else None,
                "shortagePrevention": new_nutrient.shortagePrevention if new_nutrient.shortagePrevention else None,
                "created_date": new_nutrient.created_date.strftime("%Y-%m-%d"),
                "modified_date": new_nutrient.modified_date.strftime("%Y-%m-%d") if new_nutrient.modified_date else None
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add nutrient!"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_nutrient_by_id_service(id):
    try:
        nutrient = Nutrients.query.get(id)
        if nutrient:
            # natureNutrient = NatureNutrient.query.get(nutrient.natureID)
            return jsonify({
                "nutrientID": nutrient.nutrientID,
                "nutrientName": nutrient.nutrientName,
                "natureID": nutrient.natureID if nutrient.natureID else None,
                "description": nutrient.description if nutrient.description else None,
                "needed": nutrient.needed,
                "function": nutrient.function,
                "deficiencySigns": nutrient.deficiencySigns if nutrient.deficiencySigns else None,
                "excessSigns": nutrient.excessSigns if nutrient.excessSigns else None,
                "subjectInterest": nutrient.subjectInterest if nutrient.subjectInterest else None,
                "shortagePrevention": nutrient.shortagePrevention if nutrient.shortagePrevention else None,
                "created_date": nutrient.created_date.strftime("%Y-%m-%d"),
                "modified_date": nutrient.modified_date.strftime("%Y-%m-%d") if nutrient.modified_date else None
            }), 200
        else:
            return jsonify({"message": "Not found nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_all_nutrient_service():
    try:
        nutrients = Nutrients.query.all()
        if nutrients:
            list_nutrients = []
            for item in nutrients:
                # natureNutrient = NatureNutrient.query.get(item.natureID)
                list_nutrients.append({
                    "nutrientID": item.nutrientID,
                    "nutrientName": item.nutrientName,
                    "natureID": item.natureID if item.natureID else None,
                    "description": item.description if item.description else None,
                    "needed": item.needed,
                    "function": item.function,
                    "deficiencySigns": item.deficiencySigns if item.deficiencySigns else None,
                    "excessSigns": item.excessSigns if item.excessSigns else None,
                    "subjectInterest": item.subjectInterest if item.subjectInterest else None,
                    "shortagePrevention": item.shortagePrevention if item.shortagePrevention else None,
                    "created_date": item.created_date.strftime("%Y-%m-%d"),
                    "modified_date": item.modified_date.strftime("%Y-%m-%d") if item.modified_date else None
                })

            return jsonify(list_nutrients), 200
        else:
            return jsonify({"message": "Not found list of nutrients!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_nutrient_by_id_service(id):
    try:
        nutrient = Nutrients.query.get(id)
        data = request.json
        if nutrient:
            if data and all(key in data for key in ('nutrientName', 'natureID', 'description', 'needed', 'function',
                'deficiencySigns', 'excessSigns', 'subjectInterest', 'shortagePrevention')) \
                    and data['nutrientName'] and data['needed'] and data['function'] \
                    and data['nutrientName'] != "" and data['function'] != "":
                try:
                    nutrient.nutrientName = data['nutrientName']
                    nutrient.natureID = data['natureID'] if data['natureID'] else None
                    nutrient.description = data['description'] if data['description'] else None
                    nutrient.needed = data['needed']
                    nutrient.function = data['function']
                    nutrient.deficiencySigns = data['deficiencySigns'] if data['deficiencySigns'] else None
                    nutrient.excessSigns = data['excessSigns'] if data['excessSigns'] else None
                    nutrient.subjectInterest = data['subjectInterest'] if data['subjectInterest'] else None
                    nutrient.shortagePrevention = data['shortagePrevention'] if data['shortagePrevention'] else None

                    db.session.commit()

                    # natureNutrient = NatureNutrient.query.get(nutrient.natureID)

                    return jsonify({
                        "nutrientID": nutrient.nutrientID,
                        "nutrientName": nutrient.nutrientName,
                        "natureID": nutrient.natureID if nutrient.natureID else None,
                        "description": nutrient.description if nutrient.description else None,
                        "needed": nutrient.needed,
                        "function": nutrient.function,
                        "deficiencySigns": nutrient.deficiencySigns if nutrient.deficiencySigns else None,
                        "excessSigns": nutrient.excessSigns if nutrient.excessSigns else None,
                        "subjectInterest": nutrient.subjectInterest if nutrient.subjectInterest else None,
                        "shortagePrevention": nutrient.shortagePrevention if nutrient.shortagePrevention else None,
                        "created_date": nutrient.created_date.strftime("%Y-%m-%d"),
                        "modified_date": nutrient.modified_date.strftime("%Y-%m-%d")
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update nutrient!"}), 400
        else:
            return jsonify({"message": "Not found nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Sử dụng sự kiện before_delete để xóa tất cả các đối tượng FoodNutrient liên quan trước khi xóa đối tượng Nutrients
@event.listens_for(Nutrients, 'before_delete')
def delete_related_foodNutrient(mapper, connection, target):
    try:
        FoodNutrient.query.filter_by(nutrientID=target.nutrientID).delete()
        return True
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def delete_nutrient_by_id_service(id):
    try:
        nutrient = Nutrients.query.get(id)
        if nutrient:
            try:
                db.session.delete(nutrient)
                db.session.commit()

                return jsonify({"message": "Nutrient deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete nutrient!"}), 400
        else:
            return jsonify({"message": "Not found nutrient!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_nutrients_by_natureNutrient_service(natureNutrientName):
    try:
        nutrients = Nutrients.query.join(NatureNutrient, Nutrients.natureID == NatureNutrient.natureID)\
            .filter(func.lower(NatureNutrient.natureName) == natureNutrientName.lower()).all()

        if nutrients:
            list_nutrients = []
            for item in nutrients:
                # natureNutrient = NatureNutrient.query.get(item.natureID)

                list_nutrients.append({
                    "nutrientID": item.nutrientID,
                    "nutrientName": item.nutrientName,
                    "natureID": item.natureID if item.natureID else None,
                    "description": item.description if item.description else None,
                    "needed": item.needed,
                    "function": item.function,
                    "deficiencySigns": item.deficiencySigns if item.deficiencySigns else None,
                    "excessSigns": item.excessSigns if item.excessSigns else None,
                    "subjectInterest": item.subjectInterest if item.subjectInterest else None,
                    "shortagePrevention": item.shortagePrevention if item.shortagePrevention else None,
                    "created_date": item.created_date.strftime("%Y-%m-%d"),
                    "modified_date": item.modified_date.strftime("%Y-%m-%d") if item.modified_date else None
                })

            return jsonify(list_nutrients), 200
        else:
            return jsonify({"message": "Not found list of nutrients!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
