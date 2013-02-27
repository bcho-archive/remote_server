#coding: utf-8

from flask import Blueprint, request, redirect, url_for, abort, render_template

from server.queuer import waitings
from server.base import db
from .models import Tweet
from .config import current_user

app = Blueprint('offline', __name__, static_folder='static',
        template_folder='templates')


@app.route('/')
@app.route('/timeline')
def timeline():
    tweets = Tweet.query.all()
    tweets.reverse()
    return render_template('timeline.html', tweets=tweets)


@app.route('/compose', methods=['POST'])
def compose():
    if request.method == 'POST':
        parent_id = request.form.get('parent_id', None)
        parent_id = None if parent_id == '0' else parent_id
        t = Tweet(request.form['content'], current_user, parent_id)
        db.session.add(t)
        db.session.commit()
        waitings.enqueue(t.content, t.id, current_user)
        return redirect(url_for('.timeline'))
    abort(403)


@app.route('/tweet/<int:id>', methods=['GET'])
def view_tweet(id):
    tweet = Tweet.query.filter_by(id=id).first_or_404()
    return tweet.content
