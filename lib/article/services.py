from ..model import db, Article, CategoryArticle
from flask import request, jsonify
from ..food_nutrition_ma import ArticleSchema
from sqlalchemy.sql import func

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


def add_article_service():
    data = request.json
    if data and all(key in data for key in ('title', 'thumbnail', 'author', 'shortDescription', 'content',
        'categoryID')) and data['title'] and data['content'] and data['title'] != "" and data['content'] != "":
        title = data['title']
        thumbnail = data['thumbnail'] if data['thumbnail'] else None
        author = data['author'] if data['author'] else None
        shortDescription = data['shortDescription'] if data['shortDescription'] else None
        content = data['content']
        categoryID = data['categoryID'] if data['categoryID'] else None
        try:
            new_article = Article(title=title, thumbnail=thumbnail, author=author, shortDescription=shortDescription,
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


def update_article_by_id_service(id):
    try:
        article = Article.query.get(id)
        data = request.json
        if article:
            if data and all(key in data for key in ('title', 'thumbnail', 'author', 'shortDescription', 'content',
                'categoryID')) and data['title'] and data['content'] and data['title'] != "" and data['content'] != "":
                try:
                    article.title = data['title']
                    article.thumbnail = data['thumbnail'] if data['thumbnail'] else None
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
