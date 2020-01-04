#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 23:30
# @Author  : Brave
# @Desc    : 管理员接口
# @File    : admin_resource.py
from flask import request,g

from flask_restful import Resource, reqparse
from app import admin_manager, db
from app.models import Admin, AdminSchema, Const
from app.utils.utils import merge, safe_session
import sqlalchemy
from sqlalchemy.sql import and_


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('email', type=str, location='json', store_missing=False)
parser.add_argument('password', type=str, location='json', store_missing=False)

class AdminResource(Resource):

    def get(self, aid):

        admin = Admin.query.get_or_404(aid)
        schema = AdminSchema(many=False)
        result = schema.dump(admin)
        return {'admin':result}, Const.STATUS_OK

    def post(self,aid):
        print(aid)
        admin = Admin.query.get_or_404(aid)
        args = parser.parse_args()
        print(admin, args)
        merge(admin, args)
        with safe_session(db):
            db.session.add(admin)

        return {Const.MESSAGE_KEY: '管理员信息修改成功'}, Const.STATUS_OK


class AdminListResource(Resource):
    #method_decorators = [admin_manager.login_required()]

    def get(self):
        user=admin_manager.current_user
        condition = (Admin.id > 0)
        if request.args.get('account'):
            acc = request.args.get("account")
            condition = and_(condition,Admin.name==acc)
        if request.args.get('tele'):
            request.args.get = and_(condition, Admin.email=='tele')
        admins = Admin.query.filter(condition)

        # for a in admins:
        #     a.dept_name = a.department.name
        #     a.role_name = a.role.name

        schema = AdminSchema(many=True)
        result = schema.dump(admins)

        # login_name={"login_name":user.name}
        print(result)
        return {'admins': result}, Const.STATUS_OK

    def post(self):

        admin = Admin()
        args = parser.parse_args()
        print(args)
        merge(admin, args)

        try:
            with safe_session(db):
                db.session.add(admin)
        except sqlalchemy.exc.IntegrityError as e:
            print('create admin error:', e)
            return {Const.MESSAGE_KEY: '创建管理员失败，该邮箱地址已存在'}, Const.STATUS_ERROR

        return {Const.MESSAGE_KEY: '成功创建管理员'}, Const.STATUS_OK