#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from flask_login import login_required, current_user
from models import Article, Facts
from app import db


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    return render_template("index.html")


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@main.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@main.route('/posts/<int:id>/del')
@login_required
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@main.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    article = Article.query.get(id)

    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"

    else:
        return render_template("post_update.html", article=article)


@main.route('/create-article', methods=['POST', 'GET'])
@login_required
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")


@main.route('/facts')
def facts():
    fact = Facts.query.order_by(Facts.date_fact.desc()).all()
    return render_template("facts.html", fact=fact)


@main.route('/facts/<int:id_fact>')
def facts_details(id_fact):
    fact = Facts.query.get(id_fact)
    return render_template("facts_details.html", fact=fact)


@main.route('/facts/<int:id_fact>/del')
@login_required
def facts_delete(id_fact):
    fact = Facts.query.get_or_404(id_fact)

    try:
        db.session.delete(fact)
        db.session.commit()
        return redirect('/facts')
    except Exception:
        return "При удалении факта произошла ошибка"


@main.route('/facts/<int:id_fact>/update', methods=['POST', 'GET'])
@login_required
def facts_update(id_fact):
    fact = Facts.query.get(id_fact)

    if request.method == "POST":
        fact.title_fact = request.form['title_fact']
        fact.intro_fact = request.form['intro_fact']
        fact.text_fact = request.form['text_fact']

        try:
            db.session.commit()
            return redirect('/facts')
        except Exception:
            return 'При редактировании факта произошла ошибка'

    else:
        return render_template("facts_update.html", fact=fact)


@main.route('/create-facts', methods=['POST', 'GET'])
@login_required
def create_facts():
    if request.method == 'POST':
        title_fact = request.form['title_fact']
        intro_fact = request.form['intro_fact']
        text_fact = request.form['text_fact']

        fact = Facts(title_fact=title_fact, intro_fact=intro_fact, text_fact=text_fact)

        try:
            db.session.add(fact)
            db.session.commit()
            return redirect('/facts')
        except Exception:
            return 'При добавление факта произошла ошибка'

    else:
        return render_template("create-facts.html", facts=facts)


@main.route('/robots.txt')
def robots():
    with open('robots.txt', 'r') as file:
        response = make_response(file.read())
        response.headers['Content-type'] = 'text/plane'
    return response


@main.route('/sitemap.xml')
def sitemap():
    with open('sitemap.xml', 'r') as file:
        response = make_response(file.read())
        response.headers['Content-type'] = 'text/plane'
    return response


@main.route('/vk.html')
def vk():
    return render_template('vk.html')
