# -*- coding: utf-8 -*-

from urlparse import urljoin
from flask import render_template, url_for, request, abort, jsonify
from app import app, socketio, update_pos_interval, database, socketio_path
from geotracker.position import Position
import datetime
import tasks

update_pos_task = tasks.UpdatePositionTask(update_pos_interval)


@app.template_global()
def static_url_for(filename):
    # Transform relative URLs to CDN URLs
    static_url = app.config.get('STATIC_URL')

    if static_url:
        return urljoin(static_url, filename)

    return url_for('static', filename=filename)


@socketio.on('connect')
def connect():
    # Launch the update positions task once a user is connected
    if not update_pos_task.is_started():
        update_pos_task.start()


@app.route('/')
def render_map():
    # Show the positions recorded recently to the user
    now = datetime.datetime.now()
    min_date = now - datetime.timedelta(days=1)
    min_timestamp = min_date.strftime("%s")

    positions = database.get_last_positions(min_timestamp)

    return render_template('map.html', positions=positions, socketio_path=socketio_path)


@app.route('/api/1.0/positions', methods=['POST'])
def store_position():
    if not request.json:
        abort(400)

    position = Position.from_dict(request.json)
    if not position:
        abort(400)

    # Add the position to the list of new positions to display to users
    update_pos_task.new_positions.append(position)

    # Store the position asynchronously
    tasks.store_position.delay(position)

    return jsonify({}), 202
