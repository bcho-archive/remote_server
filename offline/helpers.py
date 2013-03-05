#coding: utf-8

import functools

from flask import g, redirect, url_for, session

from models import User


def require_login(call):
    @functools.wraps(call)
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(url_for('login'))
        return call(*args, **kwargs)
    return wrapper


def user_login(user):
    session['id'] = user.id
    session['token'] = user.login_token
    session.permanet = True
    g.user = user
    return user


def user_logout():
    if not 'id' in session:
        return
    session.pop('id')
    session.pop('token')


def get_current_user():
    if session.get('id', None) and session.get('token', None):
        user = User.query.filter_by(login_token=session.get('token')).first()
        if not (user and user.id == session.get('id')):
            user = None
    else:
        user = None
    return user
