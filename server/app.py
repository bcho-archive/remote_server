#coding: utf-8

from flask import jsonify

from base import app
from utils import register_blueprint


#: register blueprints
for blueprint in ['arm', 'weibot']:
    register_blueprint(app, blueprint)


#: error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify(message='Not found.'), 404
