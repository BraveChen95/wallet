#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 21:05
# @Author  : Brave
# @Desc    : 商家信息表
# @File    : uesrs_resource.py

from flask_restful import reqparse, Resource
from app.models import User, UsersSchema, Const
from app import admin_manager, db
from app.utils.utils import merge, safe_session

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, location='json', store_missing=False)
parser.add_argument("wechat", type=str, location='json', store_missing=False)
parser.add_argument("password", type=str, location='json', store_missing=False)

class UsersResource(Resource):
    #method_decorators = [admin_manager.login_required()]
    def get(self,mid):
        user = User.query.get_or_404(mid)
        schema = UsersSchema()
        result = schema.dump(user)
        return {'users': result}, Const.STATUS_OK

    def post(self, mid):
        mer = User.query.get_or_404(mid)
        args = parser.parse_args()
        merge(mer, args)
        with safe_session(db):
            db.session.add(mer)
        return {Const.MESSAGE_KEY: '用户信息修改成功'}, Const.STATUS_OK

class UsersListResource(Resource):

    def get(self):
        print('-*---------')
        user = User.query.all()
        schema = UsersSchema(many=True)
        result = schema.dump(user)
        print(result)
        return {'users': result}, Const.STATUS_OK