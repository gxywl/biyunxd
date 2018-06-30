# _*_ encoding: utf-8 _*_

from flask import url_for, request
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect

from app.models import User, Xiaoqu, Kehu, Chanpin, Dingdan


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'adm'

    #跳转
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class UserView(MyModelView):
#    can_edit = False
#    can_delete = False
#    can_create = False
#    page_size = 5

    # 这里是为了自定义显示的column名字
    column_labels = dict(
        user=u'用户',     username=u'用户名',
    )
#     #column_list = ('Email', 'Username')
#     # column_labels = {
#     #     'Email':u'邮件地址',
#     #     'Username':u'用户名',
#     # }

#     #如果不想显示某些字段，可以重载这个变量
#     column_exclude_list = (
#         'password_hash',
#     )
#
#     column_list = (
#         'username','email',
#     )
#
#
    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)

class XiaoquView(MyModelView):
#    can_edit = False
#    can_delete = False
#    can_create = False
#    page_size = 5

    # 这里是为了自定义显示的column名字
    column_labels = dict(
        xiaoqu=u'小区',     dizhi=u'地址',
    )
#     #column_list = ('Email', 'Username')
#     # column_labels = {
#     #     'Email':u'邮件地址',
#     #     'Username':u'用户名',
#     # }

#     #如果不想显示某些字段，可以重载这个变量
#     column_exclude_list = (
#         'password_hash',
#     )
#
#     column_list = (
#         'username','email',
#     )
#
#
    def __init__(self, session, **kwargs):
        super(XiaoquView, self).__init__(Xiaoqu, session, **kwargs)

class KehuView(MyModelView):
#    can_edit = False
#    can_delete = False
#    can_create = False
#    page_size = 5

    # 这里是为了自定义显示的column名字
    column_labels = dict(
        fangjian=u'房间',     chenghu=u'称呼',   tel=u'电话',
    )
   #     #column_list = ('Email', 'Username')
#     # column_labels = {
#     #     'Email':u'邮件地址',
#     #     'Username':u'用户名',
#     # }

#     #如果不想显示某些字段，可以重载这个变量
#     column_exclude_list = (
#         'password_hash',
#     )
#
#     column_list = (
#         'username','email',
#     )
#
#
    def __init__(self, session, **kwargs):
        super(KehuView, self).__init__(Kehu, session, **kwargs)

class ChanpinView(MyModelView):
#    can_edit = False
    can_delete = False
    can_create = False
#    page_size = 5

    # 这里是为了自定义显示的column名字
    column_labels = dict(
        pinming=u'品名',     jiage=u'价格',   beizhu=u'备注',
    )
#     #column_list = ('Email', 'Username')
#     # column_labels = {
#     #     'Email':u'邮件地址',
#     #     'Username':u'用户名',
#     # }

#     #如果不想显示某些字段，可以重载这个变量
#     column_exclude_list = (
#         'password_hash',
#     )
#
#     column_list = (
#         'username','email',
#     )
#
#
    def __init__(self, session, **kwargs):
        super(ChanpinView, self).__init__(Chanpin, session, **kwargs)

class DingdanView(MyModelView):
#    can_edit = False
#    can_delete = False
#    can_create = False
#    page_size = 5

    # 这里是为了自定义显示的column名字
    column_labels = dict(
        shuliang=u'数量',     weizhi=u'位置',   xinghao=u'型号',
    )
#     #column_list = ('Email', 'Username')
#     # column_labels = {
#     #     'Email':u'邮件地址',
#     #     'Username':u'用户名',
#     # }

#     #如果不想显示某些字段，可以重载这个变量
#     column_exclude_list = (
#         'password_hash',
#     )
#
#     column_list = (
#         'username','email',
#     )
#
#
    def __init__(self, session, **kwargs):
        super(DingdanView, self).__init__(Dingdan, session, **kwargs)

class MyAdminIndexView(AdminIndexView):
    #增加这个必须要登录后才能访问，不然显示403错误
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'adm'

    #跳转
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    #后台首页
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    # @expose('/user')
    # def user(self):
    #     return self.render('admin/user.html')
    #
    # @expose('/xiangmu')
    # def xiangmu(self):
    #     return self.render('admin/xiangmu.html')
    #
    # @expose('/bujuan')
    # def bujuan(self):
    #     return self.render('admin/bujuan.html')

