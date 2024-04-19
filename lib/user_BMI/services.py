from flask import request, jsonify
from ..model import db, User, UserBMI
from ..food_nutrition_ma import UserBMISchema
from sqlalchemy.sql import func


userBMI_schema = UserBMISchema()
userBMIs_schema = UserBMISchema(many=True)


def add_userBMI_service():
    data = request.json
    if data and ('userID' in data) and ('result' in data) and data['userID'] and data['result']:
        userID = data['userID']
        result = data['result']
        try:
            new_userBMI = UserBMI(userID=userID, result=result)

            db.session.add(new_userBMI)
            db.session.commit()

            user = User.query.get(new_userBMI.userID)

            return jsonify({
                "bmiId": new_userBMI.bmiId,
                "user": user.userName if user else None,
                "result": new_userBMI.result,
                "check_date": new_userBMI.check_date.strftime("%Y-%m-%d")
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add user's BMI"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_userBMI_by_id_service(id):
    try:
        user_bmi = UserBMI.query.get(id)
        if user_bmi:
            user = User.query.get(user_bmi.userID)

            return jsonify({
                "bmiId": user_bmi.bmiId,
                "user": user.userName if user else None,
                "result": user_bmi.result,
                "check_date": user_bmi.check_date.strftime("%Y-%m-%d")
            }), 200
        else:
            return jsonify({"message": "Not found user's BMI!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_all_userBMI_service():
    try:
        user_bmis = UserBMI.query.all()
        if user_bmis:
            list_userBMIs = []
            for user_bmi in user_bmis:
                user = User.query.get(user_bmi.userID)

                list_userBMIs.append({
                    "bmiId": user_bmi.bmiId,
                    "user": user.userName if user else None,
                    "result": user_bmi.result,
                    "check_date": user_bmi.check_date.strftime("%Y-%m-%d")
                })

            return jsonify(list_userBMIs), 200
            # return userBMIs_schema.jsonify(user_bmis), 200
        else:
            return jsonify({"message": "Not found user's BMI!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_userBMI_by_id_service(id):
    try:
        user_bmi = UserBMI.query.get(id)
        data = request.json
        if user_bmi:
            if data and ('userID' in data) and ('result' in data) and data['userID'] and data['result']:
                try:
                    user_bmi.userID = data['userID']
                    user_bmi.result = data['result']

                    db.session.commit()

                    user = User.query.get(user_bmi.userID)

                    return jsonify({
                        "bmiId": user_bmi.bmiId,
                        "user": user.userName if user else None,
                        "result": user_bmi.result,
                        "check_date": user_bmi.check_date.strftime("%Y-%m-%d")
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update user's BMI!"}), 400
        else:
            return jsonify({"message": "Not found user's BMI!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def delete_userBMI_by_id_service(id):
    try:
        user_bmi = UserBMI.query.get(id)
        if user_bmi:
            try:
                db.session.delete(user_bmi)
                db.session.commit()

                return jsonify({"message": "User's BMI deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete user's BMI!"}), 400
        else:
            return jsonify({"message": "Not found user's BMI!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_userBMI_by_userName_service(userName):
    try:
        user_bmis = UserBMI.query.join(User, UserBMI.userID == User.userID)\
            .filter(func.lower(User.userName) == userName.lower()).all()
        if user_bmis:
            list_userBMIs = []
            for user_bmi in user_bmis:
                user = User.query.get(user_bmi.userID)

                list_userBMIs.append({
                    "bmiId": user_bmi.bmiId,
                    "user": user.userName if user else None,
                    "result": user_bmi.result,
                    "check_date": user_bmi.check_date.strftime("%Y-%m-%d")
                })

                return jsonify(list_userBMIs), 200
        else:
            return jsonify({"message": "Not found user's BMI!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
