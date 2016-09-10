# -*- coding: utf-8 -*-

from app import celery, database, socketio


@celery.task
def store_position(position):
    database.store_position(position)


class UpdatePositionTask:
    def __init__(self, interval):
        self.interval = interval
        self.task = None
        self.new_positions = []

    def is_started(self):
        return self.task is not None

    def start(self):
        self.task = socketio.start_background_task(target=self.run)

    def run(self):
        while True:

            if self.new_positions:
                # Send the new positions to clients
                socketio.emit('positions_update',
                              {'positions': [position.__dict__ for position in self.new_positions]})
                # Reset the list of new positions
                del self.new_positions[:]

            # Wait for a while before sending positions updates
            socketio.sleep(self.interval)
