# -*- coding: utf-8 -*-

import unittest
import os

from geofinder.database import Database

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

database_path = os.path.join(DIR_PATH, 'test_positions.db')
database = Database(database_path)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        database.init()

    def tearDown(self):
        os.remove(database_path)

    def test_store_position(self):
        database.store_position(
                {'latitude': 47.658236, 'timestamp': 1473361865, 'longitude': -2.7608470000000125, 'device_id': 'a'})

    def test_get_last_positions(self):
        database.store_position(
                {'latitude': 0, 'timestamp': 2, 'longitude': 0, 'device_id': 'a'})
        database.store_position(
                {'latitude': 0, 'timestamp': 3, 'longitude': 0, 'device_id': 'a'})
        database.store_position(
                {'latitude': 0, 'timestamp': 4, 'longitude': 0, 'device_id': 'b'})
        database.store_position(
                {'latitude': 0, 'timestamp': 1, 'longitude': 0, 'device_id': 'c'})

        last_positions = database.get_last_positions(1)

        self.assertEquals(len(last_positions), 2)
        self.assertEquals(last_positions[0]['device_id'], 'b')
        self.assertEquals(last_positions[1]['device_id'], 'a')
        self.assertEquals(last_positions[1]['timestamp'], 3)
