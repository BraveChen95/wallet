#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/8 21:05
# @Author  : Brave
# @Desc    : 商家信息表
# @File    : merchant_resource.py

from flask_restful import reqparse, Resource
from app.models import Merchants, MerchantsSchema, Const
from app import admin_manager, db
from app.utils.utils import merge, safe_session

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, location='json', store_missing=False)
parser.add_argument("wechat", type=str, location='json', store_missing=False)
parser.add_argument("wallet", type=str, location='json', store_missing=False)
parser.add_argument("password", type=str, location='json', store_missing=False)
class MerchantsResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self,mid):
        mer = Merchants.query.get_or_404(mid)
        schema = MerchantsSchema()
        result = schema.dump(mer)
        return {'merchants': result}, Const.STATUS_OK

    def post(self, mid):
        mer = Merchants.query.get_or_404(mid)
        args = parser.parse_args()
        merge(mer, args)
        with safe_session(db):
            db.session.add(mer)

        return {Const.MESSAGE_KEY: '商家信息修改成功'}, Const.STATUS_OK


class MerchantsListResource(Resource):

    def get(self):
       mer = Merchants.query.all()
       schema = MerchantsSchema(many=True)
       result = schema.dump(mer)

       return {'merchants': result}, Const.STATUS_OK

    def post(self):
        mer = Merchants()
        args = parser.parse_args()

        merge(mer, args)
        with safe_session(db):
            db.session.add(mer)

        return {Const.MESSAGE_KEY: '成功创建商家'}, Const.STATUS_OK

