#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 下午5:10
# @Author  : Brave
# @Desc    : 用户操作页面
# @File    : views.py

from flask import request, jsonify, session
from app.models import Merchants, Article, Const, ArticleSchema, ArtSchema
from app.utils.utils import merge, safe_session
from flask_restful import reqparse, Resource
from app import db, user_manager
import sqlalchemy


class MapResource(Resource):
    def get(self):
        return {'hello': 'map'}

class MerchantsLoginResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='请输入用户名', location='json', store_missing=False)
        self.parser.add_argument('password', type=str, required=True, help='请输入密码', location='json', store_missing=False)
        self.parser.add_argument('vcode', type=str, required=True, help='请输入验证码', location='json', store_missing=False)
        super(MerchantsLoginResource, self).__init__()

    def get(self):
        return {'hello': 'login'}

    def post(self):

        args = self.parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        vcode = args.get('vcode')
        if vcode.upper()!= session.get('vcode','').upper():
            return {Const.MESSAGE_KEY: '验证码错误'}, Const.STATUS_ERROR
        user = Merchants.query.filter_by(name=username).first()

        if not user:
            return {Const.MESSAGE_KEY: '该用户不存在'}, Const.STATUS_ERROR

        if not user.verify_password(password):
            return {Const.MESSAGE_KEY: '密码错误'}, Const.STATUS_ERROR
        user_manager.login(user)
        session.pop('vcode')
        return {Const.MESSAGE_KEY: '登陆成功'}, Const.STATUS_OK

class RegisterResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='请输入用户名', location='json', store_missing=False)
        self.parser.add_argument('password', type=str, required=True, help='请输入密码', location='json', store_missing=False)
        self.parser.add_argument('vcode', type=str, required=True, help='请输入验证码', location='json', store_missing=False)
        super(RegisterResource, self).__init__()

    def get(self):
        return {'hello': 'login'}

    def post(self):

        args = self.parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        vcode = args.get('vcode')
        if vcode.upper()!= session.get('vcode','').upper():
            return {Const.MESSAGE_KEY: '验证码错误'}, Const.STATUS_ERROR
        user = Merchants.query.filter_by(iphon=username).first()
        if user:
            return {Const.MESSAGE_KEY: '该用户已存在'}, Const.STATUS_ERROR
        merchants = Merchants()
        args = self.parser.parse_args()
        merge(merchants, args)
        with safe_session(db):
            db.session.add(merchants)

        session.pop('vcode')
        return {Const.MESSAGE_KEY: '注册成功'}, Const.STATUS_OK




# 手机验证码登录
class CodeLoginResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='请输入用户名', location='json',
                                 store_missing=False)
        self.parser.add_argument('vcode', type=str, required=True, help='请输入验证码', location='json',
                                 store_missing=False)
        super(CodeLoginResource, self).__init__()

    def get(self):
        return {'hello': 'login'}

    def post(self):
        args = self.parser.parse_args()
        username = args.get('username')
        vcode = args.get('vcode')
        user = Merchants.query.filter_by(phone=username).first()
        if not user:
            return {Const.MESSAGE_KEY: "用户输入有误"}, Const.STATUS_ERROR

        if vcode.upper() != session.get('vcode', '').upper():
            return {Const.MESSAGE_KEY: '验证码错误'}, Const.STATUS_ERROR
        user_manager.login(user)
        session.pop('vcode')

        return {Const.MESSAGE_KEY: "登录成功"}, Const.STATUS_ERROR


