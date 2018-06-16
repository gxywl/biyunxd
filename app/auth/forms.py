# _*_ encoding: utf-8 _*_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

from app.models import User


class LoginForm(FlaskForm):
    user = StringField('账号', validators=[DataRequired()])
    pin = PasswordField('校验码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class ChangeUserNameForm(FlaskForm):
    username = StringField('用户姓名', validators=[DataRequired()])
    submit = SubmitField('更改')
