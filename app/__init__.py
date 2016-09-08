# -*- coding: utf-8 -*-

import logging
from os import environ
from flask import Flask
from flask_socketio import SocketIO
from logging.handlers import RotatingFileHandler
from celery import Celery
from geofinder.database import Database

app = Flask(__name__)
app.config.from_object('config')
# Override config if needed
if 'GEOFINDER_SETTINGS' in environ:
    app.config.from_envvar('GEOFINDER_SETTINGS')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

database = Database(app.config['DATABASE'])
database.init()

socketio = SocketIO(app)

update_pos_interval = app.config['UPDATE_POSITION_INTERVAL'] / 1000

from app import views

file_handler = RotatingFileHandler('geofinder.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('Startup')