# 修改密码
class ResetPasswordResource(Resource):
    method_decorators = [user_manager.login_required()]

    def __init__(self):
        self.parseer = reqparse.RequestParser()
        self.parseer.add_argument('new_pwd1', type=str, required=True, help='请输入密码', location='json',
                                  store_missing=False)
        self.parseer.add_argument('new_pwd', type=str, required=True, help='请再输一次', location='json',
                                  store_missing=False)
        super(ResetPasswordResource, self).__init__()

    def post(self):
        args = self.parseer.parse_args()
        user = user_manager.current_user

        if args.get('new_pwd1') == args.get('new_pwd'):
            user.password = args.get('new_pwd')
            merge()
            with safe_session(db):
                db.session.add(user)

            return {Const.MESSAGE_KEY: '密码修改成功'}, Const.STATUS_OK

        return {Const.MESSAGE_KEY: '原密码错误'}, Const.STATUS_ERROR


#修改文章
class PublishedNewsResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True, location='json', store_missing=False )
        self.parser.add_argument('picture', type=str, required=True, location='json', store_missing=False )
        self.parser.add_argument('content', type=str, required=True, location='json', store_missing=False )
        #self.parser.add_argument('stratus', type=str, required=True, location='json', store_missing=False )
        super(PublishedNewsResource, self).__init__()

    def get(self, aid):
        #mer = user_manager.current_user
        art =Article.query.get_or_404(aid)
        print(art)
        schema = ArticleSchema()
        result = schema.dump(art)
        return {"result": result}, Const.STATUS_OK
    def post(self, aid):
        art = Article.query.get_or_404(aid)
        args = self.parser.parse_args()
        args["stratus"] ='Submitted'

        merge(art, args)
        # try:
        with safe_session(db):
            db.session.add(art)
        # except sqlalchemy.exc.IntegrityError as e:
        #     print('create admin error:', e)
        #     return {Const.MESSAGE_KEY: '创建管理员失败，该邮箱地址已存在'}, Const.STATUS_ERROR
            return {Const.MESSAGE_KEY: '新闻修改成功'}, Const.STATUS_OK

#文章展示
class NewShowResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('point', type=str, required=True, location='json', store_missing=False)
        self.parser.add_argument('time', type=str, required=True, location='json', store_missing=False)
        # self.parser.add_argument('stratus', type=str, required=True, location='json', store_missing=False )
        super(NewShowResource, self).__init__()

    def get(self):
        import time
        shijian=time.time()-24*3600
        article = Article.query.filter(Article.through_time.__ge__(shijian)).all()
        article = Article.query.all()

        print(article)

        schema = ArtSchema(many=True)

        result = schema.dump(article)
        print(result)
        return {'article': result}, Const.STATUS_OK
    def post(self):
        art={}
        point = request.json.get("point")
        time = request.json.get("time")
        article = Article.query.filter_by(point=point,through_time=time).first().first()
        art['title']= article.title
        art['content']= article.content
        art['picture']= article.picture
        return {'article': art}, Const.STATUS_OK



class NewListResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True, location='json', store_missing=False )
        self.parser.add_argument('picture', type=str, required=True, location='json', store_missing=False )
        self.parser.add_argument('content', type=str, required=True, location='json', store_missing=False )
        #self.parser.add_argument('stratus', type=str, required=True, location='json', store_missing=False )
        super(NewListResource, self).__init__()
    def get(self):
        mer = user_manager.current_user
        art = Article.query.filter_by(mer_id=mer.id).all()
        print(art)
        schema = ArticleSchema(many=True)
        result = schema.dump(art)

        return {'newlist': result}, Const.STATUS_OK
    def post(self):
        article = Article()
        args = self.parser.parse_args()
        merge(article, args)
        with safe_session(db):
            db.session.add(article)
        return {Const.MESSAGE_KEY: '成功创建管理员'}, Const.STATUS_OK



@user_manager.user_loader
def user_loader(uid):
    uid = str(uid)
    if uid is None:
        return None

    try:
        return Merchants.query.get(uid)

    except TypeError:
        return None
    except ValueError:
        return None

@user_manager.hash_generator
def hash_generator(user):
    from app.utils.utils import generate_user_hash

    return generate_user_hash(user.get_id(), user.password, user_manager.expires, user_manager.salt)

