# _*_ encoding: utf-8 _*_

import hashlib
import os
import time
from datetime import datetime, timedelta

from flask import redirect, url_for, render_template, flash, make_response, send_file, session, request
from flask_login import current_user, login_required
from sqlalchemy import func, engine, or_, and_

from app.models import User, Kehu, Dingdan, Chanpin, Xiaoqu  # , Gongren
from .. import db, moment
from .forms import NameForm, KehuForm, WilladdcpForm, YxwForm, SmForm, LyjForm, ScForm, ZwsForm, ChForm, FindkhForm, \
    KFfindForm, FineddidForm, LygForm, FinefhddidForm, FineshddidForm, FinepgddidForm, FineqkddidForm, YtcForm, JxForm, \
    stoplcddidForm, azstopddidForm, BlForm, SgdtjForm, DdzttjForm
from . import main

import tablib


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # form = NameForm()
    # bujuan=None
    kehus = Kehu.query.filter_by(user=current_user._get_current_object()).order_by(
        Kehu.id)  # .order_by(Guke.outtime.desc())

    # 管理账号转到管理页
    if current_user.role == 'adm':
        return redirect(url_for('admin.index'))

    # pass
    elif current_user.role == '客服':
        # 一般用户转转到首页..
        return redirect(url_for('main.kefucxlist'))  # request.args.get('next') or

    # pass
    elif current_user.role == '业务员':
        # 一般用户转转到首页..
        return redirect(url_for('main.kehulist'))

    elif current_user.role == '订货员':
        # 一般用户转转到首页..
        return redirect(url_for('main.dinghuolist'))

    elif current_user.role == '入库员':
        # 一般用户转转到首页..
        return redirect(url_for('main.rukulist'))

    elif current_user.role == '发货员':
        # 一般用户转转到首页..
        return redirect(url_for('main.fahuolist'))


    elif current_user.role == '收货员':
        # 一般用户转转到首页..
        return redirect(url_for('main.shouhuolist'))

    elif current_user.role == '派工员':
        # 一般用户转转到首页..
        return redirect(url_for('main.paigonglist'))


    elif current_user.role == '清款员':
        # 一般用户转转到首页..
        return redirect(url_for('main.qingkuanlist'))

    elif current_user.role == '统计员':
        # 一般用户转转到首页..
        return redirect(url_for('main.tongjilist'))



    elif current_user.role == '安装队':
        # 一般用户转转到首页..
        return redirect(url_for('main.azdwillget'))

    # elif current_user.role == '统计员':
    #     # 一般用户转转到首页..
    #     return redirect(url_for('main.tongjilist'))

    else:
        # 一般用户转转到首页..
        # return redirect(request.args.get('next') or url_for('main.kehulist'))
        pass

    # user = current_user._get_current_object()
    # if form.validate_on_submit():
    #     xiangmu = Xiangmu.query.get(form.xiangmu.data)
    #
    #     bujuan = Bujuan(user=user, xiangmu=xiangmu, jine=form.jine.data)
    #     db.session.add(bujuan)
    #     flash('已成功下单')
    #     return redirect(url_for('.index'))
    #
    # # 管理账号转到管理页
    # if user.isadm:
    #     return redirect(url_for('main.count'))
    # else:
    #     # 一般用户转转到首页..
    #     return render_template('index.html', form=form, bujuans=bujuans)


@main.route('/kehulist', methods=['GET', 'POST'])
@login_required
def kehulist():
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = FindkhForm()
    # bujuan=None

    user = current_user._get_current_object()
    if form.validate_on_submit():
        session['infostring'] = form.infostring.data
        session['status'] = form.status.data
        return redirect(url_for('main.kehulist'))

    # form.infosing.data = '％'
    if session.get('infostring') != None:
        infostring = '%' + session.get('infostring') + '%'
    else:
        infostring = '%'

    prewhere = session.get('infostring')

    status = session.get('status', 0)

    kehus = Kehu.query.filter(Kehu.user == current_user._get_current_object()).filter(
        or_(Kehu.fangjian.like(infostring), Kehu.chenghu.like(infostring),
            Kehu.tel.like(infostring))).order_by(Kehu.id.desc())  # .order_by(Guke.outtime.desc())

    # kehus = Kehu.query.filter_by(user=current_user._get_current_object(),).order_by(
    #     Kehu.id.desc())  # .order_by(Guke.outtime.desc())
    form.infostring.data = session.get('infostring', '')
    form.status.data = status

    return render_template('kehulist.html', kehus=kehus, form=form, prewhere=prewhere, status=status)  # ,


