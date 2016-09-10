# -*- coding: utf-8 -*-
class Position:
    def __init__(self, device_id, latitude, longitude, timestamp):
        self.device_id = device_id
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

    @staticmethod
    def from_dict(pos_dict):
        try:
            position = Position(pos_dict['uid'], pos_dict['lat'], pos_dict['lng'], pos_dict['time'])
        except KeyError:
            position = None

        return position
