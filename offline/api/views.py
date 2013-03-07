#coding: utf-8

from flask import Blueprint, request, g, redirect, jsonify

from offline.db import db
from offline.helpers import require_login
from offline.models import Tweet

from .helpers import require_token

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
        callback = 'http://%s?token=%s&user_id=%s&user_name=%s' % (
                callback, g.user.api_token, g.user.id, g.user.username)
        return redirect(callback)
    return 'user_id: %s token: %s' % (g.user.id, g.user.api_token)


@app.route('/tweet', methods=['POST'])
@require_token
def tweet(user):
    content = request.form['content']
    image = request.form.get('image', None)
    t = Tweet(content, user.id, image=image)
    db.session.add(t)
    db.session.commit()
    return jsonify(id=t.id)


@app.route('/tweet/update/<int:last_id>', methods=['GET'])
@require_login
def check_update(last_id):
    t = Tweet.query.order_by('id desc').first()
    return jsonify(last_id=t.id)


@app.route('/retweet', methods=['POST'])
@require_token
def retweet(user):
    content = request.form['content']
    retweet_id = request.form['retweet_id']
    t = Tweet(content, user.id, retweet_id=retweet_id)
    db.session.add(t)
    db.session.commit()
    return jsonify(id=t.id)


@app.route('/mention', methods=['GET'])
@require_token
def mention(user):
    def j(tweet_id):
        tweet = Tweet.query.filter_by(id=tweet_id).first()
        if tweet:
            return {
                    'id': tweet.id,
                    'content': tweet.content,
                    'author_id': tweet.author_id,
                    'name': tweet.author.username
            }

    return jsonify({'mentions': [j(i) for i in user.mentions]})
