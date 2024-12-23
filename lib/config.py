import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

SECRET_KEY = os.environ.get("KEY")

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATION = False

SWAGGER = {
    'title': 'Food Nutrition API',
    'uiversion': 3
}

JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=35)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

UPLOAD_FOLDER_ADMIN = "images/admin"
UPLOAD_FOLDER_USERS = "images/users"
UPLOAD_FOLDER_FOODS = "images/foods"
UPLOAD_FOLDER_NUTRIENTS = "images/nutrients"
UPLOAD_FOLDER_ARTICLES = "images/articles"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff'}