#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
import os
import unittest

from flask import url_for, request, redirect
from flask_admin import AdminIndexView, expose, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_login import current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db


from app.models import User, Kehu, Dingdan, Chanpin, Xiaoqu

app=create_app(os.getenv('BY_CONFIG') or 'default')

# manager = Manager(app)
# migrate=Migrate(app,db)
#
#
# def make_shell_context():
#     return dict(db=db, User=User, Guke=Kehu, Dingdan=Dingdan, Chanpin=Chanpin, Xiaoqu=Xiaoqu)
#
# manager.add_command('shell', Shell(make_context=make_shell_context))
#
# manager.add_command('db', MigrateCommand)
#
# @manager.command
# def test():
#     """Run the unit tests"""
#     tests=unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#
# if __name__ == '__main__':
#     manager.run()


#临时用于解决 在template中定义模板的问题－－－kefucxlist.html中使用－
# －{% set ishavedd='1' %}只能在同一层使用。对外层失效
global_var = [0]  # 定义一个全局变量，存在相应的值

def set_var(var):  # 设置全局变量
    global_var[0] = var
    return ""

def get_var():  # 获取全局变量
    return global_var[0]

#使用flask对jinja2环境变量操作，来完成jinja2全局函数的配置
app.add_template_global(set_var, 'set_var')
app.add_template_global(get_var, 'get_var')
#－－－－



if __name__ == '__main__':
    app.run()