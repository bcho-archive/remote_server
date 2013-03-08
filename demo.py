#coding: utf-8

from server.base import app
from server.models import db as server_db
from offline.views import app
from offline.models import db as offline_db


server_db.drop_all()
server_db.create_all()
offline_db.drop_all()
offline_db.create_all()
