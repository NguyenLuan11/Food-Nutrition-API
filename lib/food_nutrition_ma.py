from flask_marshmallow import Marshmallow

ma = Marshmallow()


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('adminID', 'adminName', 'fullName', 'image', 'password', 'email', 'created_date', 'modified_date')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('userID', 'userName', 'fullName', 'image', 'password', 'dateBirth', 'email', 'phone', 'address',
                  'state', 'dateJoining', 'modified_date')


class UserBMISchema(ma.Schema):
    class Meta:
        fields = ('bmiID', 'userID', 'result', 'check_date')


class FoodsSchema(ma.Schema):
    class Meta:
        fields = ('foodID', 'foodName', 'image', 'nutritionValue', 'preservation', 'note',
                  'created_date', 'modified_date')


class NatureNutrientSchema(ma.Schema):
    class Meta:
        fields = ('natureID', 'natureName')


class NutrientsSchema(ma.Schema):
    class Meta:
        fields = ('nutrientID', 'nutrientName', 'natureID', 'description', 'needed', 'function', 'deficiencySigns',
                  'excessSigns', 'subjectInterest', 'shortagePrevention', 'created_date', 'modified_date')


class FoodNutrientSchema(ma.Schema):
    class Meta:
        fields = ('foodID', 'nutrientID')


class CategoryArticleSchema(ma.Schema):
    class Meta:
        fields = ('categoryID', 'categoryName', 'created_date', 'modified_date')


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('articleID', 'title', 'thumbnail', 'author', 'shortDescription', 'content', 'categoryID',
                  'created_date', 'modified_date')

