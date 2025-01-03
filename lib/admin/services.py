from ..model import db, Admin, Foods, Article, User, Nutrients, CategoryArticle, Exercise
from ..food_nutrition_ma import AdminSchema
from flask import request, jsonify, send_from_directory, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from ..config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_ADMIN

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

UPLOAD_FOLDER_ADMIN = os.path.join(os.getcwd(), UPLOAD_FOLDER_ADMIN)


def count_all_items_service():
    try:
        foods = Foods.query.all()
        users = User.query.all()
        articles = Article.query.all()
        nutrients = Nutrients.query.all()
        categories = CategoryArticle.query.all()
        exercises = Exercise.query.all()

        return jsonify({
            "foods": len(foods) if foods else 0,
            "users": len(users) if users else 0,
            "articles": len(articles) if articles else 0,
            "nutrients": len(nutrients) if nutrients else 0,
            "categories": len(categories) if categories else 0,
            "exercises": len(exercises) if exercises else 0,
        }), 200
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def check_correct_pass_by_id_service(id):
    try:
        admin = Admin.query.get(id)
        data = request.json
        if admin:
            if data and ('password' in data) and data['password'] != "":
                check_pass = data['password'].strip()
                pass_current = admin.password

                if check_pass == pass_current:
                    return jsonify({"message": "Is correct password!"}), 200
                else:
                    return jsonify({"message": "Is not correct password!"}), 400
        else:
            return jsonify({"message": f"Not found admin with ID is {id}!"}), 404

    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_pass_by_id_service(id):
    try:
        admin = Admin.query.get(id)
        data = request.json
        if admin:
            if data and ('password' in data) and data['password'] != "":
                change_pass = data['password'].strip()

                try:
                    admin.password = change_pass
                    db.session.commit()
                    return jsonify({"message": "Update admin's password successfully!"}), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can't update admin's password!"}), 400
        else:
            return jsonify({"message": f"Not found admin with ID is {id}!"}), 404

    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def login_admin_service():
    data = request.json
    if data and ('adminName' in data) and ('password' in data) and data['adminName'] and data['password'] \
            and data['adminName'] != "" and data['password'] != "":
        adminName = data['adminName'].strip()
        password = data['password'].strip()

        admin = Admin.query.filter_by(adminName=adminName, password=password).first()

        if admin:
            # Tạo Access Token và Refresh Token
            access_token = create_access_token(identity=admin.adminName, additional_claims={'role': 'admin'})
            refresh_token = create_refresh_token(identity=admin.adminName, additional_claims={'role': 'admin'})

            return jsonify({
                "adminID": admin.adminID,
                "adminName": admin.adminName,
                "fullName": admin.fullName if admin.fullName else None,
                "image": admin.image if admin.image else None,
                "email": admin.email,
                "created_date": admin.created_date.strftime("%Y-%m-%d"),
                "modified_date": admin.modified_date.strftime("%Y-%m-%d") if admin.modified_date else None,
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"message": "Incorrect username or password!"}), 404
    else:
        return jsonify({"message": "Login error!"}), 400


def refresh_token_service():
    current_admin = get_jwt_identity()
    new_access_token = create_access_token(identity=current_admin, additional_claims={'role': 'admin'})

    return jsonify(access_token=new_access_token), 200


