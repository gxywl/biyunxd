# _*_ encoding: utf-8 _*_
from flask import redirect, url_for, render_template, flash
from flask_login import current_user, login_required
from sqlalchemy import func, engine

from app.models import User, Kehu, Dingdan, Chanpin, Xiaoqu
from .. import db
from .forms import NameForm, KehuForm, WilladdcpForm, YxwForm, SmForm, LyjForm, ScForm, ZwsForm
from . import main


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
    elif current_user.role == '业务员':
        # 一般用户转转到首页..
        return redirect(url_for('main.kehulist'))
    elif current_user.role == '订货员':
        # 一般用户转转到首页..
        return redirect(url_for('main.dinghuolist'))
    elif current_user.role == '发货员':
        # 一般用户转转到首页..
        return redirect(url_for('main.fahuolist'))
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
    # form = NameForm()
    # bujuan=None
    kehus = Kehu.query.filter_by(user=current_user._get_current_object()).order_by(
        Kehu.id)  # .order_by(Guke.outtime.desc())

    return render_template('kehulist.html', kehus=kehus)  # form=form,


@main.route('/dinghuolist', methods=['GET', 'POST'])
@login_required
def dinghuolist():
    # form = NameForm()
    # bujuan=None
    kehus = Kehu.query.filter_by(user=current_user._get_current_object()).order_by(
        Kehu.id)  # .order_by(Guke.outtime.desc())

    return render_template('dinghuolist.html', kehus=kehus)  # form=form,


@main.route('/fahuolist', methods=['GET', 'POST'])
@login_required
def fahuolist():
    # form = NameForm()
    # bujuan=None
    kehus = Kehu.query.filter_by(user=current_user._get_current_object()).order_by(
        Kehu.id)  # .order_by(Guke.outtime.desc())

    return render_template('fahuolist.html', kehus=kehus)  # form=form,


@main.route('/addkehu', methods=['GET', 'POST'])
@login_required
def addkehu():
    form = KehuForm()
    # bujuan=None
    kehus = Kehu.query.filter_by(user=current_user._get_current_object()).order_by(
        Kehu.id)  # .order_by(Guke.outtime.desc())

    user = current_user._get_current_object()
    if form.validate_on_submit():
        xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)

        kehu = Kehu(user=user, xiaoqu=xiaoqu, donghao=form.donghao.data, fanghao=form.fanghao.data,
                    chenghu=form.chenghu.data, tel=form.tel.data, status='No')

        db.session.add(kehu)
        flash('已成功添加客户')
        return redirect(url_for('main.kehulist'))

    return render_template('addkehu.html', form=form)


@main.route('/editkehu/<int:id>', methods=['GET', 'POST'])
@login_required
def editkehu(id):
    form = KehuForm()

    kehu = Kehu.query.get(id)
    user = current_user._get_current_object()

    if form.validate_on_submit():
        xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)

        kehu.xiaoqu = xiaoqu
        kehu.donghao = form.donghao.data
        kehu.fanghao = form.fanghao.data
        kehu.chenghu = form.chenghu.data
        kehu.tel = form.tel.data

        db.session.add(kehu)
        flash('已成功修改客户')
        return redirect(url_for('main.kehulist'))

    form.xiaoqu.data = kehu.xiaoqu.id
    form.donghao.data = kehu.donghao
    form.fanghao.data = kehu.fanghao
    form.chenghu.data = kehu.chenghu
    form.tel.data = kehu.tel

    return render_template('addkehu.html', form=form)


@main.route('/delkehu/<int:id>', methods=['GET', 'POST'])
@login_required
def delkehu(id):
    kehu = Kehu.query.get(id)
    db.session.delete(kehu)
    flash('已成功删除客户')

    return redirect(url_for('main.kehulist'))


@main.route('/showkehudd/<int:id>', methods=['GET', 'POST'])
@login_required
def showkehudd(id):
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
        elif chanpin.pinming == '晾衣架':
            toview = 'addlyj'
        elif chanpin.pinming == '纱窗':
            toview = 'addsc'
        elif chanpin.pinming == '指纹锁':
            toview = 'addzws'
        else:
            pass

        return redirect(url_for('main.' + toview, cpid=chanpinid, khid=kehu.id))

    return render_template('showkehudd.html', form=form, kehu=kehu)


