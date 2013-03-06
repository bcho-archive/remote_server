#coding: utf-8

from flask import Blueprint, request, g, redirect

from offline.db import db

from offline.helpers import require_login

app = Blueprint('api', __name__)


@app.route('/', methods=['GET'])
def api():
    return 'hello api'


@app.route('/setup', methods=['GET'])
@require_login
def generate_token():
    g.user.api_token = g.user.encrypt()
    db.session.commit()
    callback = request.args.get('callback', None)
    if callback:
        callback = 'http://%s?token=%s&user_id=%s' % (
                callback, g.user.api_token, g.user.id)
        print callback
        return redirect(callback)
    return 'user_id: %s token: %s' % (g.user.id, g.user.api_token)
