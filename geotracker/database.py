# -*- coding: utf-8 -*-

import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    def __init__(self, database):
        self.database = database

    def init(self):
        conn = sqlite3.connect(self.database)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS positions (
                    device_id INTEGER,
                    latitude REAL,
                    longitude REAL,
                    timestamp INTEGER
                )
                """)
            cursor.execute("CREATE INDEX IF NOT EXISTS position_device_id_idx ON positions (device_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS position_timestamp_idx ON positions (timestamp)")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def store_position(self, position):
        conn = sqlite3.connect(self.database)
        try:
            cursor = conn.cursor()
            cursor.execute("""
              INSERT INTO positions (device_id, latitude, longitude, timestamp)
                VALUES (:device_id, :latitude, :longitude, :timestamp)""",
                           (position.device_id, position.latitude, position.longitude, position.timestamp))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_last_positions(self, min_timestamp):
        conn = sqlite3.connect(self.database)
        conn.row_factory = dict_factory
        try:
            cursor = conn.cursor()
            cursor.execute("""
              SELECT pos.device_id, pos.latitude, pos.longitude, pos.timestamp
                FROM positions pos
                JOIN (SELECT device_id, MAX(timestamp) AS max_timestamp FROM positions WHERE timestamp > ? GROUP BY device_id) new_pos
                  ON pos.device_id = new_pos.device_id AND pos.timestamp = new_pos.max_timestamp
                """, (min_timestamp,))
            positions = cursor.fetchall()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

        return positions
