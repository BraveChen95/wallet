from flask import Blueprint, request, session,  session, jsonify
from flask_restful import Api, Resource
from bs4 import BeautifulSoup
import requests, re
import time
from app.main.views import LoginResource
import random
from app.utils.utils import veri_code
#from . import views

main = Blueprint("main", __name__)

api = Api(main)

api.add_resource(LoginResource, '/')



#微信登录

def xml_parser(text):
    dic = {}
    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find(name='error')
    for item in div.find_all(recursive=False):
        dic[item.name] = item.text
    return dic

@main.route('/wechat')
def wechat():
    '''获取微信二维码'''
    ctime = int(time.time() * 1000)
    qcode_url = "https://login.wx2.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}".format(
        ctime)

    rep = requests.get(
        url=qcode_url
    )
    # print(rep.text) # window.QRLogin.code = 200; window.QRLogin.uuid = "gb8UuMBZyA==";
    qcode = re.findall('uuid = "(.*)";', rep.text)[0]
    session['qcode'] = qcode
    return jsonify(qcode)

@main.route('/check/login')
def check_login():
    qcode = session['qcode']
    ctime = int(time.time() * 1000)
    # https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=oeq3xdRFig==&tip=0&r=-412057997&_=1546600257051
    # https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=oa95cvIS5w==&tip=0&r=-413943228&_=1546602155746
    check_login_url = 'https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-413943228&_={1}'.format(
        qcode, ctime)
    rep = requests.get(
        url=check_login_url
    )
    result = {'code': 408}

    if 'window.code=408' in rep.text:
        # 用户未扫码
        result['code'] = 408
    elif 'window.code=201' in rep.text:
        # 用户扫码，获取头像
        result['code'] = 201
        result['avatar'] = re.findall("window.userAvatar = '(.*)';", rep.text)[0]
    elif 'window.code=200' in rep.text:
        # 用户确认登录
        redirect_uri = re.findall('window.redirect_uri="(.*)";', rep.text)[0]
        print(redirect_uri)

        # https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A_pgPh0SjvyHWTDEF3kce2Wg@qrticket_0&uuid=wbewGl1rwQ==&lang=zh_CN&scan=1546599481&fun=new&version=v2
        # https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A_pgPh0SjvyHWTDEF3kce2Wg@qrticket_0&uuid=wbewGl1rwQ==&lang=zh_CN&scan=15

        redirect_uri = redirect_uri + "&fun=new&version=v2"
        ru = requests.get(url=redirect_uri)

        # <error><ret>0</ret><message></message><skey>@crypt_2272b9c9_c4a1df2d806c0b32bc7f8b678b907bd6</skey><wxsid>hKPtRPRAn0yZWwZW</wxsid><wxuin>1440810436</wxuin><pass_ticket>%2BuiXaDx68luSpK5djbIrAqKoVLi4vSlxTg7dQe4105vIaFK93ORlG1kPgO5uQsSi</pass_ticket><isgrayscale>1</isgrayscale></error>
        ticket_dict = xml_parser(ru.text)
        # print(ticket_dict)
        session['ticket_dict'] = ticket_dict
        result['code'] = 200

    return jsonify(result)

@main.route('/index')
def index():
    pass_ticket = session['ticket_dict']['pass_ticket']
    init_url = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-412030554&lang=zh_CN&pass_ticket={0}".format(
        pass_ticket)

    rep = requests.post(
        url=init_url,
        json={
            'BaseRequest': {
                'DeviceID': "e572672200373583",
                'Sid': session['ticket_dict']['wxsid'],
                'Skey': session['ticket_dict']['skey'],
                # 'Uin': session['ticket_dict']['wxuin'],
                'Uin': "1440810436",

            }
        }
    )
    rep.encoding = 'utf-8'

    init_user_dict = rep.json()
    print(init_user_dict)

    return jsonify(init_user_dict)


#获取手机验证码
@main.route('/test_code')
def phone_code():
    from app.utils.sms import send
    value = random.randint(0, 999999)
    code=('%06d') % value
    result = send('15701207613', code)
    if result:
        session['vcode'] = code
        return 'ok'
    return 'fail'

#获取图片验证码
@main.route('/v_code')
def prepare_v_code():
    code, path = veri_code()
    session['vcode'] = code

    return '../../static/code/'+path
