# _*_ encoding: utf-8 _*_
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.models import User
from .forms import LoginForm, ChangeUserNameForm, ChangePinForm
from . import auth


@auth.route('/loginto/<u>/<p>')
def loginto(u,p):
    user = User.query.filter_by(user=u).first()
    if user is not None and user.verify_pin(p):
        login_user(user)

        # #管理账号转到管理页
        # if user.isadm:
        #     return redirect(url_for('main.count'))
        # else:
        # #一般用户转转到首页..
        #     return redirect(request.args.get('next') or url_for('main.index'))

        # 管理账号转到管理页
        if user.role == 'adm':
            return redirect(url_for('admin.index'))

        # pass
        elif user.role == '进度客服':
            # 一般用户转转到首页..
            return redirect(url_for('main.kefucxlist'))  # request.args.get('next') or

        # pass
        elif user.role == '业务员':
            # 一般用户转转到首页..
            return redirect(url_for('main.kehulist')) #request.args.get('next') or
        elif user.role == '订货员':
            # 一般用户转转到首页..
            return redirect(url_for('main.dinghuolist')) #request.args.get('next') or

        elif user.role == '入库员':
            # 一般用户转转到首页..
            return redirect(url_for('main.rukulist'))

        # elif user.role == '出库员':
        #     # 一般用户转转到首页..
        #     return redirect(url_for('main.qukulist'))

        elif user.role == '发货员':
            # 一般用户转转到首页..
            return redirect(url_for('main.fahuolist'))
        else:
            # 一般用户转转到首页..
            # return redirect(request.args.get('next') or url_for('main.kehulist'))
            flash('角色有误')

    else:
        flash('用户名或密码错误')


@auth.route('/login', methods=['Get', 'Post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.user.data).first()
        if user is not None and user.verify_pin(form.pin.data):
            login_user(user, form.remember_me.data)

            #管理账号转到管理页
            if user.role == 'adm':
                return redirect(url_for('admin.index'))

            # pass
            elif user.role == '进度客服':
                # 一般用户转转到首页..
                return redirect(url_for('main.kefucxlist'))  # request.args.get('next') or

            # pass
            elif user.role == '业务员':
                # 一般用户转转到首页..
                return redirect(url_for('main.kehulist')) #request.args.get('next') or
            elif user.role == '订货员':
                # 一般用户转转到首页..
                return redirect(url_for('main.dinghuolist'))

            elif user.role == '入库员':
                # 一般用户转转到首页..
                return redirect(url_for('main.rukulist'))

            elif user.role == '发货员':
                # 一般用户转转到首页..
                return redirect(url_for('main.fahuolist'))
            #
            # elif user.role == '发货员':
            #     # 一般用户转转到首页..
            #     return redirect(url_for('main.fahuolist'))
            else:
            #一般用户转转到首页..
                # return redirect(request.args.get('next') or url_for('main.kehulist'))
                flash('角色有误')

            # #管理账号转到管理页
            # if user.isadm:
            #     return redirect(url_for('main.count'))
            # else:
            # #一般用户转转到首页..
            #     return redirect(request.args.get('next') or url_for('main.index'))

        else:
            flash('用户名或密码错')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))



@auth.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUserNameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your username has been updated.')
        return redirect(url_for('main.index'))
    form.username.data = current_user.username
    return render_template("auth/change_username.html", form=form)


@auth.route('/change-pin', methods=['GET', 'POST'])
@login_required
def change_pin():
    form = ChangePinForm()
    if form.validate_on_submit():
        if current_user.pin == form.opin.data:
            current_user.pin = form.npin.data
            db.session.add(current_user)
            db.session.commit()
            flash('你的口令已更改了.')
            return redirect(url_for('main.index'))
        else:
            flash('原口令不对.')
    # form.pin.data = current_user.pin
    return render_template("auth/change_pin.html", form=form)
