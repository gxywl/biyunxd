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

app=create_app(os.getenv('LSHS_CONFIG') or 'default')

manager = Manager(app)
migrate=Migrate(app,db)


def make_shell_context():
    return dict(db=db, User=User, Guke=Kehu, Dingdan=Dingdan, Chanpin=Chanpin, Xiaoqu=Xiaoqu)

manager.add_command('shell', Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests"""
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