@main.route('/dinghuolist', methods=['GET', 'POST'])
@login_required
def dinghuolist():
    if current_user.role != '订货员':
        return redirect(url_for('main.index'))

    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())

    dingdans = Dingdan.query.filter_by(status=2).order_by(Dingdan.chanpin_id,
                                                          Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    return render_template('dinghuolist.html', dingdans=dingdans, done='待订货')  # form=form,


@main.route('/rukulist', methods=['GET', 'POST'])
@login_required
def rukulist():
    if current_user.role != '入库员':
        return redirect(url_for('main.index'))

    form = FineddidForm()

    if form.validate_on_submit():
        session['ddid'] = form.ddid.data
        session['status'] = form.status.data
        return redirect(url_for('main.rukulist'))

    ddid = session.get('ddid', '')
    status = session.get('status', 0)
    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())
    if status == 0:
        if ddid != '':
            form.ddid.data = ddid
            form.status.data = status

            dingdans = Dingdan.query.filter(or_(Dingdan.status == 3, Dingdan.status == 4)).filter_by(id=ddid).order_by(
                Dingdan.chanpin_id,
                Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
        else:
            form.ddid.data = ddid
            form.status.data = status
            ddid = 0

            dingdans = Dingdan.query.filter(or_(Dingdan.status == 3, Dingdan.status == 4)).order_by(Dingdan.chanpin_id,
                                                                                                    Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    else:
        if ddid != '':
            form.ddid.data = ddid
            form.status.data = status
            dingdans = Dingdan.query.filter_by(status=status).filter_by(id=ddid).order_by(
                Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
        else:
            form.ddid.data = ddid
            form.status.data = status
            ddid = 0

            dingdans = Dingdan.query.filter_by(status=status).order_by(Dingdan.chanpin_id,
                                                                       Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    return render_template('rukulist.html', form=form, dingdans=dingdans, done='待入库', ddid=ddid, status=status)  #


@main.route('/shouhuolist', methods=['GET', 'POST'])
@login_required
def shouhuolist():
    if current_user.role != '收货员':
        return redirect(url_for('main.index'))

    form = FineshddidForm()

    if form.validate_on_submit():
        session['xiaoqu'] = form.xiaoqu.data
        session['fangjian'] = form.fangjian.data
        session['chenghu'] = form.chenghu.data
        session['chanpin'] = form.chanpin.data
        session['status'] = form.status.data
        return redirect(url_for('main.shouhuolist'))

    xiaoquid = int(session.get('xiaoqu', 0))
    fangjian = session.get('fangjian', '')
    chenghu = session.get('chenghu', '')
    chanpin = int(session.get('chanpin', 0))
    status = int(session.get('status', 0))

    form.xiaoqu.data = xiaoquid
    form.fangjian.data = fangjian
    form.chenghu.data = chenghu
    form.chanpin.data = chanpin
    form.status.data = status

    # prewhere = '小区：' + str(xiaoquid) + '房间：' + fangjian + '电话.：' + tel + '状态：' + str(status)  #

    # dingdans = Dingdan.query.filter_by(status=2).order_by(Dingdan.chanpin_id,
    #                                                       Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    # xiaoquO = Xiaoqu.query.get(xiaoquid)
    #
    # kehus = Kehu.query.filter(and_(Kehu.fangjian.like(fangjian), Kehu.tel.like(tel)))

    # dingdans = Dingdan.query.filter(Dingdan.status == status)

    # 有大问题！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # Kehu.fangjian.like(fangjian), Kehu.tel.like(tel)
    # 只要纪录集合中有一个符合即整个集合算是了
    # 与Dingdan.status不同

    xiaoqus = Xiaoqu.query.all()

    fangjian = '%' + fangjian + '%'
    chenghu = '%' + chenghu + '%'

    if status == 0:
        if xiaoquid == 0:
            kehus = Kehu.query.filter(and_(Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))
        else:
            kehus = Kehu.query.filter(
                and_(Kehu.xiaoqu_id == xiaoquid, Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))
    else:
        if xiaoquid == 0:
            kehus = Kehu.query.filter(and_(Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))
        else:
            kehus = Kehu.query.filter(
                and_(Kehu.xiaoqu_id == xiaoquid, Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))

    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())

    # if status == 0:
    #     if ddid != '':
    #         form.ddid.data = ddid
    #         form.status.data = status
    #
    #         dingdans = Dingdan.query.filter(or_(Dingdan.status == 3, Dingdan.status == 6)).filter_by(id=ddid).order_by(
    #             Dingdan.chanpin_id,
    #             Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     else:
    #         form.ddid.data = ddid
    #         form.status.data = status
    #         ddid = 0
    #
    #         dingdans = Dingdan.query.filter(or_(Dingdan.status == 3, Dingdan.status == 6)).order_by(Dingdan.chanpin_id,
    #                                                                                                 Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    # else:
    #     if ddid != '':
    #         form.ddid.data = ddid
    #         form.status.data = status
    #         dingdans = Dingdan.query.filter_by(status=status).filter_by(id=ddid).order_by(
    #             Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     else:
    #         form.ddid.data = ddid
    #         form.status.data = status
    #         ddid = 0
    #
    #         dingdans = Dingdan.query.filter_by(status=status).order_by(Dingdan.chanpin_id,
    #                                                                    Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    # return render_template('shouhuolist.html', form=form, dingdans=dingdans, done='待收货', ddid=ddid, status=status)  #
    return render_template('shouhuolist.html', form=form, xiaoqus=xiaoqus, xiaoquid=xiaoquid,
                           fangjian=fangjian, chenghu=chenghu, status=status, chanpin=chanpin,
                           kehus=kehus)  # prewhere=prewhere,, dingdans=dingdans


@main.route('/fahuolist', methods=['GET', 'POST'])
@login_required
def fahuolist():
    if current_user.role != '发货员':
        return redirect(url_for('main.index'))

    form = FinefhddidForm()

    if form.validate_on_submit():
        session['ddid'] = form.ddid.data
        session['status'] = form.status.data
        return redirect(url_for('main.fahuolist'))

    ddid = session.get('ddid', '')
    status = session.get('status', 0)
    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())

    form.ddid.data = ddid
    form.status.data = status

    if status == 0:
        if ddid != '':
            dingdans = Dingdan.query.filter(or_(Dingdan.status == 4, Dingdan.status == 5)).filter_by(id=ddid).order_by(
                Dingdan.chanpin_id,
                Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
        else:
            ddid = 0

            dingdans = Dingdan.query.filter(or_(Dingdan.status == 4, Dingdan.status == 5)).order_by(Dingdan.chanpin_id,
                                                                                                    Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    else:
        if ddid != '':
            dingdans = Dingdan.query.filter_by(status=status).filter_by(id=ddid).order_by(
                Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
        else:
            ddid = 0

            dingdans = Dingdan.query.filter_by(status=status).order_by(Dingdan.chanpin_id,
                                                                       Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    kehus = Kehu.query.all()

    return render_template('fahuolist.html', form=form, dingdans=dingdans, kehus=kehus, done='待发货', ddid=ddid,
                           status=status)  #


@main.route('/paigonglist', methods=['GET', 'POST'])
@login_required
def paigonglist():
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))

    form = FinepgddidForm()

    if form.validate_on_submit():
        # session['ddid'] = form.ddid.data
        session['xiaoqu'] = form.xiaoqu.data
        session['fangjian'] = form.fangjian.data
        # session['chenghu'] = form.chenghu.data
        session['status'] = form.status.data
        return redirect(url_for('main.paigonglist'))

    # ddid = session.get('ddid', '')
    # status = session.get('status', 0)

    xiaoquid = int(session.get('xiaoqu', 0))
    fangjian = session.get('fangjian', '')
    # chenghu = session.get('chenghu', '')
    status = int(session.get('status', 0))

    form.xiaoqu.data = xiaoquid
    form.fangjian.data = fangjian
    # form.chenghu.data = chenghu
    form.status.data = status

    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())

    # form.ddid.data = ddid
    # form.status.data = status

    # if status == 0:
    #     if ddid != '':
    #         dingdans = Dingdan.query.filter(
    #             or_(Dingdan.status == 6, Dingdan.status == 7, Dingdan.status == 8)).filter_by(id=ddid).order_by(
    #             Dingdan.chanpin_id,
    #             Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     else:
    #         ddid = 0
    #
    #         dingdans = Dingdan.query.filter(
    #             or_(Dingdan.status == 6, Dingdan.status == 7, Dingdan.status == 8)).order_by(Dingdan.chanpin_id,
    #                                                                                          Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    # else:
    #     if ddid != '':
    #         dingdans = Dingdan.query.filter_by(status=status).filter_by(id=ddid).order_by(
    #             Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     else:
    #         ddid = 0
    #
    #         dingdans = Dingdan.query.filter_by(status=status).order_by(Dingdan.chanpin_id,
    #                                                                    Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    fangjian = '%' + fangjian + '%'
    # chenghu = '%' + chenghu + '%'

    # if status == 0:
    #     if xiaoquid == 0:
    #         kehus = Kehu.query.filter(and_(Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))
    #     else:
    #         kehus = Kehu.query.filter(
    #             and_(Kehu.xiaoqu_id == xiaoquid, Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))
    # else:
    #     if xiaoquid == 0:
    #         kehus = Kehu.query.filter(and_(Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))
    #     else:
    #         kehus = Kehu.query.filter(
    #             and_(Kehu.xiaoqu_id == xiaoquid, Kehu.fangjian.like(fangjian), Kehu.chenghu.like(chenghu)))

    if status == 0:
        if xiaoquid == 0:
            kehus = Kehu.query.filter(Kehu.fangjian.like(fangjian))
        else:
            kehus = Kehu.query.filter(and_(Kehu.xiaoqu_id == xiaoquid, Kehu.fangjian.like(fangjian)))
    else:
        if xiaoquid == 0:
            kehus = Kehu.query.filter(Kehu.fangjian.like(fangjian))
        else:
            kehus = Kehu.query.filter(and_(Kehu.xiaoqu_id == xiaoquid, Kehu.fangjian.like(fangjian)))

    # kehus = Kehu.query.all()
    xiaoqus = Xiaoqu.query.all()

    # gongrens = Gongren.query.all()

    gongrens = User.query.filter_by(role=u'安装队')

    # return render_template('paigonglist.html', form=form, dingdans=dingdans, kehus=kehus, done='待发货', ddid=ddid,
    #                        status=status)  #

    return render_template('paigonglist.html', gongrens=gongrens, form=form, xiaoqus=xiaoqus, xiaoquid=xiaoquid,
                           fangjian=fangjian, status=status, kehus=kehus)  # prewhere=prewhere,, dingdans=dingdans


@main.route('/qingkuanlist', methods=['GET', 'POST'])
@login_required
def qingkuanlist():
    if current_user.role != '清款员':
        return redirect(url_for('main.index'))

    form = FineqkddidForm()

    if form.validate_on_submit():
        session['ddid'] = form.ddid.data
        session['status'] = form.status.data
        return redirect(url_for('main.qingkuanlist'))

    ddid = session.get('ddid', '')
    status = session.get('status', 0)
    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())

    form.ddid.data = ddid
    form.status.data = status

    if status == 0:
        if ddid != '':
            dingdans = Dingdan.query.filter(or_(Dingdan.status == 8, Dingdan.status == 9)).filter_by(id=ddid).order_by(
                Dingdan.chanpin_id,
                Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
        else:
            ddid = 0

            dingdans = Dingdan.query.filter(or_(Dingdan.status == 8, Dingdan.status == 9)).order_by(Dingdan.chanpin_id,
                                                                                                    Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    else:
        if ddid != '':
            dingdans = Dingdan.query.filter_by(status=status).filter_by(id=ddid).order_by(
                Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
        else:
            ddid = 0

            dingdans = Dingdan.query.filter_by(status=status).order_by(Dingdan.chanpin_id,
                                                                       Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    kehus = Kehu.query.all()

    return render_template('qingkuanlist.html', form=form, dingdans=dingdans, kehus=kehus, done='待发货', ddid=ddid,
                           status=status)  #


@main.route('/tongjilist', methods=['GET', 'POST'])
@login_required
def tongjilist():
    if current_user.role != '统计员':
        return redirect(url_for('main.index'))

    form = SgdtjForm()

    if form.validate_on_submit():
        session['sgdid'] = form.sgdid.data
        session['dayB'] = form.dayB.data.strftime('%Y-%m-%d')
        session['dayE'] = form.dayE.data.strftime('%Y-%m-%d')
        session['status'] = form.status.data
        return redirect(url_for('main.tongjilist'))

    sgdid = session.get('sgdid', 0)
    dayB = session.get('dayB', datetime.utcnow().strftime('%Y-%m-%d'))
    dayE = session.get('dayE', datetime.utcnow().strftime('%Y-%m-%d'))
    status = session.get('status', 8)

    # dayB = datetime.utcnow().strftime('%Y-%m-%d')
    # dayE = datetime.utcnow().strftime('%Y-%m-%d')

    # # 下单时间超过6小时的才在此显示
    # # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
    #
    # # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
    #
    # # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
    #
    # # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
    #
    # # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())
    #

    # dingdans = Dingdan.query.filter(Dingdan.status == 8).filter_by(azd_id=sgdid,status=status).order_by(Dingdan.time8)

    if sgdid == 0:
        if status == 8:
            dingdans = Dingdan.query.filter(
                and_(or_(Dingdan.status == 8, Dingdan.status == 9), Dingdan.time8 >= dayB,
                     Dingdan.time8 <= dayE)).order_by(
                Dingdan.azd_id, Dingdan.kehu_id)
        else:
            dingdans = Dingdan.query.filter(
                and_(Dingdan.status == status, Dingdan.time8 >= dayB, Dingdan.time8 <= dayE)).order_by(Dingdan.azd_id,
                                                                                                       Dingdan.kehu_id)
    else:  # azd_id
        if status == 8:
            dingdans = Dingdan.query.filter(
                and_(or_(Dingdan.status == 8, Dingdan.status == 9), Dingdan.azd_id == sgdid, Dingdan.time8 >= dayB,
                     Dingdan.time8 <= dayE)).order_by(
                Dingdan.azd_id, Dingdan.kehu_id)
        else:
            dingdans = Dingdan.query.filter(
                and_(Dingdan.status == status, Dingdan.azd_id == sgdid, Dingdan.time8 >= dayB,
                     Dingdan.time8 <= dayE)).order_by(Dingdan.azd_id,
                                                      Dingdan.kehu_id)

    form.sgdid.data = sgdid

    form.dayB.data = datetime.strptime(dayB, '%Y-%m-%d')  # datetime.utcnow() # dayB.strftime('%Y-%m-%d')
    form.dayE.data = datetime.strptime(dayE, '%Y-%m-%d')  # dayE.strftime('%Y-%m-%d')

    form.status.data = status
    #
    # if status == 0:
    #     if ddid != '':
    #         dingdans = Dingdan.query.filter(or_(Dingdan.status == 8, Dingdan.status == 9)).filter_by(id=ddid).order_by(
    #             Dingdan.chanpin_id,
    #             Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     else:
    #         ddid = 0
    #
    #         dingdans = Dingdan.query.filter(or_(Dingdan.status == 8, Dingdan.status == 9)).order_by(Dingdan.chanpin_id,
    #                                                                                                 Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    # else:
    #     if ddid != '':
    #         dingdans = Dingdan.query.filter_by(status=status).filter_by(id=ddid).order_by(
    #             Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     else:
    #         ddid = 0
    #
    #         dingdans = Dingdan.query.filter_by(status=status).order_by(Dingdan.chanpin_id,
    #                                                                    Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #
    # dayB = datetime.utcnow()

    if sgdid == 0:
        users = User.query.filter_by(role=u'安装队').all()
    else:
        users = User.query.filter_by(id=sgdid).all()
    # return render_template('tongjilist.html', form=form, dingdans=dingdans, kehus=kehus, done='待发货', ddid=ddid,
    #                        status=status)  #
    #
    return render_template('tongjilist.html', form=form, dingdans=dingdans, status=status, users=users, dayB=dayB,
                           dayE=dayE)


@main.route('/outaztoxls/<int:status>', methods=['GET', 'POST'])
@login_required
def outaztoxls(status):
    if current_user.role != '统计员':
        return redirect(url_for('main.index'))

    sgdid = session.get('sgdid', 0)
    dayB = session.get('dayB', datetime.utcnow().strftime('%Y-%m-%d'))
    dayE = session.get('dayE', datetime.utcnow().strftime('%Y-%m-%d'))
    status = session.get('status', 8)

    #
    # if status == 8:
    #     dingdans = Dingdan.query.filter(
    #         and_(or_(Dingdan.status == 8, Dingdan.status == 9), Dingdan.time8 >= dayB, Dingdan.time8 <= dayE)).order_by(
    #         Dingdan.azd_id, Dingdan.time8)
    # else:
    #     dingdans = Dingdan.query.filter(
    #         and_(Dingdan.status == status, Dingdan.time8 >= dayB, Dingdan.time8 <= dayE)).order_by(Dingdan.azd_id,
    #                                                                                                Dingdan.time8)

    if sgdid == 0:
        if status == 8:
            dingdans = Dingdan.query.filter(
                and_(or_(Dingdan.status == 8, Dingdan.status == 9), Dingdan.time8 >= dayB,
                     Dingdan.time8 <= dayE)).order_by(
                Dingdan.azd_id, Dingdan.kehu_id)
        else:
            dingdans = Dingdan.query.filter(
                and_(Dingdan.status == status, Dingdan.time8 >= dayB, Dingdan.time8 <= dayE)).order_by(Dingdan.azd_id,
                                                                                                       Dingdan.kehu_id)
    else:  # azd_id
        if status == 8:
            dingdans = Dingdan.query.filter(
                and_(or_(Dingdan.status == 8, Dingdan.status == 9), Dingdan.azd_id == sgdid, Dingdan.time8 >= dayB,
                     Dingdan.time8 <= dayE)).order_by(
                Dingdan.azd_id, Dingdan.kehu_id)
        else:
            dingdans = Dingdan.query.filter(
                and_(Dingdan.status == status, Dingdan.azd_id == sgdid, Dingdan.time8 >= dayB,
                     Dingdan.time8 <= dayE)).order_by(Dingdan.azd_id,
                                                      Dingdan.kehu_id)

    users = User.query.filter_by(role=u'安装队').all()

    headers = (u"No", u"安装队", u"小区", u"房间", u"产品", u"型号", u"数量", u"单位", u"时间", u"状态")

    info = []
    data = tablib.Dataset(*info, headers=headers)  # headers 数量要与 data 致

    i = 0
    for dingdan in dingdans:

        i += 1
        azdname = ''
        for user in users:
            if user.id == dingdan.azd_id:
                azdname = user.username

        shuliang = 0
        dw = ''
        if dingdan.chanpin.pinming == '阳台窗' or dingdan.chanpin.pinming == '隐形网':
            shuliang = format(float(dingdan.kuan_chang) * float(dingdan.gao) / 1000 / 1000, '.2f')
            dw = u'平方'
        elif dingdan.chanpin.pinming == '纱门':
            shuliang = format(float(dingdan.meikongkuan_bashoudigao) * float(dingdan.gao) / 1000 / 1000, '.2f')
            dw = u'平方'
        else:
            shuliang = dingdan.shuliang
            dw = u'个'

        statusP = ''
        timeF = dingdan.time8.strftime('%Y-%m-%d')
        if dingdan.status == 8:
            statusP = u'(装完)'
            timeF = dingdan.time8.strftime('%Y-%m-%d')
        elif dingdan.status == 9:
            statusP = u'(装完-清款)'
            timeF = dingdan.time8.strftime('%Y-%m-%d')
        elif dingdan.status == 7:
            statusP = u'(未完工)'
            timeF = dingdan.time8.strftime('%Y-%m-%d')
        elif dingdan.status == -1:
            statusP = u'【终止】'
            timeF = dingdan.time8.strftime('%Y-%m-%d')

        data.append(
            [i, azdname, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian, dingdan.chanpin.pinming, dingdan.xinghao,
             shuliang, dw, timeF, statusP])

    t = time.time()
    nowTime = lambda: int(round(t * 1000))
    tmpstr = current_user.username + str(nowTime())
    md5filename = hashlib.md5()
    md5filename.update(tmpstr.encode('utf-8'))
    filenamehead = md5filename.hexdigest()[:15]

    # 导出excel表
    open('app/cxls/xxxaz.xls', 'wb').write(data.xls)

    response = make_response(send_file("cxls/xxxaz.xls"))
    response.headers["Content-Disposition"] = "attachment; filename=" + 'azd' + ".xls;"
    return response

    # return redirect(url_for('main.showkehudd', id=1))


@main.route('/tongjilistq', methods=['GET', 'POST'])
@login_required
def tongjilistq():
    if current_user.role != '统计员':
        return redirect(url_for('main.index'))

    form = DdzttjForm()

    if form.validate_on_submit():
        session['dayB'] = form.dayB.data.strftime('%Y-%m-%d')
        session['dayE'] = form.dayE.data.strftime('%Y-%m-%d')
        session['status'] = form.status.data
        session['ywyid'] = form.ywyid.data

        session['xiaoquid'] = form.xiaoquid.data

        return redirect(url_for('main.tongjilistq'))

    # sgdid = session.get('sgdid', '')
    dayB = session.get('dayB', datetime.utcnow().strftime('%Y-%m-%d'))
    dayE = session.get('dayE', datetime.utcnow().strftime('%Y-%m-%d'))
    status = session.get('status', 8)
    ywyid = session.get('ywyid', 0)

    xiaoquid = session.get('xiaoquid', 0)

    # if status == 8:
    #     dingdans = Dingdan.query.filter(
    #         and_(or_(Dingdan.status == 8, Dingdan.status == 9), Dingdan.time8 >= dayB, Dingdan.time8 <= dayE)).order_by(
    #         Dingdan.azd_id,
    #         Dingdan.kehu_id)
    # else:

    dingdans = Dingdan.query.filter_by(id=-1).all()

    if status == 1:
        # 量尺
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time1 >= dayB, Dingdan.time1 <= dayE)).order_by(Dingdan.kehu_id)
    elif status == 2:
        # 量尺
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time2 >= dayB, Dingdan.time2 <= dayE)).order_by(Dingdan.kehu_id)
    elif status == 3:
        # 量尺
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time3 >= dayB, Dingdan.time3 <= dayE)).order_by(Dingdan.kehu_id)
    elif status == 6:
        # 量尺
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time6 >= dayB, Dingdan.time6 <= dayE)).order_by(Dingdan.kehu_id)
    elif status == 7:
        # 量尺
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time7 >= dayB, Dingdan.time7 <= dayE)).order_by(Dingdan.kehu_id)
    elif status == 8:
        # 完成
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time8 >= dayB, Dingdan.time8 <= dayE)).order_by(Dingdan.kehu_id)
    elif status == 9:
        # 量尺
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time9 >= dayB, Dingdan.time9 <= dayE)).order_by(Dingdan.kehu_id)
    elif status == -1:
        # 量尺
        dingdans = Dingdan.query.filter(
            and_(Dingdan.status == status, Dingdan.time_1 >= dayB, Dingdan.time_1 <= dayE)).order_by(Dingdan.kehu_id)

    # form.sgdid.data = sgdid

    form.dayB.data = datetime.strptime(dayB, '%Y-%m-%d')  # datetime.utcnow() # dayB.strftime('%Y-%m-%d')
    form.dayE.data = datetime.strptime(dayE, '%Y-%m-%d')  # dayE.strftime('%Y-%m-%d')

    form.status.data = status
    form.ywyid.data = ywyid

    form.xiaoquid.data = xiaoquid

    if xiaoquid == 0:  # 所有小区
        if ywyid == 0:
            kehus = Kehu.query.all()
        else:
            kehus = Kehu.query.filter_by(user_id=ywyid).all()
    else:
        if ywyid == 0:
            kehus = Kehu.query.filter_by(xiaoqu_id=xiaoquid).all()
        else:
            kehus = Kehu.query.filter_by(xiaoqu_id=xiaoquid).filter_by(user_id=ywyid).all()

    return render_template('tongjilistq.html', form=form, dingdans=dingdans, status=status, kehus=kehus, dayB=dayB,
                           dayE=dayE, ywyid=ywyid, xiaoquid=xiaoquid)


