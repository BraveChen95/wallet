#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 下午17:23
# @Author  : Brave
# @Desc    : 生成验证码
# @File    : utils.py

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
import oss2
import uuid
import tempfile
import base64
import datetime
import hashlib
import hmac
import re
from contextlib import contextmanager
from collections import Iterable

from werkzeug.utils import secure_filename
import os


#生成用户hash
def generate_user_hash(*args):
    s = ''
    for arg in args:
        s += str(arg)

    return hashlib.sha256().hexdigest()


#生成图片验证码
# 随机码 默认长度=1
def random_code(lenght=1):
    code = ''
    for char in range(lenght):
        code += chr(random.randint(65, 90))
    return code


# 随机颜色 默认颜色范围【1，255】
def random_color(s=1, e=255):
    return (random.randint(s, e), random.randint(s, e), random.randint(s, e))

# 生成验证码图片
# length 验证码长度
# width 图片宽度
# height 图片高度
# 返回验证码和图片
def veri_code(lenght=4, width=160, height=40):
    # 创建Image对象
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象
    font = ImageFont.truetype('Arial.ttf', 36)
    # 创建Draw对象
    draw = ImageDraw.Draw(image)
    # 随机颜色填充每个像素
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=random_color(64, 255))
    # 验证码
    code = random_code(lenght)
    # 随机颜色验证码写到图片上
    for t in range(lenght):
        draw.text((40 * t + 5, 5), code[t], font=font, fill=random_color(32, 127))

    file_name = str(uuid.uuid4()) + '.png'
    # 模糊滤镜
    image = image.filter(ImageFilter.BLUR)
    image.save("/home/cy/PycharmProjects/news_feed/app/static/code/"+file_name,"png")
    return code, file_name

#生成手机验证码
def generate_verification_code():
    value = random.randint(0, 9999)

    return '%04d' % value


#验证邮箱
def validate_email(email):
    if re.match(r'^.+@([^.@][^@]+)$', email):
        return True
    return False

#处理上传图片
def get_iso_8601(expire):
    gmt = datetime.datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def get_sign_policy(key, policy):
    return base64.encodebytes(hmac.new(bytes(key.encode("utf-8")), policy, hashlib.sha1).digest()).strip()



@contextmanager
def safe_session(db):
    try:
        yield
        db.session.commit()
    except:
        db.session.rollback()
        raise
    # finally:
    #     db.session.close()

#进行修改数据库数据
def merge(obj, dic, ignore=()):
    for key, value in dic.items():
        if isinstance(ignore, Iterable) and key in ignore:
            continue

        if hasattr(obj, key):
            setattr(obj, key, value)


#用户获取红包

def get_hongbao(hongbao_remain,hongbao_num):
    min = 0.01
    max = 0.1
    money = round(random.uniform(0, max), 2)
    hongbao_money = money if money > min else min
    hongbao_num -= 1
    hongbao_remain -= hongbao_money

    return {"hongbao_money":hongbao_money, "hogbao_num":hongbao_num,"hogbao_remain":hongbao_remain}


#处理图片上传
from flask  import jsonify

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload(f):
    if not (f and allowed_file(f.filename)):
        return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})


    basepath = os.path.dirname(__file__)  # 当前文件所在路径

    upload_path = os.path.join(basepath, '/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)