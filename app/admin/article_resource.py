#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/8 21:50
# @Author  : Brave
# @Desc    : 商家发布新闻表
# @File    : article_resource.py

from flask_restful import Resource, reqparse
from app.models import Article, ArticleSchema, Const
from app import  db, admin_manager
from app.utils.utils import merge, safe_session

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, location='json', store_missing=False)
parser.add_argument("picture", type=str, location='json', store_missing=False)
parser.add_argument("content", type=str, location='json', store_missing=False)
parser.add_argument("register_time", type=str, location='json', store_missing=False)
parser.add_argument("hongbao_money", type=str, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)
#parser.add_argument("register_time", type=str, location='json', store_missing=False)

class ArticleResource(Resource):

    def get(self, aid):
        art = Article.query.get_or_404(aid)
        schema = ArticleSchema()
        result = schema.dump(art)
        return {'article': result}, Const.STATUS_OK

    def post(self, aid):
        art = Article.query.get_or_404(aid)
        args = parser.parse_args()
        print(args)
        merge(art, args)
        with safe_session(db):
            print(art)
            db.session.add(art)

        return {Const.MESSAGE_KEY: '新闻修改成功'}, Const.STATUS_OK


class ArticleListResource(Resource):

    def get(self):
        article = Article.query.all()
        schema = ArticleSchema(many=True)
        result = schema.dump(article)

        print(result)
        return {'article': result}, Const.STATUS_OK

    def post(self):
        art = Article()
        args = parser.parse_args()
        merge(art, args)
        with safe_session(db):
            db.session.add(art)

        return {Const.MESSAGE_KEY: '成功创建新闻'}, Const.STATUS_OK