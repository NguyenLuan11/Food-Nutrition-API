from ..model import db, User, UserBMI
from ..food_nutrition_ma import UserSchema
from flask import request, jsonify, send_from_directory, abort
from sqlalchemy.sql import func
from datetime import date, datetime
from sqlalchemy import event
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from ..config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_USERS

user_schema = UserSchema()
users_schema = UserSchema(many=True)

UPLOAD_FOLDER_USERS = os.path.join(os.getcwd(), UPLOAD_FOLDER_USERS)


# GET LIST USER BMI BY ID
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


# LOGIN
def login_user_service():
    data = request.json
    if data and all(key in data for key in ('userName', 'password')) and data['userName'] and data['password'] \
            and data['userName'] != "" and data['password'] != "":
        userName = data['userName'].strip()
        password = data['password'].strip()

        user = User.query.filter_by(userName=userName, password=password).first()

        if user:
            # Tạo Access Token và Refresh Token
            access_token = create_access_token(identity=user.userName, additional_claims={'role': 'user'})
            refresh_token = create_refresh_token(identity=user.userName, additional_claims={'role': 'user'})

            list_user_bmi = get_list_user_bmi_by_userID(user.userID)

            return jsonify({
                "userID": user.userID,
                "userName": user.userName,
                "fullName": user.fullName if user.fullName else None,
                "image": user.image if user.image else None,
                "dateBirth": user.dateBirth.strftime("%Y-%m-%d") if user.dateBirth else None,
                "email": user.email,
                "phone": user.phone if user.phone else None,
                "address": user.address if user.address else None,
                "state": user.state,
                "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else [],
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"message": "Incorrect username or password!"}), 404
    else:
        return jsonify({"message": "Login error!"}), 400


# REFRESH TOKEN
def refresh_token_service():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, additional_claims={'role': 'user'})

    return jsonify(access_token=new_access_token), 200


# GET USER INFOR BY ACCESS TOKEN
def get_user_infor_by_access_token_service():
    current_user = get_jwt_identity()
    user = User.query.filter_by(userName=current_user).first()
    if user:
        list_user_bmi = get_list_user_bmi_by_userID(user.userID)

        return jsonify({
            "userID": user.userID,
            "userName": user.userName,
            "fullName": user.fullName if user.fullName else None,
            "image": user.image if user.image else None,
            "dateBirth": user.dateBirth.strftime("%Y-%m-%d") if user.dateBirth else None,
            "email": user.email,
            "phone": user.phone if user.phone else None,
            "address": user.address if user.address else None,
            "state": user.state,
            "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
            "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
            "list_user_bmi": list_user_bmi if list_user_bmi else []
        }), 200


# REGISTER
def register_user_service():
    data = request.json
    if data and all(key in data for key in ('userName', 'password', 'dateBirth', 'email')) \
            and data['userName'] and data['email'] \
            and data['userName'] != "" and data['password'] != "" and data['dateBirth'] != "" and data['email'] != "":
        userName = data['userName'].strip()
        email = data['email'].strip()

        password = data['password'].strip() if data['password'] else None
        date_list = data['dateBirth'].split('-') if data['dateBirth'] else None
        dateBirth = None
        if date_list:
            dateBirth = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))

        try:
            new_user = User(userName=userName, fullName=None, image=None, password=password, dateBirth=dateBirth,
                            email=email, phone=None, address=None)

            db.session.add(new_user)
            db.session.commit()

            list_user_bmi = get_list_user_bmi_by_userID(new_user.userID)

            return jsonify({
                "userID": new_user.userID,
                "userName": new_user.userName,
                "fullName": new_user.fullName if new_user.fullName else None,
                "image": new_user.image if new_user.image else None,
                "dateBirth": new_user.dateBirth.strftime("%Y-%m-%d") if new_user.dateBirth else None,
                "email": new_user.email,
                "phone": new_user.phone if new_user.phone else None,
                "address": new_user.address if new_user.address else None,
                "state": new_user.state,
                "dateJoining": new_user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": new_user.modified_date.strftime("%Y-%m-%d") if new_user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Register Failed!"}), 400
    else:
        return jsonify({"message": "Register error!"}), 400


# ADD USER
def add_user_service():
    data = request.json
    if data and all(key in data for key in ('userName', 'fullName', 'image', 'password', 'dateBirth', 'email',
                                            'phone', 'address')) \
            and data['userName'] and data['email'] \
            and data['userName'] != "" and data['password'] != "" and data['dateBirth'] != "" and data['email'] != "" \
            and data['fullName'] != "" and data['image'] != "" and data['phone'] != "" and data['address'] != "":
        userName = data['userName'].strip()
        email = data['email'].strip()

        password = data['password'].strip() if data['password'] else None
        date_list = data['dateBirth'].split('-') if data['dateBirth'] else None
        dateBirth = None
        if date_list:
            dateBirth = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        fullName = data['fullName'] if data['fullName'] else None
        image = data['image'] if data['image'] else None
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
                "dateBirth": new_user.dateBirth.strftime("%Y-%m-%d") if new_user.dateBirth else None,
                "email": new_user.email,
                "phone": new_user.phone if new_user.phone else None,
                "address": new_user.address if new_user.address else None,
                "state": new_user.state,
                "dateJoining": new_user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": new_user.modified_date.strftime("%Y-%m-%d") if new_user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Register Failed!"}), 400
    else:
        return jsonify({"message": "Register error!"}), 400


