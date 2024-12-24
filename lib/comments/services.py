from ..model import db, User, Foods, Nutrients, Article, CommentFood, CommentNutrient, CommentArticle
from flask import request, jsonify


# ADD COMMENTS
def add_comment_food_service():
    data = request.json

    if data and all(key in data for key in ('userID', 'foodID', 'content')) and \
            data['userID'] and data['foodID'] and data['content'] and \
            data['userID'] != "" and data['foodID'] != "" and data['content'] != "":

        user_id = data['userID']
        food_id = data['foodID']
        content = data['content']

        try:
            user = User.query.get(user_id)
            food = Foods.query.get(food_id)

            if not user:
                return jsonify({"message": "User not found"}), 404
            if not food:
                return jsonify({"message": "Food not found"}), 404

            new_comment = CommentFood(foodID=food_id, userID=user_id, content=content)
            db.session.add(new_comment)
            db.session.commit()

            return jsonify({
                "commentID": new_comment.commentID,
                "userID": new_comment.userID,
                "foodID": new_comment.foodID,
                "content": new_comment.content
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Add comment failed", "error": str(e)}), 400
    else:
        return jsonify({"message": "Invalid input data"}), 400


def add_comment_nutrient_service():
    data = request.json

    if data and all(key in data for key in ('userID', 'nutrientID', 'content')) and \
            data['userID'] and data['nutrientID'] and data['content'] and \
            data['userID'] != "" and data['nutrientID'] != "" and data['content'] != "":

        user_id = data['userID']
        nutrient_id = data['nutrientID']
        content = data['content']

        try:
            user = User.query.get(user_id)
            nutrient = Nutrients.query.get(nutrient_id)

            if not user:
                return jsonify({"message": "User not found"}), 404
            if not nutrient:
                return jsonify({"message": "Nutrient not found"}), 404

            new_comment = CommentNutrient(nutrientID=nutrient_id, userID=user_id, content=content)
            db.session.add(new_comment)
            db.session.commit()

            return jsonify({
                "commentID": new_comment.commentID,
                "userID": new_comment.userID,
                "nutrientID": new_comment.nutrientID,
                "content": new_comment.content
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Add comment failed", "error": str(e)}), 400
    else:
        return jsonify({"message": "Invalid input data"}), 400


def add_comment_article_service():
    data = request.json

    if data and all(key in data for key in ('userID', 'articleID', 'content')) and \
            data['userID'] and data['articleID'] and data['content'] and \
            data['userID'] != "" and data['articleID'] != "" and data['content'] != "":

        user_id = data['userID']
        article_id = data['articleID']
        content = data['content']

        try:
            user = User.query.get(user_id)
            article = Article.query.get(article_id)

            if not user:
                return jsonify({"message": "User not found"}), 404
            if not article:
                return jsonify({"message": "Article not found"}), 404

            new_comment = CommentArticle(articleID=article_id, userID=user_id, content=content)
            db.session.add(new_comment)
            db.session.commit()

            return jsonify({
                "commentID": new_comment.commentID,
                "userID": new_comment.userID,
                "articleID": new_comment.articleID,
                "content": new_comment.content
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Add comment failed", "error": str(e)}), 400
    else:
        return jsonify({"message": "Invalid input data"}), 400


# GET ALL COMMENTS BY ID
def get_all_comments_by_foodID_service(foodID):
    if not foodID:
        return jsonify({"message": "Invalid foodID"}), 400

    try:
        comments = CommentFood.query.filter_by(foodID=foodID).all()
        if not comments:
            return jsonify({"message": "No comments found for this food"}), 404

        comment_list = []
        for comment in comments:
            user = User.query.get(comment.userID)
            if user:
                comment_list.append({
                    "commentID": comment.commentID,
                    "userName": user.userName,
                    "userImage": user.image or None,
                    "content": comment.content,
                    "created_date": comment.created_date.strftime("%Y-%m-%d")
                })

        return jsonify(comment_list), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving comments", "error": str(e)}), 400


def get_all_comments_by_nutrientID_service(nutrientID):
    if not nutrientID:
        return jsonify({"message": "Invalid nutrientID"}), 400

    try:
        comments = CommentNutrient.query.filter_by(nutrientID=nutrientID).all()
        if not comments:
            return jsonify({"message": "No comments found for this nutrient"}), 404

        comment_list = []
        for comment in comments:
            user = User.query.get(comment.userID)
            if user:
                comment_list.append({
                    "commentID": comment.commentID,
                    "userName": user.userName,
                    "userImage": user.image or None,
                    "content": comment.content,
                    "created_date": comment.created_date.strftime("%Y-%m-%d")
                })

        return jsonify(comment_list), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving comments", "error": str(e)}), 400


def get_all_comments_by_articleID_service(articleID):
    if not articleID:
        return jsonify({"message": "Invalid articleID"}), 400

    try:
        comments = CommentArticle.query.filter_by(articleID=articleID).all()
        if not comments:
            return jsonify({"message": "No comments found for this article"}), 404

        comment_list = []
        for comment in comments:
            user = User.query.get(comment.userID)
            if user:
                comment_list.append({
                    "commentID": comment.commentID,
                    "userName": user.userName,
                    "userImage": user.image or None,
                    "content": comment.content,
                    "created_date": comment.created_date.strftime("%Y-%m-%d")
                })

        return jsonify(comment_list), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving comments", "error": str(e)}), 400
