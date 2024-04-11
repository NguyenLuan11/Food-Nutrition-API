import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from .model import db
from .food_nutrition_ma import ma
from .swagger import template, swagger_config
from .admin.controller import admin
from .article.controller import article
from .category_article.controller import categoryArticle
from .food_nutrient.controller import foodNutrient
from .foods.controller import foods
from .nature_nutrient.controller import natureNutrient
from .nutrients.controller import nutrients
from .user.controller import user


def create_app(config_file="config.py"):
    app = Flask(__name__)

    # Add config
    app.config.from_pyfile(config_file)

    # Init Marshmallow
    ma.init_app(app)

    # Init DB
    db.init_app(app)

    # Create DB
    if not os.path.exists("/food_nutrition.db"):
        with app.app_context():
            db.create_all()
            print("Created DB!")

    # JWT
    JWTManager(app)

    # Register BluePrint
    app.register_blueprint(admin)
    app.register_blueprint(article)
    app.register_blueprint(categoryArticle)
    app.register_blueprint(foodNutrient)
    app.register_blueprint(foods)
    app.register_blueprint(natureNutrient)
    app.register_blueprint(nutrients)
    app.register_blueprint(user)

    print(app.config["SECRET_KEY"])

    # Swagger
    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), 500

    return app
