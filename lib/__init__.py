import os
from zeroconf import ServiceInfo, Zeroconf
import socket
from flask import Flask, jsonify
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from flask_cors import CORS
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
from .user_BMI.controller import userBMI
from .comments.controller import comment


# Automation get local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external address to determine the local IP (without actually sending the packet)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    finally:
        s.close()
    return ip_address


# Register mDNS service when server Flask start
def register_mdns_service():
    zeroconf = Zeroconf()
    service_type = "_http._tcp.local."
    service_name = "Food_Nutrition_API._http._tcp.local."
    ip_address = socket.inet_aton(get_local_ip())  # Automation get local IP address
    port = 5007  # Port Flask server

    # Create information for service mDNS
    service_info = ServiceInfo(
        service_type,
        service_name,
        addresses=[ip_address],
        port=port,
        properties={},
        server="fn-api.local."
    )

    # Register service
    zeroconf.register_service(service_info)
    print("Service registered as fn-api.local with IP:", get_local_ip())


def create_app(config_file="config.py"):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

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

    # Mail
    mail = Mail(app)

    # Register BluePrint
    app.register_blueprint(admin)
    app.register_blueprint(article)
    app.register_blueprint(categoryArticle)
    app.register_blueprint(foodNutrient)
    app.register_blueprint(foods)
    app.register_blueprint(natureNutrient)
    app.register_blueprint(nutrients)
    app.register_blueprint(user)
    app.register_blueprint(userBMI)
    app.register_blueprint(comment)

    # print(app.config["SECRET_KEY"])

    # Swagger
    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), 500

    return app
