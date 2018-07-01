# _*_ encoding: utf-8 _*_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

from app.models import User


class LoginForm(FlaskForm):
    user = StringField('账号', validators=[DataRequired()])
    # , render_kw = {"placeholder": "Your name","style": "background: url(/static/login-locked-icon.png) no-repeat 15px center;text-indent: 28px"}
    pin = PasswordField('校验码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class ChangeUserNameForm(FlaskForm):
    username = StringField('用户姓名', validators=[DataRequired()])
    submit = SubmitField('更改')

class ChangePinForm(FlaskForm):
    opin = PasswordField('原口令', validators=[DataRequired()])
    npin = PasswordField('新口令', validators=[DataRequired(),EqualTo('confirm', message="两次口令不一致")])
    # rpin = PasswordField('新口令(重复)', validators=[DataRequired(),EqualTo(npin, message=None)])
    confirm = PasswordField('新口令(重复)')
    submit = SubmitField('更改口令')