@main.route('/tongjilistc', methods=['GET', 'POST'])
@login_required
def tongjilistc():
    return render_template(
        'tongjilistc.html')  # , form=form, dingdans=dingdans, status=status, users=users, dayB=dayB, dayE=dayE)

#
# @main.route('/anzhuanglist', methods=['GET', 'POST'])
# @login_required
# def anzhuanglist():
#     if current_user.role != '安装队':
#         return redirect(url_for('main.index'))
#     #
#     # form = FindkhForm()
#     # # bujuan=None
#     #
#     # user = current_user._get_current_object()
#     # if form.validate_on_submit():
#     #     session['infostring'] = form.infostring.data
#     #     session['status'] = form.status.data
#     #     return redirect(url_for('main.kehulist'))
#     #
#     # # form.infosing.data = '％'
#     # if session.get('infostring') != None:
#     #     infostring = '%' + session.get('infostring') + '%'
#     # else:
#     #     infostring = '%'
#     #
#     # prewhere = session.get('infostring')
#     #
#     # status = session.get('status', 0)
#     #
#     # kehus = Kehu.query.filter(Kehu.user == current_user._get_current_object()).filter(
#     #     or_(Kehu.fangjian.like(infostring), Kehu.chenghu.like(infostring),
#     #         Kehu.tel.like(infostring))).order_by(Kehu.id.desc())  # .order_by(Guke.outtime.desc())
#     #
#     # form.infostring.data = session.get('infostring', '')
#     # form.status.data = status
#     #
#     # return render_template('kehulist.html', kehus=kehus, form=form, prewhere=prewhere, status=status)  # ,
#
#     dingdans = Dingdan.query.filter(Dingdan.dingdan_azd == current_user._get_current_object()).order_by(
#         Dingdan.id.desc())  # .order_by(Guke.outtime.desc())
#
#     kehus = Kehu.query.all()
#
#     azdobj = current_user._get_current_object()
#
#     # form.infostring.data = session.get('infostring', '')
#     # form.status.data = status
#
#     return render_template('anzhuanglist.html', dingdans=dingdans, kehus=kehus,
#                            azdobj=azdobj)  # ,, form=form, prewhere=prewhere, status=status


@main.route('/azdwillget', methods=['GET', 'POST'])
@login_required
def azdwillget():
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))

    azdobj = current_user._get_current_object()

    dingdans = Dingdan.query.filter(Dingdan.dingdan_azd == azdobj).order_by(
        Dingdan.id.desc())  # .order_by(Guke.outtime.desc())

    kehus = Kehu.query.all()


    return render_template('azdwillget.html', dingdans=dingdans, kehus=kehus,
                           azdobj=azdobj)  # ,, form=form, prewhere=prewhere, status=status


@main.route('/azddoing', methods=['GET', 'POST'])
@login_required
def azddoing():
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))
    #
    # form = FindkhForm()
    # # bujuan=None
    #
    # user = current_user._get_current_object()
    # if form.validate_on_submit():
    #     session['infostring'] = form.infostring.data
    #     session['status'] = form.status.data
    #     return redirect(url_for('main.kehulist'))
    #
    # # form.infosing.data = '％'
    # if session.get('infostring') != None:
    #     infostring = '%' + session.get('infostring') + '%'
    # else:
    #     infostring = '%'
    #
    # prewhere = session.get('infostring')
    #
    # status = session.get('status', 0)
    #
    # kehus = Kehu.query.filter(Kehu.user == current_user._get_current_object()).filter(
    #     or_(Kehu.fangjian.like(infostring), Kehu.chenghu.like(infostring),
    #         Kehu.tel.like(infostring))).order_by(Kehu.id.desc())  # .order_by(Guke.outtime.desc())
    #
    # form.infostring.data = session.get('infostring', '')
    # form.status.data = status
    #
    # return render_template('kehulist.html', kehus=kehus, form=form, prewhere=prewhere, status=status)  # ,

    azdobj = current_user._get_current_object()

    dingdans = Dingdan.query.filter(Dingdan.dingdan_azd == azdobj).order_by(
        Dingdan.id.desc())  # .order_by(Guke.outtime.desc())

    kehus = Kehu.query.all()



    # form.infostring.data = session.get('infostring', '')
    # form.status.data = status

    return render_template('azddoing.html', dingdans=dingdans, kehus=kehus,
                           azdobj=azdobj)  # ,, form=form, prewhere=prewhere, status=status


