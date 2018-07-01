# _*_ encoding: utf-8 _*_
from flask import Flask
from flask_babelex import Babel

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

from config import config

moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()
# from app.exts import db

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

babel = Babel()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment = Moment(app)
    bootstrap = Bootstrap(app)

    db.init_app(app)
    login_manager.init_app(app)

    # ----------------------
    from app.admin import MyAdminIndexView, UserView, MyModelView,KehuView, ChanpinView, XiaoquView, DingdanView, ChanpinxxView
    from app.models import Kehu, Dingdan, Chanpin, Xiaoqu

    babel.init_app(app)

    # admin = Admin(app, name='后台页', template_mode='bootstrap3',index_view=AdminIndexView(name='导航栏',template='admin/welcome.html')) #,url='/admin'
    admin = Admin(app, name='数据管理', template_mode='bootstrap3', index_view=MyAdminIndexView())

    # Add administrative views here
    admin.add_view(UserView(db.session, name='用户'))
    # admin.add_view(ModelView(Post, db.session, category='Models'))

    admin.add_view(KehuView(db.session, name='客户'))
    admin.add_view(ChanpinView(db.session, name='产品'))
    admin.add_view(XiaoquView(db.session, name='小区'))
    admin.add_view(DingdanView(db.session, name='订单'))
    admin.add_view(ChanpinxxView(db.session, name='选项设置'))

    # models = [Kehu, Dingdan, Chanpin, Xiaoqu]
    # for model in models:
    #     admin.add_view(MyModelView(model, db.session, category='Models'))

    # ----------------------

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # ...

    return app
