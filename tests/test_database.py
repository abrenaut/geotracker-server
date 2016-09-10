# -*- coding: utf-8 -*-

import unittest
import os

from geotracker.database import Database
from geotracker.position import Position

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

database_path = os.path.join(DIR_PATH, 'test_positions.db')
database = Database(database_path)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        database.init()

    def tearDown(self):
        os.remove(database_path)

    def test_store_position(self):
        database.store_position(Position('uid', 47, -2.3, 1473361865))

    def test_get_last_positions(self):
        database.store_position(Position('a', 0, 0, 2))
        database.store_position(Position('a', 0, 0, 3))
        database.store_position(Position('b', 0, 0, 4))
        database.store_position(Position('c', 0, 0, 1))

        last_positions = database.get_last_positions(1)

        self.assertEquals(len(last_positions), 2)
        self.assertEquals(last_positions[0]['device_id'], 'a')
        self.assertEquals(last_positions[1]['device_id'], 'b')
        self.assertEquals(last_positions[0]['timestamp'], 3)
