from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CommentFood(db.Model):
    __tablename__ = 'comment_food'

    commentID = db.Column(db.Integer, primary_key=True)
    foodID = db.Column(db.Integer, db.ForeignKey("foods.foodID"), nullable=False)  # Liên kết với Foods
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable=False)  # Liên kết với User
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, foodID, userID, content):
        self.foodID = foodID
        self.userID = userID
        self.content = content


class CommentNutrient(db.Model):
    __tablename__ = 'comment_nutrient'

    commentID = db.Column(db.Integer, primary_key=True)
    nutrientID = db.Column(db.Integer, db.ForeignKey("nutrients.nutrientID"), nullable=False)  # Liên kết với Nutrients
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable=False)  # Liên kết với User
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, nutrientID, userID, content):
        self.nutrientID = nutrientID
        self.userID = userID
        self.content = content


class CommentArticle(db.Model):
    __tablename__ = 'comment_article'

    commentID = db.Column(db.Integer, primary_key=True)
    articleID = db.Column(db.Integer, db.ForeignKey("article.articleID"), nullable=False)  # Liên kết với Articles
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable=False)  # Liên kết với User
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, articleID, userID, content):
        self.articleID = articleID
        self.userID = userID
        self.content = content


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at


class Admin(db.Model):
    __tablename__ = "admin"

    adminID = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(50), nullable=False)
    fullName = db.Column(db.String(100))
    image = db.Column(db.String(100))
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
    image = db.Column(db.String(100))
    password = db.Column(db.String(100))
    dateBirth = db.Column(db.Date)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12))
    address = db.Column(db.String(255))
    state = db.Column(db.Boolean, default=True)
    dateJoining = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    # Thêm mối quan hệ với UserBMI và sử dụng cascade để xóa UserBMI khi User bị xóa
    bmis = db.relationship('UserBMI', backref='user', cascade="all, delete-orphan")

    comments_food = db.relationship('CommentFood', backref='user', cascade="all, delete-orphan")
    comments_nutrient = db.relationship('CommentNutrient', backref='user', cascade="all, delete-orphan")
    comments_article = db.relationship('CommentArticle', backref='user', cascade="all, delete-orphan")

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
    image = db.Column(db.String(100))
    nutritionValue = db.Column(db.Text, nullable=False)
    preservation = db.Column(db.Text)
    note = db.Column(db.Text)
    kcalOn100g = db.Column(db.Float, nullable=False)
    proteinOn100g = db.Column(db.Float, nullable=False)
    carbsOn100g = db.Column(db.Float, nullable=False)
    fatOn100g = db.Column(db.Float, nullable=False)
    fiberOn100g = db.Column(db.Float, nullable=False)
    omega3On100g = db.Column(db.Float, nullable=False)
    sugarOn100g = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    food_nutrient = db.relationship('FoodNutrient', backref='foods', cascade="all, delete-orphan")
    comments = db.relationship('CommentFood', backref='foods', cascade="all, delete-orphan")

    def __init__(self, foodName, image, kcalOn100g, nutritionValue, preservation, note,
                 proteinOn100g, carbsOn100g, fatOn100g, fiberOn100g, omega3On100g, sugarOn100g):
        self.foodName = foodName
        self.image = image
        self.kcalOn100g = kcalOn100g
        self.nutritionValue = nutritionValue
        self.preservation = preservation
        self.note = note
        self.proteinOn100g = proteinOn100g
        self.carbsOn100g = carbsOn100g
        self.fatOn100g = fatOn100g
        self.fiberOn100g = fiberOn100g
        self.omega3On100g = omega3On100g
        self.sugarOn100g = sugarOn100g


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
    needed = db.Column(db.String(50), nullable=False)
    function = db.Column(db.Text, nullable=False)
    deficiencySigns = db.Column(db.Text)
    excessSigns = db.Column(db.Text)
    subjectInterest = db.Column(db.Text)
    shortagePrevention = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    food_nutrient = db.relationship('FoodNutrient', backref='nutrients', cascade="all, delete-orphan")
    comments = db.relationship('CommentNutrient', backref='nutrients', cascade="all, delete-orphan")

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
    thumbnail = db.Column(db.Text)
    author = db.Column(db.String(100))
    origin = db.Column(db.String(200))
    linkOrigin = db.Column(db.String(255))
    shortDescription = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey("category_article.categoryID"))
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now)

    comments = db.relationship('CommentArticle', backref='article', cascade="all, delete-orphan")

    def __init__(self, title, thumbnail, author, origin, linkOrigin, shortDescription, content, categoryID):
        self.title = title
        self.thumbnail = thumbnail
        self.author = author
        self.shortDescription = shortDescription
        self.content = content
        self.categoryID = categoryID
        self.origin = origin
        self.linkOrigin = linkOrigin
