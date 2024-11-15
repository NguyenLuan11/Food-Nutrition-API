from flask import Blueprint, jsonify
from .services import add_article_service, get_all_articles_service, get_article_by_id_service, \
    update_article_by_id_service, delete_article_by_id_service, get_article_by_category_service, \
    upload_thumbnail_article_by_id_service, get_image_service
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt

article = Blueprint("article", __name__, url_prefix="/api/article-management")


@article.route("/article", methods=["POST"])
@jwt_required()
@swag_from("docs/add_article.yaml")
def add_article():
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return add_article_service()


# UPLOAD THUMBNAIL ARTICLE BY ID
@article.route("/article/upload-thumbnail/<int:id>", methods=["PUT"])
@jwt_required()
def upload_thumbnail_article_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return upload_thumbnail_article_by_id_service(id)


# GET IMG ARTICLE
@article.route('/article/thumbnail/<fileName>', methods=["GET"])
def get_image(fileName):
    return get_image_service(fileName)


@article.route("/article/<int:id>", methods=["GET"])
@swag_from("docs/get_article_by_id.yaml")
def get_article_by_id(id):
    return get_article_by_id_service(id)


@article.route("/articles", methods=["GET"])
@swag_from("docs/get_all_article.yaml")
def get_all_article():
    return get_all_articles_service()


@article.route("/article/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from("docs/update_article_by_id.yaml")
def update_article_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return update_article_by_id_service(id)


@article.route("/article/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/delete_article_by_id.yaml")
def delete_article_by_id(id):
    current_admin_role = get_jwt().get('role')
    if current_admin_role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    return delete_article_by_id_service(id)


@article.route("/article/<string:categoryName>", methods=["GET"])
@swag_from("docs/get_article_by_category.yaml")
def get_article_by_category(categoryName):
    return get_article_by_category_service(categoryName)

