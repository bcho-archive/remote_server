#coding: utf-8

from flask import request, abort, render_template, redirect, url_for
from flask import g

from app import app, db
from models import User
from helpers import require_login, user_login, user_logout, get_current_user


@app.before_request
def before_request():
    g.user = get_current_user()


@app.route('/')
@require_login
def timeline():
    return render_template('timeline.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = User.query.filter_by(
                username=request.form['username']).first_or_404()
        if user.login(request.form['password']):
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
