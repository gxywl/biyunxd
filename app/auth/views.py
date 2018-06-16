# _*_ encoding: utf-8 _*_
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.models import User
from .forms import LoginForm,ChangeUserNameForm
from . import auth


@auth.route('/loginto/<u>/<p>')
def loginto(u,p):
    user = User.query.filter_by(user=u).first()
    if user is not None and user.verify_pin(p):
        login_user(user)

        #管理账号转到管理页
        if user.isadm:
            return redirect(url_for('main.count'))
        else:
        #一般用户转转到首页..
            return redirect(request.args.get('next') or url_for('main.index'))
    flash('Invalid username or password')


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
            elif user.role == '业务员':
                # 一般用户转转到首页..
                return redirect(request.args.get('next') or url_for('main.kehulist'))
            elif user.role == '订货员':
                # 一般用户转转到首页..
                return redirect(request.args.get('next') or url_for('main.dinghuolist'))
            elif user.role == '发货员':
                # 一般用户转转到首页..
                return redirect(request.args.get('next') or url_for('main.fahuolist'))
            else:
            #一般用户转转到首页..
                # return redirect(request.args.get('next') or url_for('main.kehulist'))
                pass

            # #管理账号转到管理页
            # if user.isadm:
            #     return redirect(url_for('main.count'))
            # else:
            # #一般用户转转到首页..
            #     return redirect(request.args.get('next') or url_for('main.index'))



        flash('Invalid username or password')

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

