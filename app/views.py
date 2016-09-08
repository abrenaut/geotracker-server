# -*- coding: utf-8 -*-

from urlparse import urljoin
from flask import render_template, url_for, request, abort, jsonify
from app import app, socketio, update_pos_interval
from tasks import update_positions, store_position

update_pos_task = None


@app.template_global()
def static_url_for(filename):
    static_url = app.config.get('STATIC_URL')

    if static_url:
        return urljoin(static_url, filename)

    return url_for('static', filename=filename)


@socketio.on('connect')
def connect():
    global update_pos_task

    if not update_pos_task:
        print 'go'
        update_pos_task = socketio.start_background_task(target=update_positions, interval=update_pos_interval)


@app.route('/')
def render_map():
    return render_template('map.html')


@app.route('/api/1.0/positions', methods=['POST'])
def store_position():
    if not request.json:
        abort(400)
    store_position.delay(request.json)
    return jsonify({}), 202
