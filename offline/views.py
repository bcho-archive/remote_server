#coding: utf-8

import re

from flask import request, abort, render_template, redirect, url_for
from flask import g

from app import app, db
from models import User, Tweet, Mention
from helpers import require_login, user_login, user_logout, get_current_user


@app.before_request
def before_request():
    g.user = get_current_user()


@app.route('/')
@require_login
def timeline():
    timeline = Tweet.query.order_by('id desc').all()
    return render_template('timeline.html', timeline=timeline)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = User.query.filter_by(
                username=request.form['username']).first()
        if user and user.login(request.form['password']):
            db.session.commit()
            user_login(user)
            return redirect(url_for('.timeline'))
        else:
            error = 'login failed'
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
@require_login
def logout():
    user_logout()
    return redirect(url_for('.login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if username and password and User.is_name_unique(username):
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('.login'))
        else:
            error = 'create failed'
    return render_template('signup.html', error=error)


@app.route('/tweet/create', methods=['POST'])
@require_login
def create_tweet():
    content = request.form['content']

    tweet = Tweet(content, g.user.id)
    db.session.add(tweet)
    db.session.commit()
    
    pattern = re.compile('@(\w+)')
    for name in pattern.findall(content):
        user = User.query.filter_by(username=name).first()
        if Mention.validate(user.id, tweet.id) and user is not g.user:
            mention = Mention(user.id, tweet.id)
            db.session.add(mention)
    db.session.commit()

    return redirect(url_for('timeline'))
