# _*_ encoding: utf-8 _*_

import hashlib
import os
import time
from datetime import datetime, timedelta

from flask import redirect, url_for, render_template, flash, make_response, send_file, session, request
from flask_login import current_user, login_required
from sqlalchemy import func, engine, or_, and_

from app.models import User, Kehu, Dingdan, Chanpin, Xiaoqu
from .. import db
from .forms import NameForm, KehuForm, WilladdcpForm, YxwForm, SmForm, LyjForm, ScForm, ZwsForm, ChForm, FindkhForm, \
    KFfindForm, FineddidForm, LygForm, FinefhddidForm, FineshddidForm, FinepgddidForm, FineqkddidForm
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
    elif current_user.role == '进度客服':
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
        session['ddid'] = form.ddid.data
        session['status'] = form.status.data
        return redirect(url_for('main.paigonglist'))

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
            dingdans = Dingdan.query.filter(
                or_(Dingdan.status == 6, Dingdan.status == 7, Dingdan.status == 8)).filter_by(id=ddid).order_by(
                Dingdan.chanpin_id,
                Dingdan.kehu_id)  # .order_by(Guke.outtime.desc())
        else:
            ddid = 0

            dingdans = Dingdan.query.filter(
                or_(Dingdan.status == 6, Dingdan.status == 7, Dingdan.status == 8)).order_by(Dingdan.chanpin_id,
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

    return render_template('paigonglist.html', form=form, dingdans=dingdans, kehus=kehus, done='待发货', ddid=ddid,
                           status=status)  #


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


@main.route('/kefucxlist', methods=['GET', 'POST'])
@login_required
def kefucxlist():
    if current_user.role != '进度客服':
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
                    zje=form.zje.data, beizhu=form.beizhu.data, status=form.status.data)  # status='No'
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
        kehu.status = form.status.data
        kehu.beizhu = form.beizhu.data

        db.session.add(kehu)
        flash('已成功修改客户')
        return redirect(url_for('main.kehulist'))

    form.xiaoqu.data = kehu.xiaoqu.id
    form.fangjian.data = kehu.fangjian
    form.chenghu.data = kehu.chenghu
    form.tel.data = kehu.tel
    form.zje.data = kehu.zje
    form.status.data = kehu.status
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
        flash('先删订单才可以删')
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
        uploaded_file = form.uploadfile.data
        if uploaded_file:
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
        else:
            fullsavefilename = ''

        # savefilename

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          color=form.color.data, beizhu=form.beizhu.data, tushipic=os.path.basename(fullsavefilename),
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
        # xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)
        uploaded_file = form.uploadfile.data
        if uploaded_file:
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
        # xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)
        uploaded_file = form.uploadfile.data
        if uploaded_file:
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
        # xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)
        uploaded_file = form.uploadfile.data
        if uploaded_file:
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
        uploaded_file = form.uploadfile.data
        if uploaded_file:
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

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


@main.route('/deldingdan/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def deldingdan(ddid, khid):
    if current_user.role != '业务员':
        return redirect(url_for('main.index'))

    dingdan = Dingdan.query.get(ddid)
    db.session.delete(dingdan)
    flash('已成功删除客户')

    return redirect(url_for('main.showkehudd', id=khid))


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
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)

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
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)

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
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)

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
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)

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
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)

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
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)

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
            fullsavefilename = getnewfilename(uploaded_file.filename)
            uploaded_file.save(fullsavefilename)
            dingdan.tushipic = os.path.basename(fullsavefilename)

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
            dingdan.time1 = datetime.utcnow()

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
    dingdan.time1 = datetime.utcnow()

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
    dingdan.time1 = None

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
    dingdan.time3 = datetime.utcnow()

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
    dingdan.time3 = None

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
    dingdan.time4 = datetime.utcnow()

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
    dingdan.time4 = None

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
    dingdan.time2 = None

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
    dingdan.time5 = datetime.utcnow()

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
    dingdan = Dingdan.query.filter(Dingdan.id.in_(selids)).update({'status': 6, 'time5': datetime.utcnow()},
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
    dingdan.time6 = datetime.utcnow()

    db.session.add(dingdan)
    flash('已确认派工')

    return redirect(url_for('main.paigonglist'))


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
    dingdan.time7 = datetime.utcnow()
    dingdan.user7_id = current_user.id

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
    dingdan.time7 = None

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
    dingdan.time8 = datetime.utcnow()

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
    dingdan.time8 = None

    db.session.add(dingdan)
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
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"颜色", u"备注", u"客户", u"电话", u"地址", u"小区", u"房间")

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
                [dingdan.id, u'隐形网', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.color, dingdan.beizhu, dingdan.kehu.chenghu,
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
        dingdan.time2 = datetime.utcnow()
        db.session.add(dingdan)

    Dingdan.query.filter(and_(Dingdan.id.in_(selids), Dingdan.chanpin_id == chanpin.id)).update(
        {'status': 3, 'time2': datetime.utcnow()},
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
            u"订单号", u"产品", u"位置", u"数量", u"型号", u"宽（毫米）", u"高（毫米）", u"颜色", u"备注", u"客户", u"电话", u"地址", u"小区", u"房间")

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
                [dingdan.id, u'隐形网', dingdan.weizhi, dingdan.shuliang, dingdan.xinghao, dingdan.kuan_chang, dingdan.gao,
                 dingdan.color, dingdan.beizhu, dingdan.kehu.chenghu,
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
        dingdan.time2 = datetime.utcnow()
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
