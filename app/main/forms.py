from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    name = StringField(validators=[DataRequired('请输入用户名')])
    password = PasswordField(validators=[DataRequired('请输入密码')])