# Hàm kiểm tra định dạng file hợp lệ
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# UPDATE IMG AVT USER
def update_image_avt_user_by_id_service(id):
    try:
        user = User.query.get(id)
        data = request.files
        if user:
            if 'picAvt' not in data:
                return jsonify({"message": "No image provided!"}), 400

            file = data['picAvt']

            # Kiểm tra nếu file không có tên
            if file.filename == '':
                return jsonify({"message": "No selected file"}), 400

            # Kiểm tra loại file
            if file and allowed_file(file.filename):
                fileName = secure_filename(file.filename)  # Đảm bảo tên file an toàn
                file_path = os.path.join(UPLOAD_FOLDER_USERS, fileName)

                # Lưu file vào thư mục
                file.save(file_path)

                try:
                    # Lưu thông tin ảnh vào database
                    user.image = fileName
                    db.session.commit()

                    return jsonify({
                        "image": user.image if user.image else None
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update avatar user!"}), 400
        else:
            return jsonify({"message": "Not found user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET IMG USER
# Tải ảnh trực tiếp từ thư mục lưu trữ
def get_image_service(fileName):
    try:
        return send_from_directory(UPLOAD_FOLDER_USERS, fileName)
    except FileNotFoundError:
        abort(404, description="Image not found")


# UPDATE USER'S STATE BY ID
def update_state_user_by_id_service(id):
    try:
        user = User.query.get(id)
        data = request.json
        if user:
            if data and ('state' in data) and data['state'] and data['state'] != "":
                try:
                    state = data['state']
                    if state.lower() == 'true':
                        user.state = True
                    elif state.lower() == 'false':
                        user.state = False
                    db.session.commit()

                    return jsonify({
                        "message": "Update user's state successfully!"
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Update user's state failed!"}), 400
            else:
                return {"message": "No state provided!"}, 400
        else:
            return {"message": "User not found!"}, 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET USER BY ID
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
                "dateBirth": user.dateBirth.strftime("%Y-%m-%d") if user.dateBirth else None,
                "email": user.email,
                "phone": user.phone if user.phone else None,
                "address": user.address if user.address else None,
                "state": user.state,
                "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
            }), 200
        else:
            return jsonify({"message": "Not found user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET USER BY NAME
def get_user_by_name_service(userName):
    try:
        user = User.query.filter_by(userName=userName).first()
        if user:
            list_user_bmi = get_list_user_bmi_by_userID(user.userID)

            return jsonify({
                "userID": user.userID,
                "userName": user.userName,
                "fullName": user.fullName if user.fullName else None,
                "image": user.image if user.image else None,
                "dateBirth": user.dateBirth.strftime("%Y-%m-%d") if user.dateBirth else None,
                "email": user.email,
                "phone": user.phone if user.phone else None,
                "address": user.address if user.address else None,
                "state": user.state,
                "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
            }), 200
        else:
            return jsonify({"message": "Not found user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET USER BY EMAIL GG
def get_user_by_email_gg_service(userName, email):
    try:
        user = User.query.filter_by(userName=userName, email=email).first()
        if user:
            # Tạo Access Token và Refresh Token
            # access_token = create_access_token(identity=user.userName, additional_claims={'role': 'user'})
            # refresh_token = create_refresh_token(identity=user.userName, additional_claims={'role': 'user'})

            list_user_bmi = get_list_user_bmi_by_userID(user.userID)

            return jsonify({
                "userID": user.userID,
                "userName": user.userName,
                "fullName": user.fullName if user.fullName else None,
                "image": user.image if user.image else None,
                "dateBirth": user.dateBirth.strftime("%Y-%m-%d") if user.dateBirth else None,
                "email": user.email,
                "phone": user.phone if user.phone else None,
                "address": user.address if user.address else None,
                "state": user.state,
                "dateJoining": user.dateJoining.strftime("%Y-%m-%d"),
                "modified_date": user.modified_date.strftime("%Y-%m-%d") if user.modified_date else None,
                "list_user_bmi": list_user_bmi if list_user_bmi else []
                # "access_token": access_token,
                # "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"message": "Not found user!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET ALL USERS
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
                    "dateBirth": user.dateBirth.strftime("%Y-%m-%d") if user.dateBirth else None,
                    "email": user.email,
                    "phone": user.phone if user.phone else None,
                    "address": user.address if user.address else None,
                    "state": user.state,
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


# UPDATE USER BY ID
def update_user_by_id_service(id):
    try:
        user = User.query.get(id)
        data = request.json
        if user:
            if data and all(key in data for key in ('userName', 'fullName', 'dateBirth', 'email', 'phone', 'address')) \
                and data['userName'] and data['email'] \
                    and data['userName'] != "" and data['dateBirth'] != "" and data['email'] != "":
                try:
                    user.userName = data['userName'].strip()
                    user.fullName = data['fullName'] if data['fullName'] else None
                    date_list = data['dateBirth'].split('-') if data['dateBirth'] else None
                    if date_list:
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
                        "image": user.image if user.image else None,
                        "dateBirth": user.dateBirth.strftime("%Y-%m-%d") if user.dateBirth else None,
                        "email": user.email,
                        "phone": user.phone,
                        "address": user.address,
                        "state": user.state,
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


# DELETE USER BMI
# Sử dụng sự kiện before_delete để xóa tất cả các đối tượng UserBMI liên quan trước khi xóa đối tượng User
@event.listens_for(User, 'before_delete')
def delete_related_bmis(mapper, connection, target):
    try:
        UserBMI.query.filter_by(userID=target.userID).delete()
        return True
    except Exception as e:
        db.session.rollback()
        return False, str(e)


# DELETE USER BY ID
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