def add_admin_service():
    data = request.json
    if data and all(key in data for key in ('adminName', 'fullName', 'image', 'password', 'email')) \
        and data['adminName'] and data['password'] and data['email'] \
            and data['adminName'] != "" and data['password'] != "" and data['email'] != "":
        adminName = data['adminName'].strip()
        fullName = data['fullName'] if data['fullName'] else None
        image = data['image'] if data['image'] else None
        password = data['password'].strip()
        email = data['email'].strip()
        try:
            new_admin = Admin(adminName=adminName, fullName=fullName, image=image, password=password, email=email)
            db.session.add(new_admin)
            db.session.commit()

            return jsonify({
                "adminID": new_admin.adminID,
                "adminName": new_admin.adminName,
                "fullName": new_admin.fullName if new_admin.fullName else None,
                "image": new_admin.image if new_admin.image else None,
                "email": new_admin.email,
                "created_date": new_admin.created_date.strftime("%Y-%m-%d"),
                "modified_date": new_admin.modified_date.strftime("%Y-%m-%d") if new_admin.modified_date else None
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add new admin!"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_admin_by_id_service(id):
    try:
        admin = Admin.query.get(id)
        if admin:
            return jsonify({
                "adminID": admin.adminID,
                "adminName": admin.adminName,
                "fullName": admin.fullName if admin.fullName else None,
                "image": admin.image if admin.image else None,
                "email": admin.email,
                "created_date": admin.created_date.strftime("%Y-%m-%d"),
                "modified_date": admin.modified_date.strftime("%Y-%m-%d") if admin.modified_date else None
            }), 200
        else:
            return jsonify({"message": f"Not found admin have id is {id}!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def get_all_admin_service():
    try:
        admins = Admin.query.all()
        if admins:
            admin_list = []
            for admin in admins:
                admin_list.append({
                    "adminID": admin.adminID,
                    "adminName": admin.adminName,
                    "fullName": admin.fullName if admin.fullName else None,
                    "image": admin.image if admin.image else None,
                    "email": admin.email,
                    "created_date": admin.created_date.strftime("%Y-%m-%d"),
                    "modified_date": admin.modified_date.strftime("%Y-%m-%d") if admin.modified_date else None
                })
            return jsonify(admin_list), 200
        else:
            return jsonify({"message": "Not found list of admin!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_admin_by_id_service(id):
    try:
        admin = Admin.query.get(id)
        data = request.json
        if admin:
            if data and all(key in data for key in ('adminName', 'fullName', 'email')) \
                and data['adminName'] and data['email'] \
                    and data['adminName'] != "" and data['email'] != "":
                try:
                    admin.adminName = data['adminName'].strip()
                    admin.fullName = data['fullName'].strip() if data['fullName'] else None
                    admin.email = data['email'].strip()

                    db.session.commit()

                    return jsonify({
                        "adminID": admin.adminID,
                        "adminName": admin.adminName,
                        "fullName": admin.fullName if admin.fullName else None,
                        "image": admin.image if admin.image else None,
                        "email": admin.email,
                        "created_date": admin.created_date.strftime("%Y-%m-%d"),
                        "modified_date": admin.modified_date.strftime("%Y-%m-%d")
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update admin!"}), 400
        else:
            return jsonify({"message": "Not found admin!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Hàm kiểm tra định dạng file hợp lệ
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_image_avt_admin_by_id_service(id):
    try:
        admin = Admin.query.get(id)
        data = request.files
        if admin:
            if 'picAvt' not in data:
                return jsonify({"message": "No image provided!"}), 400

            file = data['picAvt']

            # Kiểm tra nếu file không có tên
            if file.filename == '':
                return jsonify({"message": "No selected file"}), 400

            # Kiểm tra loại file
            if file and allowed_file(file.filename):
                fileName = secure_filename(file.filename)  # Đảm bảo tên file an toàn
                file_path = os.path.join(UPLOAD_FOLDER_ADMIN, fileName)

                # Lưu file vào thư mục
                file.save(file_path)

                try:
                    # Lưu thông tin ảnh vào database
                    admin.image = fileName
                    db.session.commit()

                    return jsonify({
                        "image": admin.image if admin.image else None
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update avatar admin!"}), 400
        else:
            return jsonify({"message": "Not found admin!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Tải ảnh trực tiếp từ thư mục lưu trữ
def get_image_service(fileName):
    try:
        return send_from_directory(UPLOAD_FOLDER_ADMIN, fileName)
    except FileNotFoundError:
        abort(404, description="Image not found")


def delete_admin_by_id_service(id):
    try:
        admin = Admin.query.get(id)
        if admin:
            try:
                db.session.delete(admin)
                db.session.commit()
                return jsonify({"message": "Admin deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete admin!"}), 400
        else:
            return jsonify({"message": "Not found admin!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
