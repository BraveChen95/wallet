from flask import Blueprint, render_template, request, session, jsonify, current_app
from app import admin_manager
from app.models import Admin, Const
from app.admin.login_resource import LoginResource
from app.admin.admin_resource import AdminListResource, AdminResource
from app.admin.users_resource import UsersResource, UsersListResource
from app.admin.merchant_resource import MerchantsResource, MerchantsListResource
from app.admin.article_resource import ArticleListResource, ArticleResource
from flask_restful import Api, Resource

admin = Blueprint('sudo', __name__)
api = Api(admin)


api.add_resource(LoginResource, '/')
api.add_resource(AdminListResource, '/admins/')
api.add_resource(AdminResource, '/admins/<int:aid>')
api.add_resource(MerchantsListResource, '/merchants/')
api.add_resource(MerchantsResource, '/Merchants/<int:mid>')
api.add_resource(UsersListResource, '/users/')
api.add_resource(UsersResource, '/users/<int:uid>')
api.add_resource(ArticleListResource, '/article/')
api.add_resource(ArticleResource, '/article/<int:aid>')


# @admin.route('/', methods=["GET"])
# def index():
#     return  render_template('admin/index.html')
@admin_manager.user_loader
def user_loader(uid):
    if uid is None:
        return None

    try:
        return Admin.query.get(uid)

    except TypeError:
        return None
    except ValueError:
        return None


@admin_manager.failure_handler
def failure_handler():
    return {Const.MESSAGE_KEY: '您尚未登录或权限不足'}, Const.STATUS_DENIED


@admin_manager.hash_generator
def hash_generator(user):
    from app.utils.utils import generate_user_hash

    return generate_user_hash(user.get_id(), user.password, admin_manager.expires, admin_manager.salt)
