#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app import db



class Article(db.Model):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    intro = Column(String(300), nullable=False)
    title = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Article %r>" % self.id


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    # role = Column(Boolean, default=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.full_name}, {self.login}'


class Facts(db.Model):
    __tablename__ = 'facts'

    id_fact = Column(Integer, primary_key=True, autoincrement=True)
    intro_fact = Column(String(200), nullable=False)
    title_fact = Column(String(100), nullable=False)
    text_fact = Column(Text, nullable=False)
    date_fact = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Facts %r>" % self.id_fact
