# _*_ encoding: utf-8 _*_
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True, index=True)
    pin = db.Column(db.String(64))
    username = db.Column(db.String(64))

    role = db.Column(db.String(64))
    isuse = db.Column(db.Boolean, default=False)

    kehus = db.relationship('Kehu', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_pin(self, pin):
        return self.pin == pin

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Xiaoqu(db.Model):
    __tablename__ = 'xiaoqus'
    id = db.Column(db.Integer, primary_key=True)
    xiaoqu = db.Column(db.String(64), unique=True, index=True)
    weizhi = db.Column(db.String(100))

    kehus = db.relationship('Kehu', backref='xiaoqu', lazy='dynamic')
    #kehus = db.relationship('Kehu', primaryjoin="and_(Xiaoqu.id==Kehu.xiaoqu_id)",backref='xiaoqu', lazy='dynamic')

    def __repr__(self):
        return '<Xiaoqu %r>' % self.xiaoqu


class Chanpin(db.Model):
    __tablename__ = 'chanpins'
    id = db.Column(db.Integer, primary_key=True)
    pinming = db.Column(db.String(64))
    danjia = db.Column(db.Float)
    dingdans = db.relationship('Dingdan', backref='chanpin', lazy='dynamic')

    def __repr__(self):
        return '<Chanpin %r>' % self.pinming


class Kehu(db.Model):
    __tablename__ = 'kehus'
    id = db.Column(db.Integer, primary_key=True)
    #xiaoqu = db.Column(db.String(64))
    donghao = db.Column(db.String(64))
    fanghao = db.Column(db.String(64))
    chenghu = db.Column(db.String(64))
    tel = db.Column(db.String(64))
    status = db.Column(db.String(64), default='No')
    xdtime = db.Column(db.DateTime(), default=datetime.utcnow)

    # beizhu = db.Column(db.String(64))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    xiaoqu_id = db.Column(db.Integer, db.ForeignKey('xiaoqus.id'))

    dingdans = db.relationship('Dingdan', backref='kehu', lazy='dynamic')

    def __repr__(self):
        return '<Kehu %r>' % self.id


class Dingdan(db.Model):
    __tablename__ = 'dingdans'
    id = db.Column(db.Integer, primary_key=True)
    shuliang = db.Column(db.Integer)
    weizhi = db.Column(db.String(64))
    xinghao = db.Column(db.String(64))
    kuan_chang = db.Column(db.Integer)
    gao = db.Column(db.Integer)
    meikuan_digao = db.Column(db.Integer)
    color = db.Column(db.String(64))
    shanshu = db.Column(db.Integer)
    zhonghengtiaoshu_gantiaoshu = db.Column(db.Integer)
    shuowei = db.Column(db.String(64))
    zhangfa = db.Column(db.String(64))
    ishaveht = db.Column(db.Boolean, default=False)
    dengfenshu = db.Column(db.String(64))
    danjia = db.Column(db.Float)
    tushipic = db.Column(db.String(64))
    status = db.Column(db.String(64), default='No')

    fakaidi = db.Column(db.String(64))
    fahuotime = db.Column(db.DateTime(), default=datetime.utcnow)

    #beizhu = db.Column(db.String(64))

    kehu_id = db.Column(db.Integer, db.ForeignKey('kehus.id'))
    chanpin_id = db.Column(db.Integer, db.ForeignKey('chanpins.id'))

    def __repr__(self):
        return '<Dingdan %r>' % self.id
