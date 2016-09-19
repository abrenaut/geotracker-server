# CDN URL
STATIC_URL = ''

# Celery Broker URL
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# The name of the sqlite database
DATABASE = 'positions.db'

# The number of milliseconds between each positions update
UPDATE_POSITION_INTERVAL = 2000

# A custom socketio path
SOCKETIO_PATH = '/geotracker_socket.io'
