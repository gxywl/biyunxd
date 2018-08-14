# _*_ encoding: utf-8 _*_
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager

# class Gongren( db.Model):
#     __tablename__ = 'gongrens'
#     id = db.Column(db.Integer, primary_key=True)
#     duizhang = db.Column(db.String(64), unique=True, index=True)
#     tuandui = db.Column(db.String(64))
#     beizhu = db.Column(db.String(64))
#
#     def __repr__(self):
#         return '<Gongren %r>' % self.duizhang

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True, index=True)
    pin = db.Column(db.String(64))
    username = db.Column(db.String(64))
    tel = db.Column(db.String(32))
    role = db.Column(db.String(64))
    isuse = db.Column(db.Boolean, default=False)
    beizhu = db.Column(db.String(64))

    kehus = db.relationship('Kehu', backref='user', lazy='dynamic')

    # azcps = db.relationship('Dingdan', backref='azer', lazy='dynamic')


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
    dizhi = db.Column(db.String(100))
    beizhu = db.Column(db.String(128))

    kehus = db.relationship('Kehu', backref='xiaoqu', lazy='dynamic')

    # kehus = db.relationship('Kehu', primaryjoin="and_(Xiaoqu.id==Kehu.xiaoqu_id)",backref='xiaoqu', lazy='dynamic')

    def __repr__(self):
        return '<Xiaoqu %r>' % self.xiaoqu


class Chanpin(db.Model):
    __tablename__ = 'chanpins'
    id = db.Column(db.Integer, primary_key=True)
    pinming = db.Column(db.String(64))
    jiage = db.Column(db.Float)
    beizhu = db.Column(db.String(64))

    dingdans = db.relationship('Dingdan', backref='chanpin', lazy='dynamic')

    def __repr__(self):
        return '<Chanpin %r>' % self.pinming


class Chanpinxx(db.Model):
    __tablename__ = 'chanpinxxs'
    id = db.Column(db.Integer, primary_key=True)
    pinming = db.Column(db.String(64))
    chanshux = db.Column(db.String(64))
    chanshuz = db.Column(db.String(128))
    xuhao = db.Column(db.Integer)

    def __repr__(self):
        return '<Chanpinxx %r>' % self.pinming


class Kehu(db.Model):
    __tablename__ = 'kehus'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    xiaoqu_id = db.Column(db.Integer, db.ForeignKey('xiaoqus.id'))
    fangjian = db.Column(db.String(64))
    chenghu = db.Column(db.String(64))
    tel = db.Column(db.String(64))
    zje = db.Column(db.Float)
    beizhu = db.Column(db.String(64))
    status = db.Column(db.Integer, default=1)  # 1已测尺、2已下单、3已安装、4已清款
    time0 = db.Column(db.DateTime(), default=datetime.utcnow)
    time1 = db.Column(db.DateTime())
    time2 = db.Column(db.DateTime())
    time3 = db.Column(db.DateTime())

    dingdans = db.relationship('Dingdan', backref='kehu', lazy='dynamic')

    def __repr__(self):
        return '<Kehu %r>' % self.id


class Dingdan(db.Model):
    __tablename__ = 'dingdans'
    id = db.Column(db.Integer, primary_key=True)
    kehu_id = db.Column(db.Integer, db.ForeignKey('kehus.id'))
    chanpin_id = db.Column(db.Integer, db.ForeignKey('chanpins.id'))
    shuliang = db.Column(db.Integer)
    weizhi = db.Column(db.String(64))
    xinghao = db.Column(db.String(64))
    kuan_chang = db.Column(db.Integer)
    gao = db.Column(db.Integer)
    meikongkuan_bashoudigao = db.Column(db.Integer)
    color = db.Column(db.String(64))
    shanshu = db.Column(db.Integer)
    zhonghengtiaoshu_gantiaoshu = db.Column(db.Integer)
    shuowei = db.Column(db.String(64))
    ishaveht = db.Column(db.String(64))
    zhangfa_dengfenshu_kaishuofangshi = db.Column(db.String(64))
    jiage = db.Column(db.Float)
    tushipic = db.Column(db.String(64))
    beizhu = db.Column(db.String(64))
    status = db.Column(db.Integer, default=1)  # 1测尺、2业务下单、3工厂下单、4工厂入库、5工厂发货、6收货、7派工、8装完、9安清款
    fakaidi = db.Column(db.String(64))  # -1


    time0 = db.Column(db.DateTime(), default=datetime.utcnow)
    user0_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time1 = db.Column(db.DateTime())
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time2 = db.Column(db.DateTime())
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time3 = db.Column(db.DateTime())
    user3_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time4 = db.Column(db.DateTime())
    user4_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time5 = db.Column(db.DateTime())
    user5_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time6 = db.Column(db.DateTime())
    user6_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time7 = db.Column(db.DateTime())
    user7_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time8 = db.Column(db.DateTime())
    user8_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time9 = db.Column(db.DateTime())
    user9_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # duizhang =db.Column(db.String(64))

    azd_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dingdan_azd = db.relationship("User", foreign_keys=[azd_id])

    def __repr__(self):
        return '<Dingdan %r>' % self.id
