from flask import Blueprint
from .services import add_article_service, get_all_articles_service, get_article_by_id_service, \
    update_article_by_id_service, delete_article_by_id_service, get_article_by_category_service
from flasgger import swag_from

article = Blueprint("article", __name__, url_prefix="/api/article-management")


@article.route("/article", methods=["POST"])
@swag_from("docs/add_article.yaml")
def add_article():
    return add_article_service()


@article.route("/article/<int:id>", methods=["GET"])
@swag_from("docs/get_article_by_id.yaml")
def get_article_by_id(id):
    return get_article_by_id_service(id)


@article.route("/articles", methods=["GET"])
@swag_from("docs/get_all_article.yaml")
def get_all_article():
    return get_all_articles_service()


@article.route("/article/<int:id>", methods=["PUT"])
@swag_from("docs/update_article_by_id.yaml")
def update_article_by_id(id):
    return update_article_by_id_service(id)


@article.route("/article/<int:id>", methods=["DELETE"])
@swag_from("docs/delete_article_by_id.yaml")
def delete_article_by_id(id):
    return delete_article_by_id_service(id)


@article.route("/article/<string:categoryName>", methods=["GET"])
@swag_from("docs/get_article_by_category.yaml")
def get_article_by_category(categoryName):
    return get_article_by_category_service(categoryName)

