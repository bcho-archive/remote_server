#coding: utf-8

import functools

from flask import request as r

from offline.models import User 


def require_token(call):
    @functools.wraps(call)
    def wrapper(*args, **kwargs):
        token = r.args.get('token', '')
        user = User.query.filter_by(api_token=token).first()
        if not user:
            return 'token required'
        kwargs['user'] = user
        return call(*args, **kwargs)
    return wrapper
