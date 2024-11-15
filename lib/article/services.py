from ..model import db, Article, CategoryArticle
from flask import request, jsonify, send_from_directory, abort
from ..food_nutrition_ma import ArticleSchema
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import os
from ..config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_ARTICLES

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

UPLOAD_FOLDER_ARTICLES = os.path.join(os.getcwd(), UPLOAD_FOLDER_ARTICLES)


# Hàm kiểm tra định dạng file hợp lệ
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# UPLOAD THUMBNAIL ARTICLE BY ID
def upload_thumbnail_article_by_id_service(id):
    try:
        article = Article.query.get(id)
        uploadImg = request.files
        if article:
            if 'picArticle' in uploadImg:
                file = uploadImg['picArticle']

                # Kiểm tra nếu file không có tên
                if file.filename == '':
                    return jsonify({"message": "No selected file"}), 400

                # Kiểm tra loại file
                if file and allowed_file(file.filename):
                    fileName = secure_filename(file.filename)  # Đảm bảo tên file an toàn
                    file_path = os.path.join(UPLOAD_FOLDER_ARTICLES, fileName)

                    # Lưu file vào thư mục
                    file.save(file_path)

                    try:
                        article.thumbnail = fileName
                        db.session.commit()

                        return jsonify({
                            "thumbnail": article.thumbnail if article.thumbnail else None
                        }), 200
                    except IndentationError:
                        db.session.rollback()
                        return jsonify({"message": "Can not upload food's image!"}), 400
            else:
                return jsonify({"message": "No image provided!"}), 400
        else:
            return jsonify({"message": "Not found food!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET THUMBNAIL ARTICLE
# Tải ảnh trực tiếp từ thư mục lưu trữ
def get_image_service(fileName):
    try:
        return send_from_directory(UPLOAD_FOLDER_ARTICLES, fileName)
    except FileNotFoundError:
        abort(404, description="Image not found")


# ADD ARTICLE
def add_article_service():
    data = request.json
    if data and all(key in data for key in ('title', 'author', 'shortDescription', 'content',
        'categoryID')) and data['title'] and data['content'] and data['title'] != "" and data['content'] != "":
        title = data['title']
        author = data['author'] if data['author'] else None
        shortDescription = data['shortDescription'] if data['shortDescription'] else None
        content = data['content']
        categoryID = data['categoryID'] if data['categoryID'] else None
        try:
            new_article = Article(title=title, author=author, shortDescription=shortDescription,
                                  content=content, categoryID=categoryID)

            db.session.add(new_article)
            db.session.commit()

            # category = CategoryArticle.query.get(categoryID)

            return jsonify({
                "articleID": new_article.articleID,
                "title": new_article.title,
                "thumbnail": new_article.thumbnail if new_article.thumbnail else None,
                "author": new_article.author if new_article.author else None,
                "shortDescription": new_article.shortDescription if new_article.shortDescription else None,
                "content": new_article.content,
                # "category": category.categoryName if category else None,
                "categoryID": new_article.categoryID if new_article.categoryID else None,
                "created_date": new_article.created_date.strftime("%Y-%m-%d"),
                "modified_date": new_article.modified_date.strftime("%Y-%m-%d") if new_article.modified_date else None
            }), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add article!"}), 400
    else:
        return jsonify({"message": "Request error!"}), 400


# GET ARTICLE BY ID
def get_article_by_id_service(id):
    try:
        article = Article.query.get(id)
        if article:
            # category = CategoryArticle.query.get(article.categoryID)

            return jsonify({
                "articleID": article.articleID,
                "title": article.title,
                "thumbnail": article.thumbnail if article.thumbnail else None,
                "author": article.author if article.author else None,
                "shortDescription": article.shortDescription if article.shortDescription else None,
                "content": article.content,
                "categoryID": article.categoryID if article.categoryID else None,
                "created_date": article.created_date.strftime("%Y-%m-%d"),
                "modified_date": article.modified_date.strftime("%Y-%m-%d") if article.modified_date else None
            }), 200
        else:
            return jsonify({"message": "Not found article!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET ALL ARTICLE
def get_all_articles_service():
    try:
        articles = Article.query.all()
        if articles:
            articles_list = []
            for article in articles:
                # category = CategoryArticle.query.get(article.categoryID)

                articles_list.append({
                    "articleID": article.articleID,
                    "title": article.title,
                    "thumbnail": article.thumbnail if article.thumbnail else None,
                    "author": article.author if article.author else None,
                    "shortDescription": article.shortDescription if article.shortDescription else None,
                    "content": article.content,
                    "categoryID": article.categoryID if article.categoryID else None,
                    "created_date": article.created_date.strftime("%Y-%m-%d"),
                    "modified_date": article.modified_date.strftime("%Y-%m-%d") if article.modified_date else None
                })

            return jsonify(articles_list), 200
        else:
            return jsonify({"message": "Not found list of article!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# UPDATE ARTICLE BY ID
def update_article_by_id_service(id):
    try:
        article = Article.query.get(id)
        data = request.json
        if article:
            if data and all(key in data for key in ('title', 'author', 'shortDescription', 'content',
                'categoryID')) and data['title'] and data['content'] and data['title'] != "" and data['content'] != "":
                try:
                    article.title = data['title']
                    article.author = data['author'] if data['author'] else None
                    article.shortDescription = data['shortDescription'] if data['shortDescription'] else None
                    article.content = data['content']
                    article.categoryID = data['categoryID'] if data['categoryID'] else None

                    db.session.commit()

                    # category = CategoryArticle.query.get(article.categoryID)

                    return jsonify({
                        "articleID": article.articleID,
                        "title": article.title,
                        "thumbnail": article.thumbnail if article.thumbnail else None,
                        "author": article.author if article.author else None,
                        "shortDescription": article.shortDescription if article.shortDescription else None,
                        "content": article.content,
                        "categoryID": article.categoryID if article.categoryID else None,
                        "created_date": article.created_date.strftime("%Y-%m-%d"),
                        "modified_date": article.modified_date.strftime("%Y-%m-%d")
                    }), 200
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message": "Can not update article!"}), 400
        else:
            return jsonify({"message": "Not found article!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# DELETE ARTICLE BY ID
def delete_article_by_id_service(id):
    try:
        article = Article.query.get(id)
        if article:
            try:
                db.session.delete(article)
                db.session.commit()

                return jsonify({"message": "Article deleted!"}), 200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete article!"}), 400
        else:
            return jsonify({"message": "Not found article!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400


# GET ARTICLE BY CATEGORY
def get_article_by_category_service(categoryName):
    try:
        articles = Article.query.join(CategoryArticle, Article.categoryID == CategoryArticle.categoryID)\
            .filter(func.lower(CategoryArticle.categoryName) == categoryName.lower()).all()
        if articles:
            articles_list = []
            for article in articles:
                # category = CategoryArticle.query.get(article.categoryID)

                articles_list.append({
                    "articleID": article.articleID,
                    "title": article.title,
                    "thumbnail": article.thumbnail if article.thumbnail else None,
                    "author": article.author if article.author else None,
                    "shortDescription": article.shortDescription if article.shortDescription else None,
                    "content": article.content,
                    "categoryID": article.categoryID if article.categoryID else None,
                    "created_date": article.created_date.strftime("%Y-%m-%d"),
                    "modified_date": article.modified_date.strftime("%Y-%m-%d") if article.modified_date else None
                })

            return jsonify(articles_list), 200
        else:
            return jsonify({"message": "Not found list of article!"}), 404
    except IndentationError:
        db.session.rollback()
        return jsonify({"message": "Request error!"}), 400
