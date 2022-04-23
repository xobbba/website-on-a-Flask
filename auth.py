#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from app import db


auth = Blueprint('auth', __name__)


@auth.route('/signin')
def signin():
    return render_template('signin.html')


@auth.route('/signin', methods=['POST'])
def signin_post():
    login = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(login=login).first()

    if not user or not check_password_hash(user.password, password):
        flash('Неправильный логин или пароль')
        return redirect(url_for('auth.signin'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    login = request.form.get('login')
    password = request.form.get('password')

    if len(password) < 7 or len(login) < 5:
        flash('Введены неверные данные')
        return redirect(url_for('auth.signup'))

    full_name = request.form.get('full_name')

    user = User.query.filter_by(login=login).first()
    if user:
        flash('Пользователь с таким Login уже существует')
        return redirect(url_for('auth.signup'))

    new_user = User(
        login=login,
        full_name=full_name,
        password=generate_password_hash(password, method='sha256')
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.signin'))
