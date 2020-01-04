from . import db
from enum import unique, Enum
from flask_loginmanager import UserMixin
from marshmallow import fields, Schema
#新闻状态

class NewStatus(Enum):
    Submitted = '已提交'
    Rejected = '已驳回'
    Confirmed = '已确认'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wechat = db.Column(db.String(20))
    wallet = db.Column(db.Float(), default=0)
    password = db.Column(db.String(20))
    register_time = db.Column(db.TIMESTAMP, server_default=db.func.now())
    appid = db.Column(db.String(100))
    #merchant = db.relationship('Article', back_populates="user")

class UsersSchema(Schema):
    class Meta:
        fields = ('id', 'wechat', 'password', 'wallet', 'appid' 'register_time')
        ordered = False


class Merchants(db.Model):
    __tablename__ = "merchant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(50))
    dizhi = db.Column(db.String(100))
    register_time = db.Column(db.TIMESTAMP, server_default=db.func.now())
    wechat = db.Column(db.String(20))
    password = db.Column(db.String(20))

    article = db.relationship('Article', backref='role', lazy='dynamic')

    def get_id(self):

        return self.id

    def verify_password(self, password):
        return self.password == password

class MerchantsSchema(Schema):
    article_id = fields.String()
    class Meta:
        additional = ('id', 'name', 'address', 'password', 'wechat', 'register_time')



class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), default="")
    picture =db.Column(db.String(30), default="")
    content = db.Column(db.Text())
    hongbao_money = db.Column(db.Float(), default=0)
    hongbao_number = db.Column(db.Integer, default=1000)
    status = db.Column(db.Enum(NewStatus), default=NewStatus.Submitted)
    use_id = db.Column(db.Text(), default="")
    register_time = db.Column(db.TIMESTAMP, server_default=db.func.now())
    through_time = db.Column(db.String(50), default="")
    dizhi = db.Column(db.String(100))
    point = db.Column(db.String(100))
    #use_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    mer_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))

class ArtSchema(Schema):
    mer_name = fields.String()
    class Meta:
        additional = ('title', 'picture', 'content', 'through_time', 'dizhi', 'point')

class ArticleSchema(Schema):
    status = fields.String()
    class Meta:
        additional = ('id', 'title', 'picture', 'content', 'register_time', "hongbao_money", "hongbao_number", 'mer_id','use_id', 'register_time')

# 管理员表
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    permissions = db.Column(db.BigInteger, nullable=False, default=0)
    #dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    latest = db.Column(db.TIMESTAMP, server_default=db.func.now())
    status = db.Column(db.Boolean(True))

    def get_id(self):
        return self.id

    def get_permissions(self):
        return self.permissions

    def verify_password(self, password):
        return self.password == password


class AdminSchema(Schema):
    class Meta:
        additional = ('id', 'name', 'email', 'latest', 'status')
        ordered = False



class Const(object):
    MESSAGE_KEY = 'message'
    STATUS_ERROR = 400
    STATUS_DENIED = 401
    STATUS_OK = 200



