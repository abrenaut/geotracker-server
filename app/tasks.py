# -*- coding: utf-8 -*-

from app import celery, database, socketio


@celery.task
def store_position(position):
    database.store_position(position)


def update_positions(interval):
    while True:
        updated_positions = database.get_last_positions(0)

        socketio.emit('positions_update', {'positions' : updated_positions})

        # Give the players some time to answer
        socketio.sleep(interval)