@main.route('/azdfinished', methods=['GET', 'POST'])
@login_required
def azdfinished():
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))
    #
    # form = FindkhForm()
    # # bujuan=None
    #
    # user = current_user._get_current_object()
    # if form.validate_on_submit():
    #     session['infostring'] = form.infostring.data
    #     session['status'] = form.status.data
    #     return redirect(url_for('main.kehulist'))
    #
    # # form.infosing.data = '％'
    # if session.get('infostring') != None:
    #     infostring = '%' + session.get('infostring') + '%'
    # else:
    #     infostring = '%'
    #
    # prewhere = session.get('infostring')
    #
    # status = session.get('status', 0)
    #
    # kehus = Kehu.query.filter(Kehu.user == current_user._get_current_object()).filter(
    #     or_(Kehu.fangjian.like(infostring), Kehu.chenghu.like(infostring),
    #         Kehu.tel.like(infostring))).order_by(Kehu.id.desc())  # .order_by(Guke.outtime.desc())
    #
    # form.infostring.data = session.get('infostring', '')
    # form.status.data = status
    #
    # return render_template('kehulist.html', kehus=kehus, form=form, prewhere=prewhere, status=status)  # ,

    azdobj = current_user._get_current_object()

    dingdans = Dingdan.query.filter(Dingdan.dingdan_azd == azdobj).order_by(
        Dingdan.id.desc())  # .order_by(Guke.outtime.desc())

    kehus = Kehu.query.all()



    # form.infostring.data = session.get('infostring', '')
    # form.status.data = status

    return render_template('azdfinished.html', dingdans=dingdans, kehus=kehus,
                           azdobj=azdobj)  # ,, form=form, prewhere=prewhere, status=status



@main.route('/azdstoped', methods=['GET', 'POST'])
@login_required
def azdstoped ():
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))
    #
    # form = FindkhForm()
    # # bujuan=None
    #
    # user = current_user._get_current_object()
    # if form.validate_on_submit():
    #     session['infostring'] = form.infostring.data
    #     session['status'] = form.status.data
    #     return redirect(url_for('main.kehulist'))
    #
    # # form.infosing.data = '％'
    # if session.get('infostring') != None:
    #     infostring = '%' + session.get('infostring') + '%'
    # else:
    #     infostring = '%'
    #
    # prewhere = session.get('infostring')
    #
    # status = session.get('status', 0)
    #
    # kehus = Kehu.query.filter(Kehu.user == current_user._get_current_object()).filter(
    #     or_(Kehu.fangjian.like(infostring), Kehu.chenghu.like(infostring),
    #         Kehu.tel.like(infostring))).order_by(Kehu.id.desc())  # .order_by(Guke.outtime.desc())
    #
    # form.infostring.data = session.get('infostring', '')
    # form.status.data = status
    #
    # return render_template('kehulist.html', kehus=kehus, form=form, prewhere=prewhere, status=status)  # ,

    azdobj = current_user._get_current_object()

    dingdans = Dingdan.query.filter(Dingdan.dingdan_azd == azdobj).order_by(
        Dingdan.id.desc())  # .order_by(Guke.outtime.desc())

    kehus = Kehu.query.all()



    # form.infostring.data = session.get('infostring', '')
    # form.status.data = status

    return render_template('azdstoped.html', dingdans=dingdans, kehus=kehus,
                           azdobj=azdobj)  # ,, form=form, prewhere=prewhere, status=status





@main.route('/kefucxlist', methods=['GET', 'POST'])
@login_required
def kefucxlist():
    if current_user.role != '客服':
        return redirect(url_for('main.index'))

    form = KFfindForm()

    if form.validate_on_submit():
        session['xiaoqu'] = form.xiaoqu.data
        session['fangjian'] = form.fangjian.data
        session['tel'] = form.tel.data
        session['status'] = form.status.data
        return redirect(url_for('main.kefucxlist'))

    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())

    # xiaoquid = int(session.get('xiaoqu', 0))
    # fangjian = '%' + session.get('fangjian', '%') + '%'
    # tel = '%' + session.get('tel', '%') + '%'
    # status = int(session.get('status', 0))

    xiaoquid = int(session.get('xiaoqu', 0))
    fangjian = session.get('fangjian', '')
    tel = session.get('tel', '')
    status = int(session.get('status', 0))

    form.xiaoqu.data = xiaoquid
    form.fangjian.data = fangjian
    form.tel.data = tel
    form.status.data = status

    # prewhere = '小区：' + str(xiaoquid) + '房间：' + fangjian + '电话.：' + tel + '状态：' + str(status)  #

    # dingdans = Dingdan.query.filter_by(status=2).order_by(Dingdan.chanpin_id,
    #                                                       Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    # xiaoquO = Xiaoqu.query.get(xiaoquid)
    #
    # kehus = Kehu.query.filter(and_(Kehu.fangjian.like(fangjian), Kehu.tel.like(tel)))

    # dingdans = Dingdan.query.filter(Dingdan.status == status)

    # 有大问题！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # Kehu.fangjian.like(fangjian), Kehu.tel.like(tel)
    # 只要纪录集合中有一个符合即整个集合算是了
    # 与Dingdan.status不同

    xiaoqus = Xiaoqu.query.all()

    # if prewhere =='房间：%%电话.：%%状态：0' : #小区：0
    #     dingdans = Dingdan.query.filter(Kehu.tel.like('9999999999'))
    # else:
    #     # if xiaoquid != 0:
    #     #     if status != 0:
    #     #         dingdans = Dingdan.query.filter(
    #     #             and_(Kehu.fangjian.like(fangjian), Kehu.tel.like(tel), Kehu.xiaoqu_id == xiaoquid,
    #     #                  Dingdan.status == status)).order_by(Dingdan.chanpin_id,
    #     #                                                      Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     #     else:
    #     #         dingdans = Dingdan.query.filter(
    #     #             and_(Kehu.fangjian.like(fangjian), Kehu.tel.like(tel), Kehu.xiaoqu_id == xiaoquid)).order_by(
    #     #             Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     # else:
    #     if status != 0:
    #         dingdans = Dingdan.query.filter(
    #             and_(Kehu.fangjian.like(fangjian), Kehu.tel.like(tel), Dingdan.status == status)).order_by(
    #             Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
    #     else:
    #         dingdans = Dingdan.query.filter(
    #             and_(Kehu.fangjian.like(fangjian), Kehu.tel.like(tel))).order_by(
    #             Dingdan.chanpin_id, Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    # sql = """select b.user_id,b.user_name,b.icon,b.score,a.add_score from
    #     (select user_id, sum(score_new - score_old) as add_score from user_score_log
    #     where year(create_date)=year(now()) and month(create_date)=month(now())
    #     group by user_id) a join users b on a.user_id=b.user_id
    #     order by a.add_score desc limit 50"""
    #
    # dingdans = db.session.execute(sql).fetchall()

    # sql = """select * from dingdans"""
    #
    # dingdans = db.session.execute(sql).fetchall()

    # kehus = Kehu.query.filter(Kehu.user == current_user._get_current_object()).filter(
    #     or_(Kehu.fangjian.like(infostring), Kehu.chenghu.like(infostring),
    #         Kehu.tel.like(infostring))).order_by(Kehu.id.desc())  # .order_by(Guke.outtime.desc())

    return render_template('kefucxlist.html', xiaoqus=xiaoqus, form=form, xiaoquid=xiaoquid,
                           fangjian=fangjian, tel=tel, status=status)  # prewhere=prewhere,, dingdans=dingdans


@main.route('/dinghuoedlist', methods=['GET', 'POST'])
@login_required
def dinghuoedlist():
    if current_user.role != '订货员':
        return redirect(url_for('main.index'))

    # 下单时间超过6小时的才在此显示
    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)

    # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())

    dingdans = Dingdan.query.filter_by(status=3).order_by(Dingdan.chanpin_id,
                                                          Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    dingdans = Dingdan.query.filter_by(status=3).order_by(Dingdan.time2.desc(),
                                                          Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    return render_template('dinghuolist.html', dingdans=dingdans, done='已订货')  # form=form,


#
# @main.route('/rukuedlist', methods=['GET', 'POST'])
# @login_required
# def rukuedlist():
#     if current_user.role != '入库员':
#         return redirect(url_for('main.index'))
#
#     form = FineddidForm()
#
#     if form.validate_on_submit():
#         session['ddid'] = form.ddid.data
#         return redirect(url_for('main.rukuedlist'))
#
#     ddid = session.get('ddid', 0)
#
#     # 下单时间超过6小时的才在此显示
#     # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes > 2).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
#
#     # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1+datetime.timedelta(minutes=2))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
#
#     # dingdans = Dingdan.query.filter(Dingdan.status==2).filter(datetime.utcnow() > (Dingdan.time1 + timedelta(days=10))).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
#
#     # dingdans = Dingdan.query.filter(Dingdan.status==2).filter((datetime.utcnow()-Dingdan.time1).minutes>9000).order_by(Dingdan.chanpin_id, Dingdan.kehu_id)
#
#     # dingdans = Dingdan.query.filter_by(status="已下单").order_by(Dingdan.chanpin.id)  # .order_by(Guke.outtime.desc())
#
#     if ddid != '':
#         form.ddid.data = ddid
#         dingdans = Dingdan.query.filter_by(status=4).filter_by(id=ddid).order_by(Dingdan.chanpin_id,
#                                                               Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
#     else:
#         ddid = 0
#         dingdans = Dingdan.query.filter_by(status=4).order_by(Dingdan.chanpin_id,
#                                                               Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
#
#     return render_template('rukulist.html', form=form, dingdans=dingdans, done='已入库', ddid=ddid)  #
#

# @main.route('/fahuolist', methods=['GET', 'POST'])
# @login_required
# def fahuolist():
#     # form = NameForm()
#     # bujuan=None
#     kehus = Kehu.query.filter_by(user=current_user._get_current_object()).order_by(
#         Kehu.id)  # .order_by(Guke.outtime.desc())
#
#     return render_template('efahuolist.html', kehus=kehus)  # form=form,


@main.route('/addkehu', methods=['GET', 'POST'])
@login_required
def addkehu():
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = KehuForm()
    # bujuan=None

    user = current_user._get_current_object()
    if form.validate_on_submit():
        xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)
        kehu = Kehu(user=user, xiaoqu=xiaoqu, fangjian=form.fangjian.data, chenghu=form.chenghu.data, tel=form.tel.data,
                    zje=form.zje.data, beizhu=form.beizhu.data)  # , status=form.status.data,status='No'
        db.session.add(kehu)
        flash('已成功添加客户')
        return redirect(url_for('main.kehulist'))

    # kehus = Kehu.query.filter_by(user=current_user._get_current_object()).order_by(
    #     Kehu.id.desc())  # .order_by(Guke.outtime.desc())
    form.zje.data = 0
    return render_template('addkehu.html', form=form)


@main.route('/editkehu/<int:id>', methods=['GET', 'POST'])
@login_required
def editkehu(id):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = KehuForm()

    kehu = Kehu.query.get(id)
    user = current_user._get_current_object()

    if form.validate_on_submit():
        xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)

        kehu.xiaoqu = xiaoqu
        kehu.fangjian = form.fangjian.data
        kehu.chenghu = form.chenghu.data
        kehu.tel = form.tel.data
        kehu.zje = form.zje.data
        # kehu.status = form.status.data
        kehu.beizhu = form.beizhu.data

        db.session.add(kehu)
        flash('已成功修改客户')
        return redirect(url_for('main.kehulist'))

    form.xiaoqu.data = kehu.xiaoqu.id
    form.fangjian.data = kehu.fangjian
    form.chenghu.data = kehu.chenghu
    form.tel.data = kehu.tel
    form.zje.data = kehu.zje
    # form.status.data = kehu.status
    form.beizhu.data = kehu.beizhu

    return render_template('addkehu.html', form=form)


