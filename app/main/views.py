#from . import main
from flask import request, flash, jsonify, session
from app import user_manager, db, csrf
from app.models import User,Merchants, Const, Admin
import time
import re
import requests
import json

from flask_restful import Resource,reqparse
from app.utils.utils import safe_session





#登录操作
class LoginResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='请输入用户名', location='json', store_missing=False)
        self.parser.add_argument('password', type=str, required=True, help='请输入密码', location='json', store_missing=False)
        #self.parser.add_argument('vcode', type=str, required=True, help='请输入验证码', location='json', store_missing=False)
        super(LoginResource, self).__init__()

    def get(self):
        return {'hello': 'login'}

    def post(self):

        args = self.parser.parse_args()
        username = args.get('username')
        #password = args.get('password')
        user = User.query.filter_by(wechat=username).first()

        if not user:
            return {Const.MESSAGE_KEY: '该用户不存在'}, Const.STATUS_ERROR

        # if not user.verify_password(password):
        #     return {Const.MESSAGE_KEY: '密码错误'}, Const.STATUS_ERROR
        user_manager.login(user)
        print('-*-**-*-',user_manager.current_user)

        return {Const.MESSAGE_KEY: '登陆成功'}, Const.STATUS_OK

class UserListResource(Resource):
    pass




@user_manager.user_loader
def user_loader(uid):
    uid = str(uid)
    if uid is None:
        return None

    try:
        return User.query.get(uid)

    except TypeError:
        return None
    except ValueError:
        return None


@user_manager.hash_generator
def hash_generator(user):
    from app.utils.utils import generate_user_hash

    return generate_user_hash(user.get_id(), user.password, user_manager.expires, user_manager.salt)

