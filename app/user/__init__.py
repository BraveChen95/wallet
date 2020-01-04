from flask_restful import Api
from app.user.views import ArticleResource
from flask import Blueprint


user = Blueprint('user', __name__)

api = Api(user)


api.add_resource(ArticleResource, '/article/<int:aid>')