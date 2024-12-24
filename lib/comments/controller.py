from flask import Blueprint, jsonify
from flasgger import swag_from
from .services import add_comment_article_service, add_comment_food_service, add_comment_nutrient_service, \
    get_all_comments_by_articleID_service, get_all_comments_by_foodID_service, get_all_comments_by_nutrientID_service

comment = Blueprint("comment", __name__, url_prefix="/api/comments-management")


# ADD NEW COMMENT
@comment.route('/add-comment-article', methods=['POST'])
def add_comment_article():
    return add_comment_article_service()


@comment.route('/add-comment-food', methods=['POST'])
def add_comment_food():
    return add_comment_food_service()


@comment.route('/add-comment-nutrient', methods=['POST'])
def add_comment_nutrient():
    return add_comment_nutrient_service()


# GET ALL COMMENTS BY ID
@comment.route('/comments/article/<int:articleID>', methods=['GET'])
def get_all_comments_by_articleID(articleID):
    return get_all_comments_by_articleID_service(articleID)


@comment.route('/comments/food/<int:foodID>', methods=['GET'])
def get_all_comments_by_foodID(foodID):
    return get_all_comments_by_foodID_service(foodID)


@comment.route('/comments/nutrient/<int:nutrientID>', methods=['GET'])
def get_all_comments_by_nutrientID(nutrientID):
    return get_all_comments_by_nutrientID_service(nutrientID)
