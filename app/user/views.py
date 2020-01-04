#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 下午5:10
# @Author  : Brave
# @Desc    : 用户操作页面
# @File    : views.py

from flask import  Flask, request, jsonify
from flask_restful import Resource,reqparse
import json
from app.models import User, UsersSchema, Const, Article
import urllib.request
from app.utils.utils import merge, safe_session, get_hongbao
from app import db, user_manager


WECHAT_TOKEN = "python"
WECHAT_APPID = "wxe123456789"
WECHAT_APPSECRET = "123456789"
class UserLoginResource(Resource):
    def get(self):
        #从微信服务器上拿取用户的资料
        #拿取code参数
        code = request.args.get("code")
        if not code:

            return "缺少code参数"
        #向微信服务器发送http请求，获取access_toke
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % \
              (WECHAT_APPID, WECHAT_APPSECRET, code)

        # 使用urllib2的urlopen方法发送请求
        # 如果只传网址url参数，则默认使用http的get请求方式,返回响应对象
        response = urllib.request.urlopen(url)

        # 获取响应体数据，微信返回的json数据
        json_str = response.read()
        resp_dict = json.loads(json_str)

        #提取access_token
        if "errcode" in resp_dict:
            return u"获取acces_token失败"
        access_token = resp_dict.get("access_token")
        open_id = resp_dict.get("openid")  # 用户的编号

        #.向微信服务器发送http请求，获取用户信息
        url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % \
              (access_token, open_id)

        response = urllib.request.urlopen(url)
        # 读取微信传回的json的响应体数据
        user_json_str = response.read()
        user_dict_data = json.loads(user_json_str)
        # print(user_dict_data)
        if "errcode" in user_dict_data:
            return u"获取用户信息失败"
        else:
            # 将用户的资料数据填充到页面中
            return jsonify(user_dict_data)




class ArticleResource(Resource):

    def get(self, aid):
        print('--*-')
        article = Article.query.get_or_404(aid)
        schema = UsersSchema()
        result = schema.dump(article)
        return {"wallet": result}, Const.STATUS_OK

    def post(self,aid):
        article = Article.query.get_or_404(aid)
        use_id = user_manager.current_user
        print('-*-------',use_id.id)
        user = User.query.get_or_404(use_id.id)
        print(article.use_id)
        print(str(use_id.id))
        if str(use_id.id) not in list(article.use_id):
            use_id=article.use_id+str(use_id.id)
            hongbao_money=get_hongbao(article.hongbao_money,article.hongbao_number)
            user.wallet +=hongbao_money["hongbao_money"]
            print(hongbao_money)
            args={"hongbao_money":hongbao_money["hogbao_remain"], "hongbao_number":hongbao_money["hogbao_num"],"use_id":use_id}
            merge(article, args)
            with safe_session(db):
                db.session.add(article)

            merge(user,{"wallet":user.wallet})
            with safe_session(db):
                db.session.add(user)
            return {Const.MESSAGE_KEY: '金额到账成功'}, Const.STATUS_OK

        else:
            return {Const.MESSAGE_KEY: '已经抢过红包'}, Const.STATUS_OK





