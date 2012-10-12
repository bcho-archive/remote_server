#coding: utf-8

from config import project_codename


def import_object(name, arg=None):
    if '.' not in name:
        return __import__(name)
    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1], arg)


def register_blueprint(app, blueprint):
    url_prefix = '/%s' % blueprint
    views = import_object('%s.%s.views' % (project_codename, blueprint))
    app.register_blueprint(views.app, url_prefix=url_prefix)
    return app