@main.route('/delkehu/<int:id>', methods=['GET', 'POST'])
@login_required
def delkehu(id):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    kehu = Kehu.query.get(id)
    # 先删除

    # 如果有订单禁止删除

    if kehu.dingdans.count() > 0:
        flash('先删订单才可以删客户')
    else:

        # for dingdan in kehu.dingdans:
        #     db.session.delete(dingdan)

        db.session.delete(kehu)
        flash('已成功删除客户')

    return redirect(url_for('main.kehulist'))


@main.route('/viewkehudd/<int:id>', methods=['GET', 'POST'])
@login_required
def viewkehudd(id):
    kehu = Kehu.query.get(id)
    return render_template('viewkehudd.html', kehu=kehu)


@main.route('/showkehudd/<int:id>', methods=['GET', 'POST'])
@login_required
def showkehudd(id):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = WilladdcpForm()

    kehu = Kehu.query.get(id)

    user = current_user._get_current_object()

    if form.validate_on_submit():

        chanpinid = form.chanpin.data
        chanpin = Chanpin.query.get(chanpinid)

        toview = ''

        if chanpin.pinming == '隐形网':
            toview = 'addyxw'

        elif chanpin.pinming == '阳台窗':
            toview = 'addytc'
        elif chanpin.pinming == '玻璃':
            toview = 'addbl'

        elif chanpin.pinming == '纱门':
            toview = 'addsm'
        elif chanpin.pinming == '晾衣杆':
            toview = 'addlyg'
        elif chanpin.pinming == '晾衣机':
            toview = 'addlyj'
        elif chanpin.pinming == '纱窗':
            toview = 'addsc'
        elif chanpin.pinming == '窗花':
            toview = 'addch'
        elif chanpin.pinming == '指纹锁':
            toview = 'addzws'
        elif chanpin.pinming == '杂项':
            toview = 'addjx'
        else:
            pass

        return redirect(url_for('main.' + toview, cpid=chanpinid, khid=kehu.id))

    return render_template('showkehudd.html', form=form, kehu=kehu)


def getnewfilename(upfilename):
    # ext
    ext = os.path.splitext(upfilename)[1]

    # uploaddir
    pdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    uploaddir = os.path.join(pdir, 'static/upload')

    # filenamehead
    t = time.time()
    nowTime = lambda: int(round(t * 1000))
    tmpstr = current_user.username + str(nowTime())
    md5filename = hashlib.md5()
    md5filename.update(tmpstr.encode('utf-8'))
    filenamehead = md5filename.hexdigest()[:15]

    savefilename = '%s%s' % (filenamehead, ext)
    fullsavefilename = os.path.join(uploaddir, savefilename)

    return fullsavefilename


# 隐形网
@main.route('/addyxw/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addyxw(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = YxwForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        if form.submit.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            # savefilename

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                              color=form.color.data, beizhu=form.beizhu.data,
                              tushipic=os.path.basename(fullsavefilename),
                              status=1)

            db.session.add(dingdan)

            flash('已成功添加')

            # return redirect(url_for('main.showkehudd', id=khid))


        elif form.submita.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            # savefilename

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                              color=form.color.data, beizhu=form.beizhu.data,
                              tushipic=os.path.basename(fullsavefilename),
                              status=6)

            db.session.add(dingdan)

            flash('已成功追加, 状态转已收货')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc='')


# 阳台窗
@main.route('/addytc/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addytc(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = YtcForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
        else:
            fullsavefilename = ''

        # savefilename

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          meikongkuan_bashoudigao=form.dungo.data, shanshu=form.lango.data, shuowei=form.guanwei.data,
                          color=form.color.data, beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename),
                          status=1)

        db.session.add(dingdan)

        flash('已成功添加')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc='')


# 玻璃
@main.route('/addbl/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addbl(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = BlForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
        else:
            fullsavefilename = ''

        # savefilename

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename),
                          status=1)

        db.session.add(dingdan)

        flash('已成功添加')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc='')


# # 纱门
@main.route('/addsm/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addsm(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = SmForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
        else:
            fullsavefilename = ''

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          color=form.color.data,
                          meikongkuan_bashoudigao=form.neikuan.data, shanshu=form.shanshu.data,
                          zhonghengtiaoshu_gantiaoshu=form.zhonghengtiaoshu.data,
                          shuowei=form.shuowei.data, zhangfa_dengfenshu_kaishuofangshi=form.zhangfa.data,
                          beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename),
                          status=1)

        db.session.add(dingdan)

        flash('已成功添加')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc='')


# 晾衣杆
@main.route('/addlyg/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addlyg(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = LygForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        if form.submit.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, kuan_chang=form.chang.data, gao=form.gao.data,
                              zhonghengtiaoshu_gantiaoshu=form.gantiaoshu.data, color=form.color.data,
                              beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=1)

            db.session.add(dingdan)

            flash('已成功添加')

        if form.submita.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, kuan_chang=form.chang.data, gao=form.gao.data,
                              zhonghengtiaoshu_gantiaoshu=form.gantiaoshu.data, color=form.color.data,
                              beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=6)

            db.session.add(dingdan)

            flash('已成功追加, 状态转已收货')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# 晾衣机
@main.route('/addlyj/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addlyj(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = LyjForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        if form.submit.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, kuan_chang=form.chang.data, gao=form.gao.data,
                              zhonghengtiaoshu_gantiaoshu=form.gantiaoshu.data, color=form.color.data,
                              beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=1)

            db.session.add(dingdan)

            flash('已成功添加')

        if form.submita.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, kuan_chang=form.chang.data, gao=form.gao.data,
                              zhonghengtiaoshu_gantiaoshu=form.gantiaoshu.data, color=form.color.data,
                              beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=6)

            db.session.add(dingdan)

            flash('已成功追加, 状态转已收货')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# # 纱窗
@main.route('/addsc/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addsc(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = ScForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
        else:
            fullsavefilename = ''
        # if form.ishaveht.data == 0:
        #     ishaveht = False
        # else:
        #     ishaveht = True

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          color=form.color.data,
                          meikongkuan_bashoudigao=form.bashoudg.data,
                          zhangfa_dengfenshu_kaishuofangshi=form.dengfenshu.data,
                          ishaveht=form.ishaveht.data, shuowei=form.shuowei.data,
                          beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=1)

        db.session.add(dingdan)

        flash('已成功添加')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# # 窗花
@main.route('/addch/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addch(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = ChForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
        else:
            fullsavefilename = ''

        # if form.ishaveht.data == 0:
        #     ishaveht = False
        # else:
        #     ishaveht = True

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          color=form.color.data,
                          meikongkuan_bashoudigao=form.bashoudg.data,
                          # zhangfa_dengfenshu_kaishuofangshi=form.dengfenshu.data,ishaveht=form.ishaveht.data,
                          shuowei=form.shuowei.data,
                          beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=1)

        db.session.add(dingdan)

        flash('已成功添加')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# # 指纹锁
@main.route('/addzws/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addzws(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = ZwsForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        if form.submit.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, color=form.color.data, shuowei=form.shuowei.data,
                              zhangfa_dengfenshu_kaishuofangshi=form.kaishuofs.data,
                              beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=1)

            db.session.add(dingdan)

            flash('已成功添加')

        if form.submita.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, color=form.color.data, shuowei=form.shuowei.data,
                              zhangfa_dengfenshu_kaishuofangshi=form.kaishuofs.data,
                              beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename), status=6)

            db.session.add(dingdan)

            flash('已成功追加, 状态转已收货')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# # 杂项
@main.route('/addjx/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addjx(cpid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = JxForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        if form.submit.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, beizhu=form.beizhu.data,
                              tushipic=os.path.basename(fullsavefilename), status=1)

            db.session.add(dingdan)

            flash('已成功添加')

        if form.submita.data:

            uploaded_file = form.uploadfile.data
            if uploaded_file:
                # # 获取文件的大小了，单位是字节
                # size = len(uploaded_file.read())
                # if size > 1048576:  # 取不到
                #     flash('文件超过1M，不能上传')
                #     fullsavefilename = ''
                # else:
                fullsavefilename = getnewfilename(uploaded_file.filename)
                uploaded_file.save(fullsavefilename)
            else:
                fullsavefilename = ''

            dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                              xinghao=form.xinghao.data, beizhu=form.beizhu.data,
                              tushipic=os.path.basename(fullsavefilename), status=6)

            db.session.add(dingdan)

            flash('已成功追加, 状态转已收货')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


