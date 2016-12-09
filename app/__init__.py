# -*- coding: utf-8 -*-

import logging
from os import environ
from flask import Flask
from flask_socketio import SocketIO
from logging.handlers import RotatingFileHandler
from celery import Celery
from geotracker.database import Database


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.config.update(dict(
        STATIC_URL=environ.get('STATIC_URL', ''),
        UPDATE_POSITION_INTERVAL=environ.get('UPDATE_POSITION_INTERVAL', 2000),
        DATABASE=environ.get('DATABASE', 'positions.db'),
        AMQP_URL=environ.get('AMQP_URL', 'amqp://guest@rabbitmq:5672//'),
        SOCKETIO_PATH=environ.get('SOCKETIO_PATH', '/geotracker_socket.io')
))

celery = Celery(app.name, broker=app.config['AMQP_URL'])
celery.conf.update(app.config)

database = Database(app.config['DATABASE'])
database.init()

socketio_path = app.config['SOCKETIO_PATH']
socketio = SocketIO(app, path=socketio_path)

update_pos_interval = int(app.config['UPDATE_POSITION_INTERVAL']) / 1000

from app import views

file_handler = RotatingFileHandler('geotracker.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('Startup')
