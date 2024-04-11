from ..model import db, CategoryArticle, Article
from ..food_nutrition_ma import CategoryArticleSchema
from flask import request, jsonify
from sqlalchemy import event


categoryArticle_schema = CategoryArticleSchema()
categoriesArticle_schema = CategoryArticleSchema(many=True)


def add_categoryArticle_service():
    data = request.json
    if data and ('categoryName' in data) and data['categoryName'] and data['categoryName'] != "":
        categoryName = data['categoryName']
        try:
            new_categoryArticle = CategoryArticle(categoryName=categoryName)

            db.session.add(new_categoryArticle),
            db.session.commit()

            return jsonify({
                            "categoryId": new_categoryArticle.categoryID,
                            "categoryName": new_categoryArticle.categoryName,
                            "created_date": new_categoryArticle.created_date.strftime("%Y-%m-%d"),
                            "modified_date": new_categoryArticle.modified_date.strftime("%Y-%m-%d")
                            if new_categoryArticle.modified_date else None
                            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add category!"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


def get_categoryArticle_by_id_service(id):
    categoryArticle = CategoryArticle.query.get(id)
    if categoryArticle:
        return jsonify({"categoryId": categoryArticle.categoryID,
                        "categoryName": categoryArticle.categoryName,
                        "created_date": categoryArticle.created_date.strftime("%Y-%m-%d"),
                        "modified_date": categoryArticle.modified_date.strftime("%Y-%m-%d")
                        if categoryArticle.modified_date else None
                        }), 200
    else:
        return jsonify({"message": "Not found category!"}), 404


def get_all_categoryArticle_service():
    try:
        categoriesArticle = CategoryArticle.query.all()
        if categoriesArticle:
            categories_list = []
            for category in categoriesArticle:
                categories_list.append({
                    "categoryId": category.categoryID,
                    "categoryName": category.categoryName,
                    "created_date": category.created_date.strftime("%Y-%m-%d"),
                    "modified_date": category.modified_date.strftime("%Y-%m-%d") if category.modified_date else None
                })

            return jsonify(categories_list), 200
        else:
            return jsonify({"message": "Not found list of category!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


def update_categoryArticle_by_id_service(id):
    try:
        categoryArticle = CategoryArticle.query.get(id)
        data = request.json
        if categoryArticle:
            if data and ('categoryName' in data) and data['categoryName'] and data['categoryName'] != "":
                try:
                    categoryArticle.categoryName = data['categoryName']

                    db.session.commit()

                    return jsonify({
                                    "categoryId": categoryArticle.categoryID,
                                    "categoryName": categoryArticle.categoryName,
                                    "created_date": categoryArticle.created_date.strftime("%Y-%m-%d"),
                                    "modified_date": categoryArticle.modified_date.strftime("%Y-%m-%d")
                                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update category!"}), 400
        else:
            return jsonify({"message": "Not found category!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# Sử dụng sự kiện before_delete để xóa tất cả các đối tượng Article liên quan trước khi xóa đối tượng CategoryArticle
@event.listens_for(CategoryArticle, 'before_delete')
def delete_related_article(mapper, connection, target):
    try:
        Article.query.filter_by(categoryID=target.categoryID).delete()
        return True
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def delete_categoryArticle_by_id_service(id):
    try:
        categoryArticle = CategoryArticle.query.get(id)
        if categoryArticle:
            try:
                db.session.delete(categoryArticle)
                db.session.commit()
                return jsonify({"message": "Category deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete category!"}), 400
        else:
            return jsonify({"message": "Not found category!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
