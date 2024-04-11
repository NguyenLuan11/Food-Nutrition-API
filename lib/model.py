from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = "admin"

    adminID = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(50), nullable=False)
    fullName = db.Column(db.String(100))
    image = db.Column(db.LargeBinary)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, adminName, fullName, image, password, email):
        self.adminName = adminName
        self.fullName = fullName
        self.image = image
        self.password = password
        self.email = email


class User(db.Model):
    __tablename__ = 'user'

    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), nullable=False)
    fullName = db.Column(db.String(100))
    image = db.Column(db.LargeBinary)
    password = db.Column(db.String(100), nullable=False)
    dateBirth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12))
    address = db.Column(db.String(255))
    state = db.Column(db.Boolean, default=True)
    dateJoining = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    # Thêm mối quan hệ với UserBMI và sử dụng cascade để xóa UserBMI khi User bị xóa
    bmis = db.relationship('UserBMI', backref='user', cascade="all, delete-orphan")

    def __init__(self, userName, fullName, image, password, dateBirth, email, phone, address):
        self.userName = userName
        self.fullName = fullName
        self.image = image
        self.password = password
        self.email = email
        self.dateBirth = dateBirth
        self.phone = phone
        self.address = address


class UserBMI(db.Model):
    __tablename__ = 'user_BMI'

    bmiId = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"))
    result = db.Column(db.Float)
    check_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, userID, result):
        self.userID = userID
        self.result = result


class Foods(db.Model):
    __tablename__ = 'foods'

    foodID = db.Column(db.Integer, primary_key=True)
    foodName = db.Column(db.String(50), nullable=False)
    image = db.Column(db.LargeBinary)
    nutritionValue = db.Column(db.Text, nullable=False)
    preservation = db.Column(db.Text)
    note = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    food_nutrient = db.relationship('FoodNutrient', backref='foods', cascade="all, delete-orphan")

    def __init__(self, foodName, image, nutritionValue, preservation, note):
        self.foodName = foodName
        self.image = image
        self.nutritionValue = nutritionValue
        self.preservation = preservation
        self.note = note


class NatureNutrient(db.Model):
    __tablename__ = 'nature_nutrient'

    natureID = db.Column(db.Integer, primary_key=True)
    natureName = db.Column(db.String(100), nullable=False)

    nutrients = db.relationship('Nutrients', backref='nature_nutrient', cascade="all, delete-orphan")

    def __init__(self, natureName):
        self.natureName = natureName


class Nutrients(db.Model):
    __tablename__ = 'nutrients'

    nutrientID = db.Column(db.Integer, primary_key=True)
    nutrientName = db.Column(db.String(50), nullable=False)
    natureID = db.Column(db.Integer, db.ForeignKey("nature_nutrient.natureID"))
    description = db.Column(db.Text)
    needed = db.Column(db.Float, nullable=False)
    function = db.Column(db.Text, nullable=False)
    deficiencySigns = db.Column(db.Text)
    excessSigns = db.Column(db.Text)
    subjectInterest = db.Column(db.Text)
    shortagePrevention = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    food_nutrient = db.relationship('FoodNutrient', backref='nutrients', cascade="all, delete-orphan")

    def __init__(self, nutrientName, natureID, description, needed, function, deficiencySigns, excessSigns,
                 subjectInterest, shortagePrevention):
        self.nutrientName = nutrientName
        self.natureID = natureID
        self.description = description
        self.needed = needed
        self.function = function
        self.deficiencySigns = deficiencySigns
        self.excessSigns = excessSigns
        self.subjectInterest = subjectInterest
        self.shortagePrevention = shortagePrevention


class FoodNutrient(db.Model):
    __tablename__ = 'food_nutrient'

    foodID = db.Column(db.Integer, db.ForeignKey("foods.foodID"), primary_key=True)
    nutrientID = db.Column(db.Integer, db.ForeignKey("nutrients.nutrientID"), primary_key=True)

    def __init__(self, foodID, nutrientID):
        self.foodID = foodID
        self.nutrientID = nutrientID


class CategoryArticle(db.Model):
    __tablename__ = 'category_article'

    categoryID = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    article = db.relationship('Article', backref='category_article', cascade="all, delete-orphan")

    def __init__(self, categoryName):
        self.categoryName = categoryName


class Article(db.Model):
    __tablename__ = 'article'

    articleID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.LargeBinary)
    author = db.Column(db.String(100))
    shortDescription = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey("category_article.categoryID"))
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, title, thumbnail, author, shortDescription, content, categoryID):
        self.title = title
        self.thumbnail = thumbnail
        self.author = author
        self.shortDescription = shortDescription
        self.content = content
        self.categoryID = categoryID
