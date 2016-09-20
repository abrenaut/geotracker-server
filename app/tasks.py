# -*- coding: utf-8 -*-

from app import celery, database, socketio


@celery.task
def store_position(position):
    # Store the position asynchronously
    database.store_position(position)


class UpdatePositionTask:
    """
    Starts a background task that new devices positions to clients
    """

    def __init__(self, interval):
        self.interval = interval
        self.task = None
        self.new_positions = []

    def is_started(self):
        # Is the background task already created
        return self.task is not None

    def start(self):
        # Start the background task that send new positions to clients
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