@main.route('/deldingdan/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def deldingdan(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    dingdan = Dingdan.query.get(ddid)
    db.session.delete(dingdan)
    flash('已成功删除订单')

    return redirect(url_for('main.showkehudd', id=khid))


@main.route('/readddingdan/<int:khid>/<int:ddid>', methods=['GET', 'POST'])
@login_required
def readddingdan(khid, ddid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    # 复制  添加 跳转到编辑

    dingdano = Dingdan.query.get(ddid)
    # chanpin = Chanpin.query.get(dingdano)
    kehu = Kehu.query.get(khid)

    dingdan = Dingdan(chanpin=dingdano.chanpin, kehu=dingdano.kehu, weizhi=dingdano.weizhi, shuliang=dingdano.shuliang,
                      xinghao=dingdano.xinghao, kuan_chang=dingdano.kuan_chang, gao=dingdano.gao,
                      shuowei=dingdano.shuowei,
                      zhonghengtiaoshu_gantiaoshu=dingdano.zhonghengtiaoshu_gantiaoshu, color=dingdano.color,
                      meikongkuan_bashoudigao=dingdano.meikongkuan_bashoudigao,
                      shanshu=dingdano.shanshu,
                      zhangfa_dengfenshu_kaishuofangshi=dingdano.zhangfa_dengfenshu_kaishuofangshi,
                      ishaveht=dingdano.ishaveht, beizhu='重订（' + str(ddid) + '）' + dingdano.beizhu, status=1)

    db.session.add(dingdan)
    db.session.commit()
    ddid = dingdan.id

    dingdano.beizhu = '已重订（' + str(ddid) + '）' + dingdano.beizhu
    db.session.add(dingdano)

    user = current_user._get_current_object()

    toview = ''
    pinming = dingdano.chanpin.pinming

    flash('重订同品类：' + pinming)

    if pinming == '隐形网':
        toview = 'edityxw'
    elif pinming == '阳台窗':
        toview = 'editytc'
    elif pinming == '玻璃':
        toview = 'editbl'
    elif pinming == '纱门':
        toview = 'editsm'
    elif pinming == '晾衣杆':
        toview = 'editlyg'
    elif pinming == '晾衣机':
        toview = 'editlyj'
    elif pinming == '纱窗':
        toview = 'editsc'
    elif pinming == '窗花':
        toview = 'editch'
    elif pinming == '指纹锁':
        toview = 'editzws'
    elif pinming == '杂项':
        toview = 'editjx'

    else:
        pass

    return redirect(url_for('main.' + toview, ddid=ddid, khid=khid))


@main.route('/editdingdan/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editdingdan(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    dingdan = Dingdan.query.get(ddid)
    pinming = dingdan.chanpin.pinming

    # chanpin = Chanpin.query.get(dingdan.chanpin.id)

    if pinming == '隐形网':
        toview = 'edityxw'
    elif pinming == '阳台窗':
        toview = 'editytc'
    elif pinming == '玻璃':
        toview = 'editbl'
    elif pinming == '纱门':
        toview = 'editsm'
    elif pinming == '晾衣杆':
        toview = 'editlyg'
    elif pinming == '晾衣机':
        toview = 'editlyj'
    elif pinming == '纱窗':
        toview = 'editsc'
    elif pinming == '窗花':
        toview = 'editch'
    elif pinming == '指纹锁':
        toview = 'editzws'
    elif pinming == '杂项':
        toview = 'editjx'
    else:
        pass

    return redirect(url_for('main.' + toview, ddid=ddid, khid=khid))


# 隐形网
@main.route('/edityxw/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def edityxw(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = YxwForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.kuan.data
        dingdan.gao = form.gao.data
        dingdan.color = form.color.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color
    form.beizhu.data = dingdan.beizhu

    # form.beizhu.tushipic = fullsavefilename,  dingdan.tushipic

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# 阳台窗
@main.route('/editytc/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editytc(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = YtcForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.kuan.data
        dingdan.gao = form.gao.data

        dingdan.meikongkuan_bashoudigao = form.dungo.data
        dingdan.shanshu = form.lango.data
        dingdan.shuowei = form.guanwei.data

        dingdan.color = form.color.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao

    form.dungo.data = dingdan.meikongkuan_bashoudigao
    form.lango.data = dingdan.shanshu
    form.guanwei.data = dingdan.shuowei

    form.color.data = dingdan.color
    form.beizhu.data = dingdan.beizhu

    # form.beizhu.tushipic = fullsavefilename,  dingdan.tushipic

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# 玻璃
@main.route('/editbl/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editbl(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = BlForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.kuan.data
        dingdan.gao = form.gao.data

        # dingdan.meikongkuan_bashoudigao = form.dungo.data
        # dingdan.shanshu = form.lango.data
        # dingdan.shuowei = form.guanwei.data

        # dingdan.color = form.color.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao

    # form.dungo.data = dingdan.meikongkuan_bashoudigao
    # form.lango.data = dingdan.shanshu
    # form.guanwei.data = dingdan.shuowei

    # form.color.data = dingdan.color
    form.beizhu.data = dingdan.beizhu

    # form.beizhu.tushipic = fullsavefilename,  dingdan.tushipic

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# # 纱门
@main.route('/editsm/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editsm(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = SmForm()

    if form.validate_on_submit():

        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.kuan.data
        dingdan.gao = form.gao.data
        dingdan.color = form.color.data

        dingdan.meikongkuan_bashoudigao = form.neikuan.data
        dingdan.shanshu = form.shanshu.data
        dingdan.zhonghengtiaoshu_gantiaoshu = form.zhonghengtiaoshu.data
        dingdan.shuowei = form.shuowei.data
        dingdan.zhangfa_dengfenshu_kaishuofangshi = form.zhangfa.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)

        flash('已成功修改订制')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)
    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    form.neikuan.data = dingdan.meikongkuan_bashoudigao

    form.shanshu.data = str(dingdan.shanshu)
    form.zhonghengtiaoshu.data = str(dingdan.zhonghengtiaoshu_gantiaoshu)

    form.shuowei.data = dingdan.shuowei
    form.zhangfa.data = dingdan.zhangfa_dengfenshu_kaishuofangshi
    form.beizhu.data = dingdan.beizhu

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# # 晾衣杆
@main.route('/editlyg/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editlyg(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = LygForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.chang.data
        dingdan.gao = form.gao.data
        dingdan.color = form.color.data
        dingdan.zhonghengtiaoshu_gantiaoshu = form.gantiaoshu.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.chang.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    # 这里如果不做Str 则不能显示原来的数据！！
    form.gantiaoshu.data = str(dingdan.zhonghengtiaoshu_gantiaoshu)

    form.beizhu.data = dingdan.beizhu

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# # 晾衣机
@main.route('/editlyj/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editlyj(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = LyjForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.chang.data
        dingdan.gao = form.gao.data
        dingdan.color = form.color.data
        dingdan.zhonghengtiaoshu_gantiaoshu = form.gantiaoshu.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.chang.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    # 这里如果不做Str 则不能显示原来的数据！！
    form.gantiaoshu.data = str(dingdan.zhonghengtiaoshu_gantiaoshu)

    form.beizhu.data = dingdan.beizhu

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# # 纱窗
@main.route('/editsc/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editsc(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = ScForm()

    if form.validate_on_submit():

        # if form.ishaveht.data == 0:
        #     ishaveht = False
        # else:
        #     ishaveht = True

        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.kuan.data
        dingdan.gao = form.gao.data
        dingdan.color = form.color.data

        dingdan.meikongkuan_bashoudigao = form.bashoudg.data
        dingdan.zhangfa_dengfenshu_kaishuofangshi = form.dengfenshu.data
        dingdan.shuowei = form.shuowei.data
        dingdan.ishaveht = form.ishaveht.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)
        db.session.commit()

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    form.bashoudg.data = dingdan.meikongkuan_bashoudigao
    form.dengfenshu.data = dingdan.zhangfa_dengfenshu_kaishuofangshi
    form.shuowei.data = dingdan.shuowei
    # if dingdan.ishaveht:
    #     ishaveht = 1
    # else:
    #     ishaveht = 0
    form.ishaveht.data = dingdan.ishaveht
    form.beizhu.data = dingdan.beizhu

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# # 窗花
@main.route('/editch/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editch(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = ChForm()

    if form.validate_on_submit():

        # if form.ishaveht.data == 0:
        #     ishaveht = False
        # else:
        #     ishaveht = True

        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.kuan_chang = form.kuan.data
        dingdan.gao = form.gao.data
        dingdan.color = form.color.data

        dingdan.meikongkuan_bashoudigao = form.bashoudg.data
        # dingdan.zhangfa_dengfenshu_kaishuofangshi = form.dengfenshu.data
        dingdan.shuowei = form.shuowei.data
        # dingdan.ishaveht = form.ishaveht.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)
        db.session.commit()

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    form.bashoudg.data = dingdan.meikongkuan_bashoudigao
    # form.dengfenshu.data = dingdan.zhangfa_dengfenshu_kaishuofangshi
    form.shuowei.data = dingdan.shuowei
    # if dingdan.ishaveht:
    #     ishaveht = 1
    # else:
    #     ishaveht = 0
    # form.ishaveht.data = dingdan.ishaveht
    form.beizhu.data = dingdan.beizhu

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# # 指纹锁
@main.route('/editzws/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editzws(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = ZwsForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data
        dingdan.color = form.color.data
        dingdan.shuowei = form.shuowei.data
        dingdan.zhangfa_dengfenshu_kaishuofangshi = form.kaishuofs.data
        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)
        db.session.commit()

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao
    form.color.data = dingdan.color
    form.shuowei.data = dingdan.shuowei
    form.kaishuofs.data = dingdan.zhangfa_dengfenshu_kaishuofangshi
    form.beizhu.data = dingdan.beizhu

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


# # 杂项
@main.route('/editjx/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editjx(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    form = JxForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi = form.weizhi.data
        dingdan.shuliang = form.shuliang.data
        dingdan.xinghao = form.xinghao.data

        dingdan.beizhu = form.beizhu.data

        uploaded_file = form.uploadfile.data
        if uploaded_file:
            # # 获取文件的大小了，单位是字节
            # size = len(uploaded_file.read())
            # if size > 1048576:  # 取不到
            #     flash('文件超过1M，不能上传')
            #     fullsavefilename = ''
            # else:
            #     uploaded_file = form.uploadfile.data
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)
        # else:
        #     fullsavefilename = ''

        db.session.add(dingdan)
        db.session.commit()

        flash('已成功修改')

        return redirect(url_for('main.showkehudd', id=khid))

    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = str(dingdan.shuliang)
    form.xinghao.data = dingdan.xinghao

    form.beizhu.data = dingdan.beizhu

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu, imgsrc=dingdan.tushipic)


@main.route('/doxiadan/<int:khid>', methods=['GET', 'POST'])
@login_required
def doxiadan(khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    for dingdan in kehu.dingdans:
        if dingdan.status == 1:
            dingdan.status = 2
            dingdan.time2 = datetime.utcnow()

    db.session.add(kehu)
    flash('已确认下单')

    return redirect(url_for('main.showkehudd', id=khid))


@main.route('/doxiadanone/<int:khid>/<int:ddid>', methods=['GET', 'POST'])
@login_required
def doxiadanone(khid, ddid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 2
    dingdan.time2 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认下单')

    return redirect(url_for('main.showkehudd', id=khid))


@main.route('/undoxiadanone/<int:khid>/<int:ddid>', methods=['GET', 'POST'])
@login_required
def undoxiadanone(khid, ddid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 1
    dingdan.time2 = None

    db.session.add(dingdan)
    flash('已撤单')

    return redirect(url_for('main.showkehudd', id=khid))


@main.route('/rukuone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def rukuone(ddid):
    if current_user.role != '入库员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 4
    dingdan.time4 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认入库')

    return redirect(url_for('main.rukulist'))


@main.route('/unrukuone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def unrukuone(ddid):
    if current_user.role != '入库员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 3
    dingdan.time4 = None

    db.session.add(dingdan)
    flash('已撤入')

    return redirect(url_for('main.rukulist'))


@main.route('/fahuoone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def fahuoone(ddid):
    if current_user.role != '发货员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 5
    dingdan.time5 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认发货')

    return redirect(url_for('main.fahuolist'))


@main.route('/unfahuoone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def unfahuoone(ddid):
    if current_user.role != '发货员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 4
    dingdan.time5 = None

    db.session.add(dingdan)
    flash('已撤发')

    return redirect(url_for('main.fahuolist'))


@main.route('/udinghuoone/<int:ddid>', methods=['GET'])
@login_required
def udinghuoone(ddid):
    if current_user.role != '订货员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 2
    dingdan.time3 = None

    db.session.add(dingdan)
    flash('已撤订')

    return redirect(url_for('main.dinghuoedlist'))


@main.route('/shouhuoone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def shouhuoone(ddid):
    if current_user.role != '收货员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 6
    dingdan.time6 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认收货')

    return redirect(url_for('main.shouhuolist'))


@main.route('/doselshouhuo/<selids>', methods=['GET', 'POST'])
@login_required
def doselshouhuo(selids):
    if current_user.role != '收货员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    # dingdan = Dingdan.query.get(ddid)
    # dingdan.status = 6
    # dingdan.time5 = datetime.utcnow()
    #
    # db.session.add(dingdan)

    selids = selids.strip(',')
    selids = list(eval('[' + selids + ']'))

    # dingdan = Dingdan.query.filter(Dingdan.id in selids).update({Dingdan.status:6, Dingdan.time5:datetime.utcnow()})

    # dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 6, 'time5': datetime.utcnow()},
    #                                                               synchronize_session=False)

    # 这样
    dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 6, 'time6': datetime.utcnow()},
                                                                  synchronize_session=False)
    #
    # dingdans = Dingdan.query.filter(Dingdan.id.in_(selids)).all()
    #
    # for dingdan in dingdans:
    #     dingdan.status = 6
    #     dingdan.time5 = datetime.utcnow()
    #     db.session.add(dingdan)

    # dingdan.status = 6
    # dingdan.time5 = datetime.utcnow()
    # db.session.add(dingdan)

    # flash('已确认收货')

    # return redirect(url_for('main.shouhuolist'))
    return 'done'


@main.route('/unshouhuoone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def unshouhuoone(ddid):
    if current_user.role != '收货员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 3
    dingdan.time4 = None

    db.session.add(dingdan)
    flash('已撤收')

    return redirect(url_for('main.shouhuolist'))


@main.route('/paigongone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def paigongone(ddid):
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 7
    dingdan.time7 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认派工')

    return redirect(url_for('main.paigonglist'))


@main.route('/dopaigong/<selids>/<sgd>', methods=['GET', 'POST'])
@login_required
def dopaigong(selids, sgd):
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))

    selids = selids.strip(',')
    selids = list(eval('[' + selids + ']'))

    # dingdan = Dingdan.query.filter(Dingdan.id in selids).update({Dingdan.status:6, Dingdan.time5:datetime.utcnow()})

    # dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 6, 'time5': datetime.utcnow()},
    #                                                               synchronize_session=False)

    # 这样
    # dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 7, 'time8': datetime.utcnow(),'duizhang':sgd},
    #                                                               synchronize_session=False)
    dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update(
        {'status': 7, 'time7': datetime.utcnow(), 'azd_id': sgd},
        synchronize_session=False)
    return 'done'


@main.route('/unpaigongone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def unpaigongone(ddid):
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 6
    dingdan.time7 = None

    dingdan.azd_id = None

    dingdan.az_status = None
    dingdan.az_time_1 = None
    dingdan.az_time1 = None
    dingdan.az_time3 = None

    # dingdan.duizhang = None

    db.session.add(dingdan)
    flash('已派工')

    return redirect(url_for('main.paigonglist'))


@main.route('/stoplc/<int:ddid>', methods=['GET', 'POST'])
@login_required
def stoplc(ddid):
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))

    form = stoplcddidForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)
        dingdan.status = -1
        dingdan.time_1 = datetime.utcnow()
        dingdan.user_1_id = current_user.id

        dingdan.beizhue = form.beizhue.data  # "终止流程"

        # dingdan.duizhang = None

        db.session.add(dingdan)
        flash('已终止流程')

        return redirect(url_for('main.paigonglist'))

    dingdan = Dingdan.query.get(ddid)

    form.beizhue.data = dingdan.beizhue

    # form.beizhu.tushipic = fullsavefilename,  dingdan.tushipic

    return render_template('stoplc.html', form=form, dingdan=dingdan)



@main.route('/accstop/<int:ddid>', methods=['GET', 'POST'])
@login_required
def accstop(ddid):
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))


    dingdan = Dingdan.query.get(ddid)
    dingdan.status = -1
    dingdan.time_1 = datetime.utcnow()
    dingdan.user_1_id = current_user.id

    dingdan.beizhue = dingdan.az_beizhue

    # dingdan.duizhang = None

    db.session.add(dingdan)
    flash('已终止流程')

    return redirect(url_for('main.paigonglist'))



@main.route('/azstop/<int:ddid>', methods=['GET', 'POST'])
@login_required
def azstop(ddid):
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))

    form = azstopddidForm()

    if form.validate_on_submit():
        dingdan = Dingdan.query.get(ddid)
        dingdan.az_status = -1
        dingdan.az_time_1 = datetime.utcnow()
        # dingdan.az_user_1_id = current_user.id

        dingdan.az_beizhue = form.az_beizhue.data  # "终止流程"

        # dingdan.duizhang = None

        # dingdan.status = -1
        # dingdan.time_1 = datetime.utcnow()

        db.session.add(dingdan)
        flash('已终止安装')

        return redirect(url_for('main.azddoing'))

    dingdan = Dingdan.query.get(ddid)

    form.az_beizhue.data = dingdan.az_beizhue

    # form.beizhu.tushipic = fullsavefilename,  dingdan.tushipic

    return render_template('azstop.html', form=form, dingdan=dingdan)


@main.route('/getrenwu/<int:ddid>', methods=['GET', 'POST'])
@login_required
def getrenwu(ddid):
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.az_status = 1
    dingdan.az_time1 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认接单')

    return redirect(url_for('main.azdwillget'))


@main.route('/azjiedansel/<selids>', methods=['GET', 'POST'])
@login_required
def azjiedansel(selids):
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))

    selids = selids.strip(',')
    selids = list(eval('[' + selids + ']'))

    # dingdan = Dingdan.query.filter(Dingdan.id in selids).update({Dingdan.status:6, Dingdan.time5:datetime.utcnow()})

    # dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 6, 'time5': datetime.utcnow()},
    #                                                               synchronize_session=False)

    # 这样
    # dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 7, 'time8': datetime.utcnow(),'duizhang':sgd},
    #
    #                                                            synchronize_session=False)
    dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update(
        {'az_status': 1, 'az_time1': datetime.utcnow()},
        synchronize_session=False)

    flash('已确认接单')

    return redirect(url_for('main.azdwillget'))


@main.route('/azwancheng/<int:ddid>', methods=['GET', 'POST'])
@login_required
def azwancheng(ddid):
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.az_status = 3
    dingdan.az_time3 = datetime.utcnow()

    dingdan.status = 8
    dingdan.time8 = datetime.utcnow()

    dingdan.user8_id = current_user.id

    db.session.add(dingdan)
    flash('已申请完成')

    return redirect(url_for('main.anzhuanglist'))


@main.route('/azwangongsel/<selids>', methods=['GET', 'POST'])
@login_required
def azwangongsel(selids):
    if current_user.role != '安装队':
        return redirect(url_for('main.index'))

    selids = selids.strip(',')
    selids = list(eval('[' + selids + ']'))

    # dingdan = Dingdan.query.filter(Dingdan.id in selids).update({Dingdan.status:6, Dingdan.time5:datetime.utcnow()})

    # dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 6, 'time5': datetime.utcnow()},
    #                                                               synchronize_session=False)

    # 这样
    # dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 7, 'time8': datetime.utcnow(),'duizhang':sgd},
    #
    #                                                            synchronize_session=False)
    dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update(
        {'az_status': 3, 'az_time3': datetime.utcnow(), 'status': 8, 'time8': datetime.utcnow(),
         'user8_id': current_user.id},
        synchronize_session=False)

    flash('已申请完成')

    return redirect(url_for('main.azddoing'))


@main.route('/wanchengone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def wanchengone(ddid):
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 8
    dingdan.time8 = datetime.utcnow()

    dingdan.user8_id = current_user.id

    db.session.add(dingdan)
    flash('已确认完成')

    return redirect(url_for('main.paigonglist'))


@main.route('/unwanchengone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def unwanchengone(ddid):
    if current_user.role != '派工员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 7
    dingdan.time8 = None

    db.session.add(dingdan)
    flash('已撤完')

    return redirect(url_for('main.paigonglist'))


@main.route('/qingkunone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def qingkunone(ddid):
    if current_user.role != '清款员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 9
    dingdan.time9 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认清款')

    return redirect(url_for('main.qingkuanlist'))


@main.route('/unqingkunone/<int:ddid>', methods=['GET', 'POST'])
@login_required
def unqingkunone(ddid):
    if current_user.role != '清款员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = 2
    # kehu.time1 = datetime.utcnow()

    # for dingdan in kehu.dingdans:
    #     dingdan.status = 2
    #     dingdan.time1 = datetime.utcnow()

    dingdan = Dingdan.query.get(ddid)
    dingdan.status = 8
    dingdan.time9 = None

    db.session.add(dingdan)
    flash('已撤清款')

    return redirect(url_for('main.qingkuanlist'))


@main.route('/qingkunonek/<int:khid>', methods=['GET', 'POST'])
@login_required
def qingkunonek(khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    kehu = Kehu.query.get(khid)
    kehu.status = 4
    kehu.time3 = datetime.utcnow()

    for dingdan in kehu.dingdans:
        if dingdan.status == 8:
            dingdan.status = 9
            dingdan.time9 = datetime.utcnow()

    db.session.add(kehu)

    # dingdan = Dingdan.query.get(khid)
    # dingdan.status = 9
    # dingdan.time9 = datetime.utcnow()
    #
    # db.session.add(dingdan)

    flash('已确认清款')

    return redirect(url_for('main.kehulist'))


@main.route('/unqingkunonek/<int:khid>', methods=['GET', 'POST'])
@login_required
def unqingkunonek(khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    kehu = Kehu.query.get(khid)
    kehu.status = 3
    # kehu.time2 = datetime.utcnow()
    kehu.time3 = None

    for dingdan in kehu.dingdans:
        if dingdan.status == 9:
            dingdan.status = 8
            # dingdan.time9 = datetime.utcnow()
            dingdan.time9 = None

    db.session.add(kehu)

    # dingdan = Dingdan.query.get(ddid)
    # dingdan.status = 8
    # dingdan.time9 = None
    #
    # db.session.add(dingdan)
    flash('已撤清款')

    return redirect(url_for('main.qingkuanlist'))


@main.route('/setkehuover/<int:khid>', methods=['GET', 'POST'])
@login_required
def setkehuover(khid):
    kehu = Kehu.query.get(khid)
    kehu.status = u'已完成'
    # kehu.xdtime = datetime.utcnow

    # for dingdan in kehu.dingdans:
    #     dingdan.status = u'已下单'

    db.session.add(kehu)
    flash('已标志完成客户')

    return redirect(url_for('main.showkehudd', id=khid))


@main.route('/outseltoxls/<string:pm>/<string:selids>', methods=['GET', 'POST'])
@login_required
def outseltoxls(pm, selids):
    if current_user.role != '订货员':
        return redirect(url_for('main.index'))

    selids = selids.strip(',')
    selids = list(eval('[' + selids + ']'))

    # 取出品名  过滤业务下单
    chanpin = Chanpin.query.filter_by(pinming=pm).first()

    # pdingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).first();
    # pm = pdingdan.chanpin.pinming

    # dingdans = Dingdan.query.filter_by(status=2).order_by(Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    # dingdans = Dingdan.query.filter_by(status=2, chanpin_id=chanpin.id).order_by(Dingdan.chanpin_id,
    #                                                                        Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    dingdans = Dingdan.query.filter(and_(Dingdan.id.in_(selids), Dingdan.chanpin_id == chanpin.id)).order_by(
        Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    # return dingdans

    if pm == '隐形网':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"颜色",
            u"备注",
            u"业务员（电话）")

    elif pm == '阳台窗':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）",
            u"窗台高（毫米）",
            u'栏高（毫米）', u'管位', u"颜色",
            u"备注", u"业务员（电话）")

    elif pm == '玻璃':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）",
            u"备注", u"业务员（电话）")

    elif pm == '纱门':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）",
            u"内空宽（毫米）",
            u"颜色", u'扇数', u'中横条数', u'锁位', u'装法',
            u"备注", u"业务员（电话）")

    elif pm == '晾衣杆' or pm == '晾衣机':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"长（毫米）", u"高（毫米）", u"杆条数",
            u"颜色",
            u"备注", u"业务员（电话）")

    elif pm == '纱窗':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）",
            u"把手底高（毫米）",
            u"锁位", u"颜色", u"等分数", u"有否横条", u"备注",
            u"业务员（电话）")

    elif pm == '窗花':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）",
            u"把手底高（毫米）",
            u"锁位", u"颜色", u"备注",
            u"业务员（电话）")

    elif pm == '指纹锁':
        headers = (
            u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"颜色", u"锁位", u"开锁方式",
            u"备注",
            u"业务员（电话）")

    elif pm == '杂项':
        headers = (u"订单号", u"下单时间", u"小区", u"地址", u"房间", u"客户", u"电话", u"产品", u"位置", u"数量", u"型号", u"备注", u"业务员（电话）")

    info = []
    data = tablib.Dataset(*info, headers=headers)  # headers 数量要与 data 致

    for dingdan in dingdans:

        if pm == '隐形网':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, u'隐形网', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.color, dingdan.beizhu, dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '阳台窗':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, u'阳台窗', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.shanshu, dingdan.shuowei, dingdan.color,
                 dingdan.beizhu, dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '玻璃':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, u'玻璃', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.beizhu, dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '纱门':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, u'纱门', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.color, dingdan.shanshu, dingdan.zhonghengtiaoshu_gantiaoshu,
                 dingdan.shuowei, dingdan.zhangfa_dengfenshu_kaishuofangshi, dingdan.beizhu,
                 dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '晾衣杆' or pm == '晾衣机':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, pm, dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.zhonghengtiaoshu_gantiaoshu, dingdan.color, dingdan.beizhu,
                 dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '纱窗':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, pm, dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.shuowei, dingdan.color,
                 dingdan.zhangfa_dengfenshu_kaishuofangshi, dingdan.ishaveht, dingdan.beizhu,
                 dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '窗花':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, pm, dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.shuowei, dingdan.color,
                 dingdan.beizhu, dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '指纹锁':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, u'指纹锁', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.color, dingdan.shuowei,
                 dingdan.zhangfa_dengfenshu_kaishuofangshi, dingdan.beizhu,
                 dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

        elif pm == '杂项':
            data.append(
                [dingdan.id, dingdan.time2.strftime('%Y-%m-%d %H:%M'), dingdan.kehu.xiaoqu.xiaoqu,
                 dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.fangjian,
                 dingdan.kehu.chenghu, dingdan.kehu.tel, pm, dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.beizhu, dingdan.kehu.user.username + '(' + dingdan.kehu.user.tel + ')'])

    t = time.time()
    nowTime = lambda: int(round(t * 1000))
    tmpstr = current_user.username + str(nowTime())
    md5filename = hashlib.md5()
    md5filename.update(tmpstr.encode('utf-8'))
    filenamehead = md5filename.hexdigest()[:15]

    # 导出excel表
    open('app/cxls/xxx.xls', 'wb').write(data.xls)

    response = make_response(send_file("cxls/xxx.xls"))
    response.headers["Content-Disposition"] = "attachment; filename=" + 'outdinghuo' + ".xls;"
    return response

    # 导出excel表
    # open('app/cxls/'+filenamehead+'.xls', 'wb').write(data.xls)
    #
    # response = make_response(send_file("cxls/"+filenamehead+".xls"))
    # response.headers["Content-Disposition"] = "attachment; filename=" + filenamehead + ".xls;"
    # return response

    # return redirect(url_for('main.showkehudd', id=1))


@main.route('/taggetitsel/<string:pm>/<string:selids>', methods=['GET', 'POST'])
@login_required
def taggetitsel(pm, selids):
    if current_user.role != '订货员':
        return redirect(url_for('main.index'))

    selids = selids.strip(',')
    selids = list(eval('[' + selids + ']'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = u'已完成'
    # #kehu.xdtime = datetime.utcnow
    #
    # # for dingdan in kehu.dingdans:
    # #     dingdan.status = 3
    #
    #
    # db.session.add(kehu)
    # flash('已标志完成客户')

    chanpin = Chanpin.query.filter_by(pinming=pm).first()

    dingdans = Dingdan.query.filter(and_(Dingdan.id.in_(selids), Dingdan.chanpin_id == chanpin.id))
    for dingdan in dingdans:
        dingdan.status = 3
        dingdan.time3 = datetime.utcnow()
        db.session.add(dingdan)

    Dingdan.query.filter(and_(Dingdan.id.in_(selids), Dingdan.chanpin_id == chanpin.id)).update(
        {'status': 3, 'time3': datetime.utcnow()},
        synchronize_session=False)

    # dingdans = Dingdan.query.filter_by(status=2, chanpin_id=chanpin.id)
    #
    # for dingdan in dingdans:
    #     dingdan.status = 3
    #     dingdan.time2 = datetime.utcnow()
    #     db.session.add(dingdan)

    # return redirect(url_for('main.dinghuolist'))

    return 'done'


@main.route('/outtoxls/<string:pm>', methods=['GET', 'POST'])
@login_required
def outtoxls(pm):
    if current_user.role != '订货员':
        return redirect(url_for('main.index'))

    # 取出品名  过滤业务下单
    chanpin = Chanpin.query.filter_by(pinming=pm).first()
    dingdans = Dingdan.query.filter_by(status=2, chanpin_id=chanpin.id).order_by(Dingdan.chanpin_id,
                                                                                 Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())

    if pm == '隐形网':
        headers = (
            u"订单号", u"下单时间", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"颜色", u"备注", u"客户", u"电话", u"地址", u"小区",
            u"房间")

    elif pm == '阳台窗':
        headers = (
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"窗台高（毫米）", u'栏高（毫米）', u'管位', u"颜色",
            u"备注", u"客户", u"电话", u"地址", u"小区", u"房间")

    elif pm == '玻璃':
        headers = (
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）",
            u"备注", u"客户", u"电话", u"地址", u"小区", u"房间")

    elif pm == '纱门':
        headers = (
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"内空宽（毫米）", u"颜色", u'扇数', u'中横条数', u'锁位', u'装法',
            u"备注", u"客户", u"电话", u"地址", u"小区", u"房间")


    elif pm == '晾衣杆' or pm == '晾衣机':
        headers = (
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"长（毫米）", u"高（毫米）", u"杆条数", u"颜色", u"备注", u"客户", u"电话", u"地址", u"小区",
            u"房间")

    elif pm == '纱窗':
        headers = (
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"把手底高（毫米）", u"锁位", u"颜色", u"等分数", u"有否横条", u"备注",
            u"客户", u"电话", u"地址", u"小区", u"房间")

    elif pm == '窗花':
        headers = (
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"把手底高（毫米）", u"锁位", u"颜色", u"备注",
            u"客户", u"电话", u"地址", u"小区", u"房间")

    elif pm == '指纹锁':
        headers = (u"订单号", u"产品", u"位置", u"数量", u"型号", u"颜色", u"锁位", u"开锁方式", u"备注", u"客户", u"电话", u"地址", u"小区", u"房间")

    info = []
    data = tablib.Dataset(*info, headers=headers)  # headers 数量要与 data 致

    for dingdan in dingdans:

        if pm == '隐形网':
            data.append(
                [dingdan.id, dingdan.time2, u'隐形网', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao,
                 dingdan.kuan_chang, dingdan.gao,
                 dingdan.color, dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])

        elif pm == '阳台窗':
            data.append(
                [dingdan.id, u'阳台窗', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.shanshu, dingdan.shuowei, dingdan.color,
                 dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])

        elif pm == '玻璃':
            data.append(
                [dingdan.id, u'玻璃', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])

        elif pm == '纱门':
            data.append(
                [dingdan.id, u'纱门', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.color, dingdan.shanshu, dingdan.zhonghengtiaoshu_gantiaoshu,
                 dingdan.shuowei, dingdan.zhangfa_dengfenshu_kaishuofangshi, dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])


        elif pm == '晾衣杆' or pm == '晾衣机':
            data.append(
                [dingdan.id, pm, dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.zhonghengtiaoshu_gantiaoshu, dingdan.color, dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])

        elif pm == '纱窗':
            data.append(
                [dingdan.id, pm, dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.shuowei, dingdan.color,
                 dingdan.zhangfa_dengfenshu_kaishuofangshi, dingdan.ishaveht, dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])

        elif pm == '窗花':
            data.append(
                [dingdan.id, pm, dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.meikongkuan_bashoudigao, dingdan.shuowei, dingdan.color,
                 dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])

        elif pm == '指纹锁':
            data.append(
                [dingdan.id, u'指纹锁', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.color, dingdan.shuowei,
                 dingdan.zhangfa_dengfenshu_kaishuofangshi, dingdan.beizhu, dingdan.kehu.chenghu,
                 dingdan.kehu.tel, dingdan.kehu.xiaoqu.dizhi, dingdan.kehu.xiaoqu.xiaoqu, dingdan.kehu.fangjian])

    t = time.time()
    nowTime = lambda: int(round(t * 1000))
    tmpstr = current_user.username + str(nowTime())
    md5filename = hashlib.md5()
    md5filename.update(tmpstr.encode('utf-8'))
    filenamehead = md5filename.hexdigest()[:15]

    # 导出excel表
    open('app/cxls/xxx.xls', 'wb').write(data.xls)

    response = make_response(send_file("cxls/xxx.xls"))
    response.headers["Content-Disposition"] = "attachment; filename=" + 'yxw' + ".xls;"
    return response

    # return redirect(url_for('main.showkehudd', id=1))


@main.route('/taggetit/<string:pm>', methods=['GET', 'POST'])
@login_required
def taggetit(pm):
    if current_user.role != '订货员':
        return redirect(url_for('main.index'))

    # kehu = Kehu.query.get(khid)
    # kehu.status = u'已完成'
    # #kehu.xdtime = datetime.utcnow
    #
    # # for dingdan in kehu.dingdans:
    # #     dingdan.status = 3
    #
    #
    # db.session.add(kehu)
    # flash('已标志完成客户')

    chanpin = Chanpin.query.filter_by(pinming=pm).first()
    dingdans = Dingdan.query.filter_by(status=2, chanpin_id=chanpin.id)

    for dingdan in dingdans:
        dingdan.status = 3
        dingdan.time3 = datetime.utcnow()
        db.session.add(dingdan)

    return redirect(url_for('main.dinghuolist'))

#
# @main.route('/list')
# def list():
#     bujuans=Bujuan.query.order_by(Bujuan.outtime.desc())
#     return render_template('list.html', bujuans=bujuans)

# @main.route('/user/<username>')
# def user(username):
#
# @main.route('/count')
# @login_required
# def count():
#
#     countbujuans = db.session.query(Xiangmu.xiangmu, db.func.sum(Bujuan.jine),Xiangmu.id).join(Bujuan).group_by(
#         Xiangmu.xiangmu).all()
#
#
#     alls = db.session.query(db.func.sum(Bujuan.jine)).all()
#
#
#     countbujuanbyusers = db.session.query(Xiangmu.xiangmu, User.username,db.func.sum(Bujuan.jine)).join(Bujuan).join(User).group_by(
#         Xiangmu.xiangmu, Bujuan.user).all()
#
#     return render_template('count.html', bujuans=countbujuans, alls=alls,countbujuanbyusers=countbujuanbyusers)
#
# @main.route('/countlist/<int:xiangmuid>')
# @login_required
# def countlist(xiangmuid):
#
#     alls = db.session.query(db.func.sum(Bujuan.jine)).all()
#
#
#     countbujuanbyusers = db.session.query(Xiangmu.xiangmu, User.username,db.func.sum(Bujuan.jine)).join(Bujuan).join(User).group_by(
#         Xiangmu.xiangmu, User.id).having(Bujuan.xiangmu_id==xiangmuid).all()
#
#     return render_template('countlist.html', alls=alls,countbujuanbyusers=countbujuanbyusers)
