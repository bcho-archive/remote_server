#coding: utf-8

from werkzeug.utils import import_string

from config import project_codename


def register_blueprint(app, blueprint):
    url_prefix = '/%s' % blueprint
    views = import_string('%s.%s.views' % (project_codename, blueprint))
    app.register_blueprint(views.app, url_prefix=url_prefix)
    return app
