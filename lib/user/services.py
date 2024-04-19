from ..model import db, User, UserBMI
from ..food_nutrition_ma import UserSchema
from flask import request, jsonify
from sqlalchemy.sql import func
from datetime import date, datetime
from sqlalchemy import event

user_schema = UserSchema()
users_schema = UserSchema(many=True)


def get_list_user_bmi_by_userID(userID):
    user_bmi = UserBMI.query.filter_by(userID=userID).all()
    # print(user_bmi)

    list_user_bmi = []

    if user_bmi:
        for user_bmi in user_bmi:
            list_user_bmi.append({
                "bmiId": user_bmi.bmiId,
                "result": user_bmi.result,
                "check_date": user_bmi.check_date.strftime("%Y-%m-%d")
            })

            return list_user_bmi
    else:
        return None


def login_user_service():
    data = request.json
    if data and all(key in data for key in ('userName', 'password')) and data['userName'] and data['password'] \
        and data['userName'] != "" and data['password'] != "":
        userName = data['userName']
        password = data['password']

        user = User.query.filter_by(userName=userName, password=password).first()

        if user:
            list_user_bmi = get_list_user_bmi_by_userID(user.userID)

            return jsonify({
                "userID": user.userID,
                "userName": user.userName,
                "fullName": user.fullName if user.fullName else None,
                "image": user.image if user.image else None,
                "dateBirth": user.dateBirth.strftime("%Y-%m-%d"),
                "email": user.email,
                "phone": user.phone if user.phone else None,
                "address": user.address if user.address else None,
                "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
            }), 200
        else:
            return jsonify({"message": "Incorrect username or password!"}), 404
    else:
        return jsonify({"message": "Login error!"}), 400


def add_user_service():
    data = request.json
    if data and all(key in data for key in ('userName', 'fullName', 'image', 'password', 'dateBirth', 'email',
        'phone', 'address')) and data['userName'] and data['password'] and data['dateBirth'] and data['email'] \
        and data['userName'] != "" and data['password'] != "" and data['dateBirth'] != "" and data['email'] != "":
        userName = data['userName']
        fullName = data['fullName'] if data['fullName'] else None
        image = data['image'] if data['image'] else None
        password = data['password']
        date_list = data['dateBirth'].split('-')
        dateBirth = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        email = data['email']
        phone = data['phone'] if data['phone'] else None
        address = data['address'] if data['address'] else None
        try:
            new_user = User(userName=userName, fullName=fullName, image=image, password=password, dateBirth=dateBirth,
                            email=email, phone=phone, address=address)

            db.session.add(new_user)
            db.session.commit()

            list_user_bmi = get_list_user_bmi_by_userID(new_user.userID)

            return jsonify({
                "userID": new_user.userID,
                "userName": new_user.userName,
                "fullName": new_user.fullName if new_user.fullName else None,
                "image": new_user.image if new_user.image else None,
                "dateBirth": new_user.dateBirth.strftime("%Y-%m-%d"),
                "email": new_user.email,
                "phone": new_user.phone if new_user.phone else None,
                "address": new_user.address if new_user.address else None,
                "dateJoining": new_user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": new_user.modified_date.strftime("%Y-%m-%d") if new_user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add new user!"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_user_by_id_service(id):
    try:
        user = User.query.get(id)
        if user:
            list_user_bmi = get_list_user_bmi_by_userID(user.userID)

            return jsonify({
                "userID": user.userID,
                "userName": user.userName,
                "fullName": user.fullName if user.fullName else None,
                "image": user.image if user.image else None,
                "dateBirth": user.dateBirth.strftime("%Y-%m-%d"),
                "email": user.email,
                "phone": user.phone if user.phone else None,
                "address": user.address if user.address else None,
                "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
            }), 200
        else:
            return jsonify({"message": "Not found user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_all_user_service():
    try:
        users = User.query.all()
        if users:
            user_list = []
            for user in users:
                list_user_bmi = get_list_user_bmi_by_userID(user.userID)

                user_list.append({
                    "userID": user.userID,
                    "userName": user.userName,
                    "fullName": user.fullName if user.fullName else None,
                    "image": user.image if user.image else None,
                    "dateBirth": user.dateBirth.strftime("%Y-%m-%d"),
                    "email": user.email,
                    "phone": user.phone if user.phone else None,
                    "address": user.address if user.address else None,
                    "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                    "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
                    "list_user_bmi": list_user_bmi if list_user_bmi else []
                })
            return jsonify(user_list), 200
        else:
            return jsonify({"message": "Not found list of user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_user_by_id_service(id):
    try:
        user = User.query.get(id)
        data = request.json
        if user:
            if data and all(key in data for key in ('userName', 'fullName', 'image', 'password', 'dateBirth', 'email',
                'phone', 'address')) and data['userName'] and data['password'] and data['dateBirth'] and data['email'] \
                and data['userName'] != "" and data['password'] != "" and data['dateBirth'] != "" and data['email'] != "":
                try:
                    user.userName = data['userName']
                    user.fullName = data['fullName'] if data['fullName'] else None
                    user.image = data['image'] if data['image'] else None
                    user.password = data['password']
                    date_list = data['dateBirth'].split('-')
                    user.dateBirth = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
                    user.email = data['email']
                    user.phone = data['phone'] if data['phone'] else None
                    user.address = data['address'] if data['address'] else None

                    db.session.commit()

                    list_user_bmi = get_list_user_bmi_by_userID(user.userID)

                    return jsonify({
                        "userID": user.userID,
                        "userName": user.userName,
                        "fullName": user.fullName,
                        "image": user.image,
                        "dateBirth": user.dateBirth.strftime("%Y-%m-%d"),
                        "email": user.email,
                        "phone": user.phone,
                        "address": user.address,
                        "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                        "modified_date": user.modified_date.strftime("%Y-%m-%d"),
                        "list_user_bmi": list_user_bmi if list_user_bmi else []
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update user!"}), 400
        else:
            return jsonify({"message": "Not found user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Sử dụng sự kiện before_delete để xóa tất cả các đối tượng UserBMI liên quan trước khi xóa đối tượng User
@event.listens_for(User, 'before_delete')
def delete_related_bmis(mapper, connection, target):
    try:
        UserBMI.query.filter_by(userID=target.userID).delete()
        return True
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def delete_user_by_id_service(id):
    try:
        user = User.query.get(id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()

                return jsonify({"message": "User deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete user!"}), 400
        else:
            return jsonify({"message": "Not found user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