# 隐形网
@main.route('/addyxw/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addyxw(cpid, khid):
    form = YxwForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():
        # xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          color=form.color.data, status='No')

        db.session.add(dingdan)

        flash('已成功添加订制')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# # 纱门
@main.route('/addsm/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addsm(cpid, khid):
    form = SmForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():
        # xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          color=form.color.data,
                          meikuan_digao=form.neikuan.data, shanshu=form.shanshu.data,
                          zhonghengtiaoshu_gantiaoshu=form.zhonghengtiaoshu.data,
                          shuowei=form.shuowei.data, zhangfa=form.zhangfa.data,
                          status='No')

        db.session.add(dingdan)

        flash('已成功添加订制')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# 晾衣架
@main.route('/addlyj/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addlyj(cpid, khid):
    form = LyjForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():
        # xiaoqu = Xiaoqu.query.get(form.xiaoqu.data)

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.chang.data, gao=form.gao.data,
                          zhonghengtiaoshu_gantiaoshu=form.gantiaoshu.data,
                          color=form.color.data, status='No')

        db.session.add(dingdan)

        flash('已成功添加订制')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# # 纱窗
@main.route('/addsc/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addsc(cpid, khid):
    form = ScForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():
        if form.ishaveht.data ==0:
            ishaveht = False
        else:
            ishaveht = True

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, kuan_chang=form.kuan.data, gao=form.gao.data,
                          color=form.color.data,
                          meikuan_digao=form.digao.data, dengfenshu=form.dengfenshu.data,
                          ishaveht=ishaveht,
                          shuowei=form.shuowei.data,
                          status='No')


        db.session.add(dingdan)

        flash('已成功添加订制')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


# # 指纹锁
@main.route('/addzws/<int:cpid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def addzws(cpid, khid):
    form = ZwsForm()

    chanpin = Chanpin.query.get(cpid)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    if form.validate_on_submit():

        dingdan = Dingdan(chanpin=chanpin, kehu=kehu, weizhi=form.weizhi.data, shuliang=form.shuliang.data,
                          xinghao=form.xinghao.data, color=form.color.data, shuowei=form.shuowei.data,
                          status='No')


        db.session.add(dingdan)

        flash('已成功添加订制')

        return redirect(url_for('main.showkehudd', id=khid))

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


@main.route('/deldingdan/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def deldingdan(ddid, khid):
    dingdan = Dingdan.query.get(ddid)
    db.session.delete(dingdan)
    flash('已成功删除客户')

    return redirect(url_for('main.showkehudd', id=khid))




@main.route('/editdingdan/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editdingdan(ddid,khid):

    dingdan = Dingdan.query.get(ddid)
    pinming = dingdan.chanpin.pinming

    #chanpin = Chanpin.query.get(dingdan.chanpin.id)

    if pinming == '隐形网':
        toview = 'edityxw'
    elif pinming == '纱门':
        toview = 'editsm'
    elif pinming == '晾衣架':
        toview = 'editlyj'
    elif pinming == '纱窗':
        toview = 'editsc'
    elif pinming == '指纹锁':
        toview = 'editzws'
    else:
        pass

    return redirect(url_for('main.' + toview, ddid=ddid, khid=khid))


# 隐形网
@main.route('/edityxw/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def edityxw(ddid, khid):
    form = YxwForm()

    if form.validate_on_submit():

        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi=form.weizhi.data
        dingdan.shuliang=form.shuliang.data
        dingdan.xinghao=form.xinghao.data
        dingdan.kuan_chang=form.kuan.data
        dingdan.gao=form.gao.data
        dingdan.color=form.color.data


        db.session.add(dingdan)

        flash('已成功修改订制')

        return redirect(url_for('main.showkehudd', id=khid))


    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = dingdan.shuliang
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)




# # 纱门
@main.route('/editsm/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editsm(ddid, khid):
    form = SmForm()

    if form.validate_on_submit():

        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi=form.weizhi.data
        dingdan.shuliang=form.shuliang.data
        dingdan.xinghao=form.xinghao.data
        dingdan.kuan_chang=form.kuan.data
        dingdan.gao=form.gao.data
        #dingdan.color=form.color.data

        dingdan.meikuan_digao = form.neikuan.data
        dingdan.shanshu = form.shanshu.data
        dingdan.zhonghengtiaoshu_gantiaoshu = form.zhonghengtiaoshu.data
        dingdan.shuowei = form.shuowei.data
        dingdan.zhangfa = form.zhangfa.data
        dingdan.color = form.color.data


        db.session.add(dingdan)

        flash('已成功修改订制')

        return redirect(url_for('main.showkehudd', id=khid))


    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = dingdan.shuliang
    form.xinghao.data = dingdan.xinghao
    form.kuan.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    form.neikuan.data = dingdan.meikuan_digao
    form.shanshu.data = dingdan.shanshu
    form.zhonghengtiaoshu.data = dingdan.zhonghengtiaoshu_gantiaoshu
    form.shuowei.data = dingdan.shuowei
    form.zhangfa.data = dingdan.zhangfa
    #form.color.data =dingdan.color


    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)



# # 晾衣架
@main.route('/editlyj/<int:ddid>/<int:khid>', methods=['GET', 'POST'])
@login_required
def editlyj(ddid, khid):
    form = LyjForm()

    if form.validate_on_submit():

        dingdan = Dingdan.query.get(ddid)

        dingdan.weizhi=form.weizhi.data
        dingdan.shuliang=form.shuliang.data
        dingdan.xinghao=form.xinghao.data
        dingdan.kuan_chang=form.chang.data
        dingdan.gao=form.gao.data
        dingdan.color=form.color.data

        dingdan.zhonghengtiaoshu_gantiaoshu = form.gantiaoshu.data


        db.session.add(dingdan)

        flash('已成功修改订制')

        return redirect(url_for('main.showkehudd', id=khid))


    dingdan = Dingdan.query.get(ddid)

    chanpin = Chanpin.query.get(dingdan.chanpin.id)
    kehu = Kehu.query.get(khid)

    # form.cpid.data = chanpin
    # form.khid.data = kehu.id

    form.weizhi.data = dingdan.weizhi
    form.shuliang.data = dingdan.shuliang
    form.xinghao.data = dingdan.xinghao
    form.chang.data = dingdan.kuan_chang
    form.gao.data = dingdan.gao
    form.color.data = dingdan.color

    form.gantiaoshu.data = dingdan.zhonghengtiaoshu_gantiaoshu


    return render_template('adddingdan.html', form=form, chanpin=chanpin, kehu=kehu)


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
