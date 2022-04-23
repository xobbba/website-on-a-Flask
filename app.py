#!/usr/bin/env python
# -*- coding: utf-8 -*-
import secrets

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///web.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = secrets.token_hex(16)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
login_manager.init_app(app)

from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


from auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from main import main as main_blueprint

app.register_blueprint(main_blueprint)

login_manager.login_message = 'Для начала нужно авторизоваться'

if __name__ == '__main__':
    app.run(
        debug=False,
        SESSION_COOKIE_HTTPONLY=False,
        REMEMBER_COOKIE_HTTPONLY=False,
        SESSION_COOKIE_SAMESITE="None"
    )
