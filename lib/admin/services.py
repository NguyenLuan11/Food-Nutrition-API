from ..model import db, Admin, Foods, Article, User, Nutrients, CategoryArticle
from ..food_nutrition_ma import AdminSchema
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


def count_all_items_service():
    try:
        foods = Foods.query.all()
        users = User.query.all()
        articles = Article.query.all()
        nutrients = Nutrients.query.all()
        categories = CategoryArticle.query.all()

        return jsonify({
            "foods": len(foods) if foods else 0,
            "users": len(users) if users else 0,
            "articles": len(articles) if articles else 0,
            "nutrients": len(nutrients) if nutrients else 0,
            "categories": len(categories) if categories else 0,
        }), 200
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


def update_image_avt_admin_by_id_service(id):
    try:
        admin = Admin.query.get(id)
        data = request.json
        if admin:
            if data and ('image' in data) and data['image'] and data['image'] != "":
                try:
                    admin.image = data['image']
                    db.session.commit()

                    return jsonify({
                        "image": admin.image if admin.image else None
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update avatar admin!"}), 400
            else:
                return jsonify({"message": "No image provided!"}), 400
        else:
            return jsonify({"message": "Not found admin!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


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
